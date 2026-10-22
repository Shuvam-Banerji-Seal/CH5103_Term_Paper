# CH5103 Term Paper: Uncommon Molecular Electronic Configurations

Supporting material for a term paper on

> G. Gryn'ova, M. L. Coote, C. Corminboeuf, **"Theory and practice of uncommon molecular electronic
> configurations"**, *WIREs Comput. Mol. Sci.* **2015**, 5, 440–459.
> [doi:10.1002/wcms.1233](https://doi.org/10.1002/wcms.1233)

The review covers diradicals with fluctuating ground-state multiplicity (triplet vs open-shell singlet)
and "quasi-closed-shell" radicals whose SOMO lies *below* a doubly occupied orbital (non-aufbau
ordering). This repository contains:

- **step-by-step derivations** of all the mathematics behind the review (and its cited theory);
- **numerical and symbolic checks** of every derived result (PySCF, SymPy, exact diagonalisation);
- **machine-checked Lean 4 / Mathlib proofs** of the algebraic identities;
- the review's **figures and formulae as reusable assets**.

**Verdict:** see [`docs/FINDINGS.md`](docs/FINDINGS.md). In short, the theory is sound wherever it
could be tested. One sign error and one citation error were found, plus some overstated claims. The
distonic-radical pH switch is reproduced with CAM-B3LYP but not with B3LYP.

## Contents

| Path | What |
|---|---|
| [`paper/`](paper) | The review (open access, CC BY-NC-ND; redistributed unmodified) |
| [`derivations/`](derivations) | LaTeX derivations: 18 sections ([`derivations.pdf`](derivations/derivations.pdf)) |
| [`assets/figures/`](assets/figures) | All 17 figures + 5 schemes at 300 dpi |
| [`assets/figures.jsonl`](assets/figures.jsonl) | Figure/scheme number → file, page, verbatim caption |
| [`assets/formulae.tex`](assets/formulae.tex) | Key formulae, ready to paste ([PDF](assets/formulae.pdf)) |
| [`verification/`](verification) | Test scripts (T1–T15), DFT logs, [`lean_proofs/`](verification/lean_proofs) (T17) |
| [`scripts/extract_figures.py`](scripts/extract_figures.py) | Regenerates `assets/` from the PDF (byte-identical) |
| [`docs/FINDINGS.md`](docs/FINDINGS.md) | Claim-by-claim assessment of the review |
| [`docs/VERIFICATION.md`](docs/VERIFICATION.md) | Test matrix and how to run it |
| [`plans/`](plans) | Working log: plan, decisions, doubts and their resolutions, full test log |

### Derivations at a glance

| § | Topic | Key result |
|---|---|---|
| 1–2 | Antisymmetry, two-electron wavefunctions | OSS = ½(D_iv − D_iii); the review prints "+" (an error) |
| 3–4 | 2e/2o Hamiltonian, Fermi holes | E_OSS − E_T = 2K; K ≥ 0 and J ≥ K proved |
| 5 | Hund's rule | Virial theorem ⇒ the frozen-orbital (Slater) mechanism is impossible; less screening confirmed (He, C) |
| 6–7 | Static correlation, kinetic exchange | H₂ RHF error → U/2; J ≈ k − 2t²/(U−V) |
| 8–9 | NBMOs, spin polarisation | Disjoint ⇒ K = 0 (ZDO); Ovchinnikov = Lieb's theorem; gap ∝ U² for disjoint |
| 10–11 | Koopmans/Janak, quasi-closed shell | E_S − E_T = Δε_HOMO; UHF α/β splitting; redox fingerprint |
| 12 | ROHF canonicalisation | Diagonal blocks arbitrary ⇒ orbital order is a convention |
| 13–15 | 3d/4s, quantum numbers, adiabatic theorem | Δ = (ε_d − ε_s) + (J̄_dd − J̄_ds); [l₁, 1/r₁₂] ≠ 0 |
| 16 | Broken symmetry | Yamaguchi projection derived and tested |

## Quick start

Requires [uv](https://docs.astral.sh/uv/), a TeX distribution with `latexmk`, and (for the proofs)
[elan](https://github.com/leanprover/elan).

```bash
make sync          # Python 3.12 environment from uv.lock
make verify        # fast verification suite (prints PASS/FAIL per test)
make derivations   # build derivations/derivations.pdf
make figures       # re-extract figures + captions from the PDF
make lean          # Lean 4 proofs (fetches the Mathlib cache)
```

Notes:
- All `uv` calls use `--project .`, so a global `UV_PROJECT` does not interfere.
- Scripts run with `python -I` to ignore any global `PYTHONPATH`.
- `make` uses all cores (`THREADS=$(nproc)`).

## Sources

The derivations quote the review and, where accessible, the original works it cites. Paywalled
originals are marked as such, and nothing beyond what the review states is attributed to them. See §17
of the derivations for the full access table.

## License

The review PDF is © 2015 The Authors, published by John Wiley & Sons under CC BY-NC-ND; it is included
unmodified for non-commercial use. No license has yet been chosen for the original material
(derivations, scripts, proofs) in this repository.
