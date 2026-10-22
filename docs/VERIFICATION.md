# Verification suite

Every result in [`derivations/`](../derivations) is checked by a script in [`verification/`](../verification)
or by a Lean proof in [`verification/lean_proofs/`](../verification/lean_proofs).

## Running

```bash
make sync         # uv sync --project .   (Python 3.12, pinned in uv.lock)
make verify       # fast suite, ~3 min on 2 threads
make verify-dft   # T11/T11c: DFT geometry optimisations, ~1-2 h
make lean         # Lean 4.29.1 + Mathlib v4.29.1 (downloads the Mathlib cache, ~5 GB)
```

Each Python test prints a final `PASS`/`FAIL` line. Run a single test with
`OMP_NUM_THREADS=$(nproc) uv run --project . python -I verification/<script>.py`.

**Environment notes**
- `--project .` overrides a global `UV_PROJECT` if one is set.
- `python -I` (isolated mode) ignores a global `PYTHONPATH` that may point at another Python's
  site-packages.

## Test matrix

| ID | Script | What it checks | Derivation § | Status |
|---|---|---|---|---|
| T1 | `t01_spin_and_determinants.py` | S², S_z eigenfunctions; Fig. 1 combinations; sign erratum | 1, 2 | PASS |
| T2 | `t02_two_orbital_hamiltonian.py` | 2e/2o singlet matrix + E_T vs full CI (5 random integral sets, max dev 2×10⁻¹⁴); Koopmans/UHF relations | 3, 10, 11 | PASS |
| T3 | `t03_t05_hund_virial_h2.py` | K_pq ≥ 0, J_pq ≥ K_pq for water MOs | 4 | PASS |
| T4 | ″ | He 2³S/2¹S, exact 2-electron in a 16s7p4d basis, virial scaling, less screening | 5 | PASS |
| T5 | ″ | H₂ minimal basis: RHF/CI/triplet/OSS closed forms vs PySCF, R → ∞ limits | 6 | PASS |
| T6 | `t06_t09_models.py` | two-orbital gap model (symbolic) | 6 | PASS |
| T7 | ″ | extended Hubbard dimer: kinetic exchange −4t²/(U−V) | 7 | PASS |
| T8 | ″ | Hückel: zero-sum rule, pairing theorem, NBMO count ≥ N−2T, disjointness | 8 | PASS |
| T9 | ″ | Hubbard exact diagonalisation: S_gs = ½\|n_A−n_B\| for 7 graphs; spin alternation | 9 | PASS |
| T9b | `t09b_t15_correlation.py` | S–T gap ∝ U (non-disjoint) vs ∝ U² (disjoint) | 8, 9 | PASS |
| T10 | `t10_t12_t13_symbolic.py` | S–T gap = HOMO-energy difference | 10 | PASS |
| T11a | `t11_rohf_and_distonic.py` | ROHF stationarity blocks; canonicalisation dependence | 12 | PASS |
| T11b | ″ | distonic radical anion ΔSCF, pH switch (B3LYP) | 11 | FAIL: no crossover (+0.06 eV); diagnosed by T11c |
| T11c | `t11c_distonic_functionals.py` | functional (B3LYP/CAM-B3LYP) and separation dependence | 11 | PASS at CAM-B3LYP (anions −0.36 / −0.30 eV, acids +1.42 / +1.23 eV); all 8 runs done |
| T12 | `t10_t12_t13_symbolic.py` | 3d/4s algebra | 13 | PASS |
| T13 | ″ | [l₁, 1/r₁₂] ≠ 0, [L, 1/r₁₂] = 0 | 14 | PASS |
| T14 | `t06_t09_models.py` | Yamaguchi projection on BS-UHF Hubbard dimer | 16 | PASS |
| T15 | `t09b_t15_correlation.py` | same-spin vs opposite-spin correlation (MP2, He) | 5 | PASS |
| T17 | `lean_proofs/Ch5103/Identities.lean` | 17 theorems, standard axioms only (`propext`, `Classical.choice`, `Quot.sound`) | several | PASS |

## Failures found during development

These are recorded in `plans/tests.md`. Each was diagnosed before the test was changed.
- **T5:** symmetry tolerance 10⁻¹⁰ on (11|12) at R = 20 bohr. The value was −8×10⁻⁹, round-off from an
  overlap of ~10⁻¹⁶; the tolerance was loosened to 10⁻⁶.
- **T8:** NBMO count = N − 2T was assumed. Cyclobutadiene violates it: N − 2T is only a lower bound.
- **T9b:** the lowest S_z = 0 level was taken to be a singlet. For triplet ground states it is the
  triplet's M_S = 0 component; the test now identifies the true lowest singlet.
- **T11a:** a SOMO/HOMO flip was assumed within the standard canonicalisation schemes. It only occurs
  for weights outside [0, 1]; the test now measures the crossing weight A*.
- **T12:** the illustrative parameters gave Δ < 0; they were replaced and the expected sign is now asserted.
