"""Generate the numerical data plotted in the slides (CSV files in presentation/data/).

  h2_curves.csv        H2 / STO-3G: RHF, 2x2 CI (= FCI), triplet, open-shell singlet vs R (bohr)
  hubbard_gap.csv      E(T) - E(S) vs U for CBD, TME (disjoint) and TMM, MX (nondisjoint), t = 1
  spin_density.csv     pentadienyl radical site spin densities for several U (Hubbard, exact)
  yamaguchi.csv        Yamaguchi J vs exact J for the Hubbard dimer
Usage:  OMP_NUM_THREADS=2 uv run --project .. python -I scripts/make_data.py   (from presentation/)
"""
import csv
import itertools
import pathlib

import numpy as np
from pyscf import ao2mo, gto, scf

OUT = pathlib.Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)


def write(name, header, rows):
    with open(OUT / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", name, len(rows), "rows")


# ---------------------------------------------------------------- H2 minimal basis
def h2(R):
    m = gto.M(atom=f"H 0 0 0; H 0 0 {R}", basis="sto-3g", unit="Bohr", verbose=0)
    mf = scf.RHF(m).run(conv_tol=1e-12)
    C = mf.mo_coeff
    h = C.T @ (m.intor("int1e_kin") + m.intor("int1e_nuc")) @ C
    g = ao2mo.restore(1, ao2mo.kernel(m, C), 2)
    vnn = m.energy_nuc()
    J11, J22, J12, K12 = g[0, 0, 0, 0], g[1, 1, 1, 1], g[0, 0, 1, 1], g[0, 1, 0, 1]
    e1, e2 = 2 * h[0, 0] + J11, 2 * h[1, 1] + J22
    eci = 0.5 * (e1 + e2 - np.sqrt((e2 - e1) ** 2 + 4 * K12**2))
    et = h[0, 0] + h[1, 1] + J12 - K12
    eoss = h[0, 0] + h[1, 1] + J12 + K12
    return e1 + vnn, eci + vnn, et + vnn, eoss + vnn


eH = scf.UHF(gto.M(atom="H 0 0 0", basis="sto-3g", spin=1, verbose=0)).run().e_tot
rows = []
for R in np.round(np.concatenate([np.arange(0.8, 3.0, 0.1), np.arange(3.0, 8.01, 0.25)]), 3):
    rows.append([R, *[round(x, 6) for x in h2(R)], round(2 * eH, 6)])
write("h2_curves.csv", ["R", "RHF", "CI", "T", "OSS", "twoEH"], rows)


# ---------------------------------------------------------------- Hubbard exact diagonalisation
def hubbard(edges, n, nup, ndn, U, t=1.0):
    ups = [sum(1 << i for i in c) for c in itertools.combinations(range(n), nup)]
    dns = [sum(1 << i for i in c) for c in itertools.combinations(range(n), ndn)]

    def hop(states):
        idx = {s: k for k, s in enumerate(states)}
        T = np.zeros((len(states), len(states)))
        for k, s in enumerate(states):
            for i, j in edges:
                for a, b in ((i, j), (j, i)):
                    if (s >> b) & 1 and not (s >> a) & 1:
                        lo, hi = min(a, b), max(a, b)
                        sign = (-1) ** bin(s & (((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1))).count("1")
                        T[idx[s ^ (1 << b) ^ (1 << a)], k] += -t * sign
        return T

    H = np.kron(hop(ups), np.eye(len(dns))) + np.kron(np.eye(len(ups)), hop(dns))
    H += U * np.diag([bin(u & d).count("1") for u in ups for d in dns])
    return H, ups, dns


def ring(n):
    return [(i, (i + 1) % n) for i in range(n)]


graphs = {
    "CBD": (4, ring(4)), "TME": (6, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)]),
    "TMM": (4, [(0, 1), (0, 2), (0, 3)]), "MX": (8, ring(6) + [(0, 6), (2, 7)]),
}
Us = [0.05, 0.1, 0.2, 0.4, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0]
rows = []
for U in Us:
    row = [U]
    for name, (n, edges) in graphs.items():
        e0 = np.linalg.eigvalsh(hubbard(edges, n, n // 2, n - n // 2, U)[0])
        e1 = np.linalg.eigvalsh(hubbard(edges, n, n // 2 + 1, n - n // 2 - 1, U)[0])
        e_sing = next(e for e in e0 if np.min(np.abs(e1 - e)) > 1e-9)
        row.append(round(e1[0] - e_sing, 8))           # >0: singlet below triplet
    rows.append(row)
write("hubbard_gap.csv", ["U", *graphs], rows)

# spin densities of the pentadienyl radical
chain = [(i, i + 1) for i in range(4)]
rows = []
for U in (0.0, 1.0, 3.0, 6.0):
    H, ups, dns = hubbard(chain, 5, 3, 2, U)
    w, v = np.linalg.eigh(H)
    p = (v[:, 0].reshape(len(ups), len(dns))) ** 2
    rho = [sum(p[a, b] * (((ups[a] >> i) & 1) - ((dns[b] >> i) & 1))
               for a in range(len(ups)) for b in range(len(dns))) for i in range(5)]
    rows.append([U, *[round(r, 5) for r in rho]])
write("spin_density.csv", ["U", "s1", "s2", "s3", "s4", "s5"], rows)


# ---------------------------------------------------------------- Yamaguchi projection, Hubbard dimer
def bs_uhf(U, t=1.0):
    na = np.array([0.95, 0.05]); nb = na[::-1].copy()
    for _ in range(20000):
        Fa = np.array([[U * nb[0], -t], [-t, U * nb[1]]]); Fb = np.array([[U * na[0], -t], [-t, U * na[1]]])
        ea, Ca = np.linalg.eigh(Fa); eb, Cb = np.linalg.eigh(Fb)
        na_n, nb_n = Ca[:, 0] ** 2, Cb[:, 0] ** 2
        if np.allclose(na_n, na, atol=1e-14) and np.allclose(nb_n, nb, atol=1e-14):
            break
        na, nb = 0.5 * (na + na_n), 0.5 * (nb + nb_n)
    E = ea[0] + eb[0] - U * na @ nb
    return E, 1 - (Ca[:, 0] @ Cb[:, 0]) ** 2


rows = []
for U in np.round(np.arange(2.2, 16.01, 0.2), 2):
    E_bs, s2 = bs_uhf(U)
    j_y = E_bs / (2 - s2)
    j_ex = (U - np.sqrt(U**2 + 16)) / 4
    rows.append([U, round(j_y, 6), round(j_ex, 6), round(s2, 5)])
write("yamaguchi.csv", ["U", "Jyam", "Jexact", "S2BS"], rows)
