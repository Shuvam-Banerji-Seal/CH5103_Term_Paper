"""T2: analytic 2-electron/2-orbital energies (D3, D11, D12, D13) vs brute-force diagonalisation.

Random real symmetric one-electron integrals h_pq and two-electron integrals (pq|rs) with full
8-fold permutational symmetry (chemists' notation) are generated; the exact Hamiltonian in the
basis of all 2-electron determinants is built with PySCF's FCI machinery and compared with the
closed-form matrix elements derived in the LaTeX document.
"""
import numpy as np
from pyscf import fci, ao2mo

rng = np.random.default_rng(7)
ok = True

def random_integrals(n):
    h = rng.normal(size=(n, n)); h = (h + h.T) / 2
    # positive-semidefinite-ish ERI built from random "orbital products" to mimic Coulomb kernel
    L = rng.normal(size=(n * (n + 1) // 2, 6))
    eri_packed = L @ L.T                       # (pq|rs) as PSD matrix over pair index -> K >= 0
    eri = ao2mo.restore(1, eri_packed, n)
    return h, eri

for trial in range(5):
    h, g = random_integrals(2)
    a, b = 0, 1
    ha, hb, hab = h[a, a], h[b, b], h[a, b]
    Jaa, Jbb, Jab, Kab = g[a, a, a, a], g[b, b, b, b], g[a, a, b, b], g[a, b, a, b]
    Laab, Lbba = g[a, a, a, b], g[b, b, b, a]      # (aa|ab), (bb|ba)

    # --- analytic (derived) results
    E_T = ha + hb + Jab - Kab
    H_singlet = np.array([
        [2 * ha + Jaa, Kab, np.sqrt(2) * (hab + Laab)],
        [Kab, 2 * hb + Jbb, np.sqrt(2) * (hab + Lbba)],
        [np.sqrt(2) * (hab + Laab), np.sqrt(2) * (hab + Lbba), ha + hb + Jab + Kab],
    ])                                               # basis |aa-bar|, |bb-bar|, OSS
    ES_analytic = np.linalg.eigvalsh(H_singlet)

    # --- brute force: FCI for 2 electrons in 2 orbitals, singlets and triplets separately
    solver = fci.direct_spin1.FCI()
    e_s, _ = solver.kernel(h, g, 2, (1, 1), nroots=4)
    # classify roots by <S^2>
    e_all, cs = solver.kernel(h, g, 2, (1, 1), nroots=4)
    singlets, triplets = [], []
    for e, c in zip(e_all, cs):
        s2, _ = fci.spin_op.spin_square0(c, 2, (1, 1))
        (singlets if s2 < 1 else triplets).append(e)
    e_trip_ms1 = fci.direct_spin1.FCI().kernel(h, g, 2, (2, 0))[0]
    c1 = np.allclose(sorted(singlets), ES_analytic)
    c2 = np.allclose(triplets, [E_T]) and np.isclose(e_trip_ms1, E_T)
    # Singlet-triplet gap of the pure OSS configuration (diagonal elements): 2K
    c3 = np.isclose(H_singlet[2, 2] - E_T, 2 * Kab)
    c4 = Kab >= 0
    print(f"trial {trial}: singlet eigvals match {c1}, triplet match {c2}, "
          f"<OSS|H|OSS>-E_T=2K {c3}, K>=0 {c4}")
    ok &= c1 and c2 and c3 and c4

# --- frozen-orbital Koopmans relations used in D11/D12 (3 orbitals: c (core-ish), s (SOMO), h (HOMO))
# config s^1 h^2 (doublet).  UHF-like orbital energies from Slater-Condon:
#   eps_h(alpha) = h_h + J_hh + J_hs - K_hs ; eps_h(beta) = h_h + J_hh + J_hs
#   eps_s(alpha) = h_s + 2 J_hs - K_hs
# check them as  E(N) - E(N-1, frozen) for removing the given spin-orbital.
from itertools import combinations
def det_energy(occ, h, g):
    """Energy of a single determinant; occ = list of (spatial index, spin)."""
    E = sum(h[p, p] for p, _ in occ)
    for (p, sp_), (q, sq) in combinations(occ, 2):
        E += g[p, p, q, q] - (g[p, q, p, q] if sp_ == sq else 0.0)
    return E
for trial in range(3):
    h, g = random_integrals(2)
    s, hh = 0, 1
    N = [(s, 'a'), (hh, 'a'), (hh, 'b')]
    E0 = det_energy(N, h, g)
    eps_h_a = E0 - det_energy([(s, 'a'), (hh, 'b')], h, g)
    eps_h_b = E0 - det_energy([(s, 'a'), (hh, 'a')], h, g)
    eps_s_a = E0 - det_energy([(hh, 'a'), (hh, 'b')], h, g)
    Jhh, Jhs, Khs = g[hh, hh, hh, hh], g[hh, hh, s, s], g[hh, s, hh, s]
    c = (np.isclose(eps_h_a, h[hh, hh] + Jhh + Jhs - Khs)
         and np.isclose(eps_h_b, h[hh, hh] + Jhh + Jhs)
         and np.isclose(eps_s_a, h[s, s] + 2 * Jhs - Khs)
         and np.isclose(eps_h_b - eps_h_a, Khs))
    print(f"Koopmans/UHF orbital-energy relations trial {trial}: {c}")
    ok &= c
    # oxidation from h of s^1 h^2 -> s^1 h^1: triplet vs open-shell singlet split = 2 K_hs
    E_cat_T = det_energy([(s, 'a'), (hh, 'a')], h, g)
    E_cat_OSS_diag = h[s, s] + h[hh, hh] + Jhs + Khs
    c = np.isclose(E_cat_OSS_diag - E_cat_T, 2 * Khs)
    print(f"  cation OSS(diag) - T = 2K_hs: {c}")
    ok &= c
print("T2 PASS" if ok else "T2 FAIL")
