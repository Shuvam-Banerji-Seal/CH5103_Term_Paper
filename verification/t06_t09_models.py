"""Model-Hamiltonian tests.
T6: two-orbital singlet CI vs orbital gap Delta (D7).
T7: two-site (extended) Hubbard model, exact vs analytic and vs -4t^2/U (D8).
T8: Hückel NBMOs: zero-sum rule, pairing theorem, Longuet-Higgins count, disjointness (D9).
T9: Hubbard exact diagonalisation of pi-diradicals: ground-state S vs Ovchinnikov/Lieb,
    and spin-density alternation (dynamic spin polarisation) in pentadienyl (D10).
T14: broken-symmetry UHF + Yamaguchi projection on the Hubbard dimer (D18).
"""
import itertools
import numpy as np
import sympy as sp
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh

ok = True

# ------------------------------------------------------------------ T6
D, K, Jd, Jx = sp.symbols("Delta K J_d J_x", positive=True)
Hs = sp.Matrix([[-D + Jd, K], [K, D + Jd]])          # |a a-bar>, |b b-bar>, h_a=-D/2, h_b=+D/2
evals = Hs.eigenvals()
E_S = Jd - sp.sqrt(D**2 + K**2)
c6 = E_S in evals
E_T = Jx - K
gap = sp.simplify(E_S - E_T)
# ground-state coefficients: c2/c1 = (E_S - H11)/K
ratio = sp.simplify((E_S - (-D + Jd)) / K)
lim0 = sp.limit(ratio, D, 0)                          # -> -1 : equal weights, pure diradical
liminf = sp.limit(ratio, D, sp.oo)                    # -> 0  : closed shell
print(f"T6: E_S root {c6}; E_S-E_T = {gap}; c2/c1 = {ratio}; Delta->0: {lim0}; Delta->inf: {liminf}")
ok &= c6 and lim0 == -1 and liminf == 0

# ------------------------------------------------------------------ helpers: fermionic ED
def hubbard_ham(edges, nsite, nup, ndn, t=1.0, U=1.0):
    """Sparse Hubbard H = -t sum_<ij>,s (c+_is c_js + h.c.) + U sum_i n_iu n_id, fixed (nup, ndn).
    Basis: product of up and down occupation bit-strings; Jordan-Wigner order: all up, then all down."""
    ups = [sum(1 << i for i in c) for c in itertools.combinations(range(nsite), nup)]
    dns = [sum(1 << i for i in c) for c in itertools.combinations(range(nsite), ndn)]
    iu = {s: k for k, s in enumerate(ups)}; idn = {s: k for k, s in enumerate(dns)}
    nU, nD = len(ups), len(dns)
    def hop_list(states, index):
        rows, cols, vals = [], [], []
        for k, s in enumerate(states):
            for i, j in edges:
                for a, b in ((i, j), (j, i)):           # c+_a c_b
                    if (s >> b) & 1 and not (s >> a) & 1:
                        s2 = s ^ (1 << b) ^ (1 << a)
                        lo, hi = min(a, b), max(a, b)
                        sign = (-1) ** bin(s & (((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1))).count("1")
                        rows.append(index[s2]); cols.append(k); vals.append(-t * sign)
        return sps.csr_matrix((vals, (rows, cols)), shape=(len(states), len(states)))
    Tu, Td = hop_list(ups, iu), hop_list(dns, idn)
    H = sps.kron(Tu, sps.identity(nD)) + sps.kron(sps.identity(nU), Td)
    dbl = np.array([bin(u & d).count("1") for u in ups for d in dns], dtype=float)
    H = H + U * sps.diags(dbl)
    return H.tocsr(), ups, dns

def ground(H, k=1):
    if H.shape[0] <= 400:
        w, v = np.linalg.eigh(H.toarray()); return w[:k], v[:, :k]
    w, v = eigsh(H, k=k, which="SA", tol=1e-12); o = np.argsort(w); return w[o], v[:, o]

# ------------------------------------------------------------------ T7
t, U, V, k = sp.symbols("t U V k", positive=True)
# localized basis l, r ; singlets: covalent (l r), ionic+ (l^2 + r^2)/sqrt2, ionic- ; triplet
E_T7 = V - k
Hcov_ion = sp.Matrix([[V + k, 2 * t], [2 * t, U + k]])   # covalent / ionic(+) block (h_lr = -t)
E_S7 = (U + V + 2 * k - sp.sqrt((U - V) ** 2 + 16 * t**2)) / 2
c7a = sp.simplify(sorted(Hcov_ion.eigenvals().keys(), key=str)[0] - E_S7) == 0 or \
      any(sp.simplify(e - E_S7) == 0 for e in Hcov_ion.eigenvals())
series = sp.series((E_S7 - E_T7).subs({V: 0, k: 0}), t, 0, 4).removeO()
print(f"T7 analytic: E_S-E_T = {sp.simplify(E_S7 - E_T7)}; Hubbard (V=k=0) series: {sp.simplify(series)}")
c7b = sp.simplify(series + 4 * t**2 / U) == 0
# numeric check with the general 2e/2o FCI (localized integrals) for one parameter set
from pyscf import fci
tv, Uv, Vv, kv = 1.0, 6.0, 1.5, 0.2
h = np.array([[0.0, -tv], [-tv, 0.0]])
g = np.zeros((2, 2, 2, 2)); g[0, 0, 0, 0] = g[1, 1, 1, 1] = Uv
g[0, 0, 1, 1] = g[1, 1, 0, 0] = Vv
for (p, q, r, s) in [(0, 1, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0), (1, 0, 0, 1)]:
    g[p, q, r, s] = kv
e_all, cs = fci.direct_spin1.FCI().kernel(h, g, 2, (1, 1), nroots=4)
sing = [e for e, c in zip(e_all, cs) if fci.spin_op.spin_square0(c, 2, (1, 1))[0] < 1]
trip = [e for e, c in zip(e_all, cs) if fci.spin_op.spin_square0(c, 2, (1, 1))[0] > 1]
subs = {t: tv, U: Uv, V: Vv, k: kv}
c7c = np.isclose(min(sing), float(E_S7.subs(subs))) and np.isclose(trip[0], float(E_T7.subs(subs)))
# Hubbard ED engine cross-check on the dimer
Hd, _, _ = hubbard_ham([(0, 1)], 2, 1, 1, t=1.0, U=6.0)
w = np.linalg.eigvalsh(Hd.toarray())
c7d = np.isclose(w[0], (6 - np.sqrt(36 + 16)) / 2)
print(f"T7: eig match {c7a}, -4t^2/U leading term {c7b}, FCI(ext. Hubbard) match {c7c}, ED engine {c7d}")
ok &= bool(c7a and c7b and c7c and c7d)

# ------------------------------------------------------------------ molecules (pi graphs)
def ring(n, start=0): return [(start + i, start + (i + 1) % n) for i in range(n)]
mols = {
    # name: (nsite, edges)
    "CBD (square)": (4, ring(4)),
    "TMM": (4, [(0, 1), (0, 2), (0, 3)]),
    "TME": (6, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)]),
    "MX (m-xylylene)": (8, ring(6) + [(0, 6), (2, 7)]),
    "TriMB": (9, ring(6) + [(0, 6), (2, 7), (4, 8)]),
    "TetraMB (1,2,4,5)": (10, ring(6) + [(0, 6), (1, 7), (3, 8), (4, 9)]),
    "p-xylylene (Kekule)": (8, ring(6) + [(0, 6), (3, 7)]),
}

