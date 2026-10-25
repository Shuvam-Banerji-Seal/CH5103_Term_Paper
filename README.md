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

**Website:** <https://shuvam-banerji-seal.github.io/CH5103_Term_Paper/> has an overview, the findings, the test
matrix, the figure gallery and an [in-browser slide viewer](https://shuvam-banerji-seal.github.io/CH5103_Term_Paper/slides.html).

**Video:** a complete narrated explainer (1080p, about three and a half hours, with captions) is attached to the
[latest release](https://github.com/Shuvam-Banerji-Seal/CH5103_Term_Paper/releases/latest): every slide frame
animated and every derivation step spoken, plus appendices that walk through every verification script and every
Lean proof line by line. How it was made: [`video/README.md`](video/README.md).

**Verdict:** see [`docs/FINDINGS.md`](docs/FINDINGS.md). In short, the theory is sound wherever it
could be tested. One sign error (confirmed three independent ways) and one citation error were found,
plus some overstated or imprecise claims. The distonic-radical pH switch is reproduced with CAM-B3LYP
(both test systems) but not with B3LYP.

## Contents

| Path | What |
|---|---|
| [`paper/`](paper) | The review (open access, CC BY-NC-ND; redistributed unmodified) |
| [`derivations/`](derivations) | LaTeX derivations: 18 sections ([`derivations.pdf`](derivations/derivations.pdf)) |
| [`presentation/`](presentation) | Beamer deck, 134 numbered frames, every step explained ([with builds](presentation/ch5103-presentation.pdf), [handout](presentation/ch5103-handout.pdf)) |
| [`assets/figures/`](assets/figures) | All 17 figures + 5 schemes at 300 dpi |
| [`assets/figures.jsonl`](assets/figures.jsonl) | Figure/scheme number → file, page, verbatim caption |
| [`assets/formulae.tex`](assets/formulae.tex) | Key formulae, ready to paste ([PDF](assets/formulae.pdf)) |
| [`verification/`](verification) | Test scripts (T1–T15, T1b, `t11c_check.py`), [`results/`](verification/results) of the last run, DFT logs, [`lean_proofs/`](verification/lean_proofs) (T17) |
| [`scripts/extract_figures.py`](scripts/extract_figures.py) | Regenerates `assets/` from the PDF (byte-identical) |
| [`docs/FINDINGS.md`](docs/FINDINGS.md) | Claim-by-claim assessment of the review |
| [`docs/VERIFICATION.md`](docs/VERIFICATION.md) | Test matrix and how to run it |
| [`plans/`](plans) | Working log: plan, decisions, doubts and their resolutions, full test log, slide audit |
| [`video/`](video) | The explainer video: ManimGX scenes, Breeze-TTS-2 narration on the CPU, a JavaScript editor ([how it was made](video/README.md)) |
| [`site/`](site) | The GitHub Pages site, assembled by [`scripts/build_site.sh`](scripts/build_site.sh) |
| [`.github/workflows/pages.yml`](.github/workflows/pages.yml) | On every push to `main`: runs the verification suite, rebuilds every PDF in TeX Live, assembles the site and deploys it (only if all tests pass) |

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
make verify        # fast verification suite (PASS/FAIL per test; output saved in verification/results/)
make derivations   # build derivations/derivations.pdf
make figures       # re-extract figures + captions from the PDF
make lean          # Lean 4 proofs (fetches the Mathlib cache)
make -C presentation pdf handout   # beamer deck (LuaLaTeX), with builds and as a handout
scripts/build_site.sh  # assemble the website into _site/ (open _site/index.html via any static server)
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
