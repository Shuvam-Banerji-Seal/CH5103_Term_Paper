# Presentation

A beamer deck on Gryn'ova, Coote & Corminboeuf, *WIREs Comput. Mol. Sci.* **2015**, 5, 440:
134 frames (593 pages with overlays), in 19 parts. It runs from the molecular Hamiltonian to the
review's sign error, then through our verification and a claim-by-claim verdict.

**Output:** [`ch5103-presentation.pdf`](ch5103-presentation.pdf)

## Layout

```
presentation/
├── main.tex                 preamble + \input of every section, in order
├── latexmkrc                LuaLaTeX, out-of-tree build/, theme/ on TEXINPUTS
├── Makefile                 make / make assets / make check
├── theme/
│   ├── beamerthemeNoir.sty  black theme: calligraphic titles, Libertinus, progress-bar footline
│   └── noir-macros.sty      notation, overlay helpers (\hl, \canc, ...), boxes, pgfplots style
├── sections/                one file per part (00-title ... 19-verdict)
├── figures/
│   ├── screenshots/         rendered from the review PDF (incl. the highlighted sign error)
│   ├── diagrams/            vector PDFs built from diagrams-src/
│   └── diagrams-svg/        intermediate SVGs
├── diagrams-src/            JavaScript generators (node) -> SVG -> PDF (rsvg-convert)
├── data/                    CSV data plotted with pgfplots
└── scripts/                 make_screenshots.py, make_data.py, check_log.py
```

The review's own figures are read from `../assets/figures/` through `\graphicspath`.

## Building

```bash
make            # latexmk (LuaLaTeX) -> ch5103-presentation.pdf, then the log check
make assets     # optional: regenerate screenshots, plot data (PySCF) and JS diagrams
```

You need TeX Live with LuaLaTeX, `minted` (with `latexminted`), and the fonts Libertinus, EB Garamond,
TeX Gyre Chorus and JetBrains Mono. `make assets` also needs `uv`, `node` and `rsvg-convert`.

`make check` lists every warning, bad box and missing glyph in `build/main.log`. The deck builds
with none (`CLEAN`).

## Design

- **Theme:** a pure-black canvas with off-white text and gold / cyan / rose / green accents. Frame and
  part titles are calligraphic (TeX Gyre Chorus); body text and maths are Libertinus; labels use EB
  Garamond small caps.
- **Progress bar:** the footline is a loading-style bar driven by *page / total pages*, so it
  advances on every overlay step. It has a glowing head, plus the section name and frame counter.
- **Animated derivations:** each step is revealed with `\uncover`, one cell at a time inside
  `align*`. Cancellations are struck through as they happen (`\canc<n>`), and highlighted terms
  change colour on cue (`\hl<n>`).
- **Colour-coded boxes:** claims from the paper (gold), assumptions (violet), results (green),
  verification (cyan), errata (rose).

## Content sources

- The derivations follow [`../derivations/`](../derivations).
- The numbers come from [`../verification/`](../verification) and from `scripts/make_data.py`.
- The DFT results come from `../verification/logs/t11*.log`.
- The NBMO diagrams are computed in JavaScript: Hückel matrix, Jacobi diagonalisation, then a
  rotation that minimises Σ a²b². They reproduce the Python values: 1/6 for TMM, 1/16 for
  m-xylylene, and 0 for CBD and TME.