def bipartition(n, edges):
    col = {0: 0}; stack = [0]; adj = {i: [] for i in range(n)}
    for i, j in edges: adj[i].append(j); adj[j].append(i)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in col: col[v] = 1 - col[u]; stack.append(v)
            elif col[v] == col[u]: return None
    return col

def max_matching(n, edges):
    best = 0
    for r in range(n // 2, 0, -1):
        for sub in itertools.combinations(edges, r):
            vs = [v for e in sub for v in e]
            if len(vs) == len(set(vs)): return r
    return best

# ------------------------------------------------------------------ T8
print("T8 Hückel (beta = -1 units: A = adjacency, E = alpha + x beta)")
for name, (n, edges) in mols.items():
    A = np.zeros((n, n))
    for i, j in edges: A[i, j] = A[j, i] = 1
    x, C = np.linalg.eigh(A)
    nz = np.sum(np.abs(x) < 1e-9)
    col = bipartition(n, edges)
    nA = sum(1 for v in col.values() if v == 0); nB = n - nA
    T = max_matching(n, edges)
    pairing = np.allclose(np.sort(x), np.sort(-x))
    Z = C[:, np.abs(x) < 1e-9]
    zero_sum = np.allclose(A @ Z, 0) if nz else True          # sum of neighbour coefficients = 0
    disj = ""
    if nz == 2:
        th = np.linspace(0, np.pi, 20001)
        a = np.outer(Z[:, 0], np.cos(th)) + np.outer(Z[:, 1], np.sin(th))
        b = -np.outer(Z[:, 0], np.sin(th)) + np.outer(Z[:, 1], np.cos(th))
        onsite = np.sum(a**2 * b**2, axis=0)
        disj = f" min_theta sum a^2 b^2 = {onsite.min():.2e} -> {'DISJOINT' if onsite.min() < 1e-6 else 'non-disjoint'}"
    lh = (nz >= n - 2 * T) and (n - 2 * T >= abs(nA - nB))   # Longuet-Higgins: lower bound
    print(f"  {name:22s} N={n} nA/nB={nA}/{nB} #NBMO={nz} N-2T={n-2*T} |nA-nB|={abs(nA-nB)} "
          f"pairing={pairing} zero-sum={zero_sum}{disj}")
    ok &= pairing and zero_sum and lh
expect_disjoint = {"CBD (square)": True, "TME": True, "TMM": False, "MX (m-xylylene)": False}

# ------------------------------------------------------------------ T9
print("T9 Hubbard ED (t=1, U=3): ground-state S vs Ovchinnikov S=|nA-nB|/2")
U9 = 3.0
for name, (n, edges) in mols.items():
    col = bipartition(n, edges); nA = sum(1 for v in col.values() if v == 0); nB = n - nA
    S_ov = abs(nA - nB) / 2
    # lowest energy in each Sz sector (N = n electrons, half filling)
    Emin = {}
    for nup in range((n + 1) // 2, n + 1):
        ndn = n - nup
        H, _, _ = hubbard_ham(edges, n, nup, ndn, U=U9)
        Emin[(nup - ndn) / 2] = ground(H)[0][0]
    E0 = min(Emin.values())
    S_gs = max(sz for sz, e in Emin.items() if abs(e - E0) < 1e-8)
    gap = Emin[S_gs + 1] - E0 if (S_gs + 1) in Emin else float("nan")
    print(f"  {name:22s} S_gs={S_gs} S_Ovch={S_ov} gap to S+1 = {gap:.4f} t  match={S_gs == S_ov}")
    ok &= S_gs == S_ov

# spin density alternation (Scheme 1): pentadienyl radical, open chain of 5 sites, 5 electrons, Sz=1/2
n, edges = 5, [(i, i + 1) for i in range(4)]
H, ups, dns = hubbard_ham(edges, n, 3, 2, U=U9)
w, v = ground(H); psi = v[:, 0]
nU, nD = len(ups), len(dns)
prob = (psi.reshape(nU, nD)) ** 2
rho_s = [sum(prob[a, b] * (((ups[a] >> i) & 1) - ((dns[b] >> i) & 1)) for a in range(nU) for b in range(nD))
         for i in range(n)]
alt = all(np.sign(rho_s[i]) == (1 if i % 2 == 0 else -1) for i in range(n))
# Hückel NBMO (U=0) has exactly zero spin density on even (unstarred) sites:
H0, _, _ = hubbard_ham(edges, n, 3, 2, U=0.0); w0, v0 = ground(H0); p0 = v0[:, 0].reshape(nU, nD) ** 2
rho0 = [sum(p0[a, b] * (((ups[a] >> i) & 1) - ((dns[b] >> i) & 1)) for a in range(nU) for b in range(nD))
        for i in range(n)]
print(f"  pentadienyl spin densities U=0: {np.round(rho0, 4)}; U=3t: {np.round(rho_s, 4)}; "
      f"sum={sum(rho_s):.4f}; alternating {alt}")
ok &= alt and np.allclose(np.array(rho0)[[1, 3]], 0, atol=1e-10)

# ------------------------------------------------------------------ T14
def uhf_dimer(U, t=1.0, m0=0.9, iters=5000):
    """Broken-symmetry UHF for the half-filled Hubbard dimer; returns E, <S^2>."""
    na = np.array([0.5 + m0 / 2, 0.5 - m0 / 2]); nb = na[::-1].copy()
    for _ in range(iters):
        Fa = np.array([[U * nb[0], -t], [-t, U * nb[1]]]); Fb = np.array([[U * na[0], -t], [-t, U * na[1]]])
        ea, Ca = np.linalg.eigh(Fa); eb, Cb = np.linalg.eigh(Fb)
        na_new, nb_new = Ca[:, 0] ** 2, Cb[:, 0] ** 2
        if np.allclose(na_new, na, atol=1e-14) and np.allclose(nb_new, nb, atol=1e-14): break
        na, nb = 0.5 * na + 0.5 * na_new, 0.5 * nb + 0.5 * nb_new
    E = ea[0] + eb[0] - U * np.dot(na, nb)
    ovl = Ca[:, 0] @ Cb[:, 0]
    S2 = 0 + 0 + 1 - ovl**2           # Sz^2 + Sz + N_beta - sum |<a|b>|^2  with Sz=0, N_beta=1
    return E, S2
print("T14 Yamaguchi projection, H = -2J S1.S2 convention, J_exact = (E_S - E_T)/2")
for Uv in (3.0, 6.0, 12.0, 24.0):
    E_BS, S2_BS = uhf_dimer(Uv)
    E_HS, S2_HS = 0.0, 2.0                      # triplet is exact in UHF (single determinant)
    J_Y = (E_BS - E_HS) / (S2_HS - S2_BS)
    J_noproj = (E_BS - E_HS) / 1.0              # "no projection" (Noodleman-like strong-overlap limit) variant
    J_ex = ((Uv - np.sqrt(Uv**2 + 16)) / 2 - 0.0) / 2
    print(f"  U/t={Uv:5.1f}: E_BS={E_BS:.5f} <S2>_BS={S2_BS:.4f} J_Yam={J_Y:.5f} J_exact={J_ex:.5f} "
          f"rel.err={(J_Y - J_ex) / J_ex:+.3f}")
    if Uv >= 12: ok &= abs((J_Y - J_ex) / J_ex) < 0.15
print("T6-T9,T14 PASS" if ok else "T6-T9,T14 FAIL")
