"""T9b: disjoint diradicals (CBD, TME): singlet-triplet gap vanishes at first order in U and grows as U^2
      (spin polarisation is a second-order/correlation effect); non-disjoint TMM, MX: gap linear in U. (D9, D10)
T15: same-spin vs opposite-spin correlation (Krylov's statement quoted in the review). (D5)
"""
import importlib.util, sys, pathlib
import numpy as np
from pyscf import gto, scf, mp

here = pathlib.Path(__file__).parent
ok = True

# --- reuse the Hubbard ED engine (copied into a small library module to avoid re-running t06 tests)
src = (here / "t06_t09_models.py").read_text()
lib = src.split("# ------------------------------------------------------------------ helpers: fermionic ED")[1] \
         .split("# ------------------------------------------------------------------ T7")[0]
ns = {}
exec("import itertools\nimport numpy as np\nimport scipy.sparse as sps\nfrom scipy.sparse.linalg import eigsh\n" + lib, ns)
hubbard_ham, ground = ns["hubbard_ham"], ns["ground"]

def ring(n): return [(i, (i + 1) % n) for i in range(n)]
graphs = {
    "CBD": (4, ring(4), True), "TME": (6, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)], True),
    "TMM": (4, [(0, 1), (0, 2), (0, 3)], False), "MX": (8, ring(6) + [(0, 6), (2, 7)], False),
}
print("T9b: E(S=1) - E(S=0) at half filling vs U (t=1); fitted exponent p in gap ~ U^p for small U")
for name, (n, edges, disjoint) in graphs.items():
    Us = np.array([0.05, 0.1, 0.2])
    gaps = []
    for U in Us:
        # lowest singlet = lowest Sz=0 level that is NOT also an Sz=1 level (those belong to S>=1 multiplets)
        H0 = hubbard_ham(edges, n, n // 2, n - n // 2, U=U)[0].toarray()
        H1 = hubbard_ham(edges, n, n // 2 + 1, n - n // 2 - 1, U=U)[0].toarray()
        e0 = np.linalg.eigvalsh(H0); e1 = np.linalg.eigvalsh(H1)
        E_trip = e1[0]
        E_sing = next(e for e in e0 if np.min(np.abs(e1 - e)) > 1e-9)
        gaps.append(E_trip - E_sing)      # >0: singlet lower ; <0: triplet lower
    gaps = np.array(gaps)
    p = np.polyfit(np.log(Us), np.log(np.abs(gaps)), 1)[0]
    print(f"  {name}: gaps {np.round(gaps, 6)} -> exponent {p:.2f}; sign {'singlet' if gaps[0] > 0 else 'triplet'} lower;"
          f" disjoint={disjoint}")
    ok &= (abs(p - 2) < 0.15) if disjoint else (abs(p - 1) < 0.15)
    ok &= (gaps[0] > 0) if disjoint else (gaps[0] < 0)

# --- T15a: MP2 same-spin vs opposite-spin correlation, per pair
print("T15a: MP2/cc-pVTZ (frozen core) correlation split")
mols = {"H2O": "O 0 0 0; H 0 0.757 0.587; H 0 -0.757 0.587",
        "N2": "N 0 0 0; N 0 0 1.098",
        "C2H4": "C 0 0 0.667; C 0 0 -0.667; H 0 0.923 1.238; H 0 -0.923 1.238; H 0 0.923 -1.238; H 0 -0.923 -1.238"}
for name, atom in mols.items():
    m = gto.M(atom=atom, basis="cc-pvtz", verbose=0)
    mf = scf.RHF(m).run()
    pt = mp.MP2(mf).set_frozen().run()
    nocc = pt.nocc
    n_ss_pairs = 2 * nocc * (nocc - 1) / 2         # alpha-alpha + beta-beta pairs
    n_os_pairs = nocc * nocc
    r_total = pt.e_corr_ss / pt.e_corr_os
    r_pair = (pt.e_corr_ss / n_ss_pairs) / (pt.e_corr_os / n_os_pairs)
    print(f"  {name}: E_ss={pt.e_corr_ss:.5f} E_os={pt.e_corr_os:.5f} ratio={r_total:.3f}; per-pair ratio={r_pair:.3f}")
    ok &= r_total < 0.5

# --- T15b: He: correlation of a same-spin pair (2^3S) vs opposite-spin pair (1^1S)
def he_basis():
    s = [0.02 * 2.2 ** k for k in range(16)]
    p = [0.04 * 2.6 ** k for k in range(7)]
    d = [0.08 * 3.0 ** k for k in range(4)]
    return {"He": [[0, [e, 1.0]] for e in s] + [[1, [e, 1.0]] for e in p] + [[2, [e, 1.0]] for e in d]}
he = gto.M(atom="He 0 0 0", basis=he_basis(), verbose=0)
e_hf_1S = scf.RHF(he).run().e_tot
mf3 = scf.ROHF(gto.M(atom="He 0 0 0", basis=he_basis(), spin=2, verbose=0)).run()
exact_1S, exact_3S = -2.903724377034, -2.1752293782367    # Pekeris/Drake benchmarks
r = (exact_3S - mf3.e_tot) / (exact_1S - e_hf_1S)
print(f"T15b: He 1^1S: HF={e_hf_1S:.6f} Ecorr={exact_1S - e_hf_1S:.5f}; 2^3S: ROHF={mf3.e_tot:.6f} "
      f"Ecorr={exact_3S - mf3.e_tot:.5f}; same-spin/opposite-spin pair ratio={r:.3f}")
ok &= 0 < r < 0.1
print("T9b,T15 PASS" if ok else "T9b,T15 FAIL")
