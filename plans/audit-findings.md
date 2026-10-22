# Slide audit against the paper (cycle 2)

Five read-only Haiku sub-agents each audited one block of slide sections against the paper text
(pdftotext of the PDF). Every finding was re-checked by hand before acting. All five independently
re-derived the sign error on p. 441 and confirmed it. No mathematical error was found in the slides.

The sign error was also re-confirmed by a new method (T1b, `verification/t01b_sign_error_numeric.py`).
The paper's two determinants were transcribed as printed and S² was applied as an operator to the
numerical two-electron tensors: ½(|iii|+|iv|) has S² = 2 (triplet). The paper's own product form has
S² = 0 and equals ½(|iv|−|iii|).

## Findings acted on (slide changes)
| # | where | finding | disposition |
|---|---|---|---|
| 1 | 13 Fig 7(b) | slide said triplet → singlet; in Fig 7(b) trans has antiparallel (singlet) and cis has parallel (triplet) spins | **slide error, fixed**: singlet (trans) → triplet (cis) |
| 2 | 12 TriMB | paper p.444 calls MX *and* TriMB "triplet ground states"; TriMB has 3 unpaired electrons, rule and ED give S = 3/2 | noted on slide + FINDINGS as an imprecision **in the paper** |
| 3 | 19, FINDINGS | "obsolete" is not the paper's word; it says "the obsolescence of qualitative rules" | quote corrected |
| 4 | 03 Box 1 | paper body says "direct observation of copper's d-orbitals" (p.448) | wording + page fixed |
| 5 | 03 Box 1 | paper says canonicalisation changes non-aufbau *occupations/orderings* | wording fixed |
| 6 | 02, 16 | paper says redox products are *polyradicals* | "polyradical (diradical in the simplest case)" |
| 7 | 04 | "No two electrons with the same four quantum numbers" was in quote marks but is a paraphrase | quote marks removed; Pauli's wording cited p.448 |
| 8 | 05 | "triplet: one determinant" — only M_S = ±1 are single determinants | refined |
| 9 | 05 | merged M_S = ±1 quote | quote the M_S = +1 line, "−1 analogous" outside quotes |
| 10 | 06 | Hund statement is the review's own wording (citing IUPAC), not Hund 1925 | attribution fixed |
| 11 | 07 | Coulomb hole needs correlation beyond one determinant (dynamic), not "configuration mixing" | wording fixed |
| 12 | 07 | Fermi hole: P_T(r,r)=0 holds for the whole triplet (all M_S) | wording fixed |
| 13 | 08 | "solved exactly" — 16s7p4d basis, within 1e-4 Eh | title fixed |
| 14 | 08 | Slater panel: frozen-orbital reading is ours; virial theorem + sign of ΔV_ee decide | wording fixed |
| 15 | 06 | σg/σu are not NBMOs | example list fixed |
| 16 | 10 | "no ionic character" in quote marks; "paper's two pictures" | quotes dropped, wording fixed |
| 17 | 12 | Ovchinnikov rule "is expected to" (p.443); Kollmar–Staemmler attribution | wording fixed |
| 18 | 12 | Fig 4: p,p' parallel; m,m' and m,p' antiparallel | added |
| 19 | 13 | Fig 7(e) slip: "needs nondisjoint" overstated | softened |
| 20 | 14 | review says only "lacks dynamic electron correlation"; ref. 20 is its source | wording + ref fixed |
| 21 | 15 | [H, L] = 0 only for an atom (central field) | qualified |
| 22 | 15 | "non-aufbau orderings are real" vs our ROHF point | "non-aufbau occupations observed via observables" |
| 23 | 15 | "4s above 3d" is "in neutral atoms"; "almost all atoms" unsourced; J_dd ≫ J_ds is a heuristic | qualified |
| 24 | 16 | TTFCOO⁻NH₄⁺ is "according to … calculations on the model tetramer"; Fig 16 diradical result is computational | qualified |
| 25 | 18 | T11b miss is 0.06–0.07 eV; T11c *shows* functional dependence; T11c PASS was manual | wording fixed; `t11c_check.py` added to print PASS/FAIL from the logs |
| 26 | 18 | T16 (citation checks) has no script | footnote |
| 27 | 19 | "settles Hund's rule", "theorems of models", "chemistry stands" overreach | narrowed |
| 28 | 01 | "every step was checked" | "every identity used was checked" |
| 29 | 18 | "test-first" claim not documented | dropped |

## Findings checked and not acted on
- Hongo et al. quote (08): flagged "unverified" by the auditor, but it was verified verbatim against the
  arXiv full text in cycle 1 (plans/research.md). Kept; the slide now says "full text".
- Joke slide (05): clearly marked as a joke; kept, as requested by the user.
