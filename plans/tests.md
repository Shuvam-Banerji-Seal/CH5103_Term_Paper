# Test log
| time | test | command | result | notes |
|---|---|---|---|---|
| c1 | T1 spin eigenfunctions, Fig.1 combos | python -I t01_spin_and_determinants.py | PASS | paper '+' combination = triplet (confirmed) |
| c1 | T2 2e/2o H vs FCI (5 random sets), Koopmans/UHF relations | t02_two_orbital_hamiltonian.py | PASS | |
| c1 | T3 K_pq>=0, J>=K water MOs | t03_t05_hund_virial_h2.py | PASS | |
| c1 | T4 He 2^3S/2^1S exact 2e in 57-fn basis + scaling | same | PASS | E err 1.7e-5/1.1e-4; virial 2.000000; dVee=+0.0185, dVne=-0.0772, dT=+0.0293 |
| c1 | T5 H2 STO-3G analytic vs PySCF R=1.4..20 | same | PASS (after fix) | first FAIL: symmetry tol 1e-10 on (11|12)=-8e-9 at R=20 (roundoff, S~1e-16); tol->1e-6 |
| c1 | T6 two-orbital CI vs Delta | t06_t09_models.py | PASS | |
| c1 | T7 ext. Hubbard dimer | same | PASS | |
| c1 | T8 Hückel NBMO rules | same | PASS (after fix) | first FAIL: CBD #NBMO=2 > N-2T=0 -> Longuet-Higgins is a lower bound |
| c1 | T9 Hubbard ED S_gs = Ovchinnikov/Lieb for 7 graphs; pentadienyl spin alternation | same | PASS | |
| c1 | T14 Yamaguchi projection on Hubbard dimer | same | PASS | rel err 7.7% (U=3t) -> 0.1% (U=12t) |
| c1 | T10 frozen-orbital S-T = eps difference | t10_t12_t13_symbolic.py | PASS | |
| c1 | T12 3d/4s algebra | same | PASS (after fix) | illustration numbers corrected (gave Delta<0) |
| c1 | T13 commutators | same | PASS | |
| c1 | T9b gap scaling vs U (disjoint U^2 singlet; nondisjoint U^1 triplet) | t09b_t15_correlation.py | PASS (after fix) | first FAIL: Sz=0 lowest level was triplet's M=0 component; fixed singlet identification |
| c1 | T15 SS/OS correlation | same | PASS | He ratio 0.023; MP2 per-pair 0.32–0.43 -> review claim system-dependent |
| c1 | T11a ROHF stationarity + canonicalisation | t11_rohf_and_distonic.py | stationarity PASS; flip assumption FAIL -> test revised | no flip for 0<=A<=1; A*≈1.04 (H2NO, NO2) |
| c1 | T11b distonic anion ΔSCF (UB3LYP/6-31+G*) | same | running | anion: alpha-SOMO below alpha-HOMO (orbital non-aufbau) BUT vertical CS singlet 3.946 < triplet 4.008 eV |
| c1 | T11b final | t11_rohf_and_distonic.py | FAIL (pH-switch crossover criterion) | acid: SOMO=HOMO, IE_T-IE_CS=+1.31 eV; anion: SOMO 3 below aHOMO, IE_T-IE_CS=+0.06 eV. Orbital inversion + 1.25 eV shift reproduced; no energetic crossover at UB3LYP for short linker. Kept as known-failing; diagnosis pending T11c |
| c1 | T17 Lean 4.29.1 / Mathlib v4.29.1: 17 theorems (Identities.lean) | lake build; #print axioms | PASS | build OK first try, 0 sorry; all 17 depend only on propext, Classical.choice, Quot.sound |
| c1 | T11c | t11c_distonic_functionals.py | NOT RUN | waiter job stopped by Claude Code (system critically low on memory: 1 GB free of 14 GB) before T11c started; no log produced. Not restarted per harness rule; awaiting user go-ahead |
