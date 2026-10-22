# Final verification report — derivations of Gryn'ova, Coote & Corminboeuf (2015)

## Scope
Step-by-step derivations of all mathematics in the review (derivations/, 18 sections), each tied to a
numerical, symbolic or formal check; consultation of the cited originals where accessible; a findings
document (docs/FINDINGS.md) and a presentation (presentation/).

## Numbers
- Cycles: 1 (with loop-backs inside the cycle for every failing test).
- Searches: 4 research sub-agents (Haiku) + own targeted searches (Lieb 1989, Katriel–Pauncz year,
  Hongo 2004 arXiv full text, Liu–Langenaeker).
- Tests: 19 entries (T1–T17 incl. T9b, T11a/b/c). 18 PASS; T11b known-failing and diagnosed by T11c.
- Test failures found and diagnosed during development: 5 (T5 tolerance, T8 equality→bound, T9b singlet
  identification, T11a expectation, T12 illustration numbers) + T11b (functional dependence).
- Lean: 17 theorems, `lake build` clean, `#print axioms` shows only propext / Classical.choice / Quot.sound.
- To-do: 22/22 resolved (1 sub-item blocked: Liu–Langenaeker paywalled).
- Doubts: 6 logged; 4 resolved, DB5 unresolved-and-flagged, DB6 resolved with a stated hypothesis.

## Findings about the review
1. Sign error p.441: OSS printed as ½(D_iii + D_iv) = M_S=0 triplet; correct ½(D_iv − D_iii). [T1, Lean]
2. Citation year: Katriel & Pauncz Adv. Quantum Chem. 10 is 1977, not 1975. [DB1]
3. Same-spin correlation "an order of magnitude" smaller: true for He (0.023), overstated for molecules
   (MP2 per-pair 0.3–0.4). [T15]
4. ROHF canonicalisation dependence: true in principle; for H2NO/NO2/CH3/allyl a flip needs A ≈ 1.04 > 1. [T11a]
5. Distonic radical anions → diradical on oxidation, pH-switchable: reproduced with CAM-B3LYP for both test
   systems (−0.36, −0.30 eV; acids +1.42, +1.23 eV); B3LYP misses by ~0.07 eV. [T11b, T11c]
6. Possible wording slip p.445 (Fig.7e "disjoint NBMOs" ⇒ triplet). [DB5, unverified]
7. Everything else tested (Hund/less screening, static correlation, kinetic exchange, disjointness,
   Ovchinnikov/Lieb, Koopmans/Janak gap, 3d/4s, quantum numbers, Yamaguchi) confirmed.

## Confidence
HIGH for the mathematics (every identity symbolically or formally checked; numerics reproduce closed forms
to 1e-14–1e-16). MEDIUM for literature attribution: most originals were paywalled, so only the review's
wording and verified abstracts are attributed to them. MEDIUM for the distonic conclusion: two functionals,
one basis, vertical energies only, gas phase.

## Known limitations
- Paywalled originals not read: Borden–Davidson, Kollmar–Staemmler, Gallup, Salem–Rowland, BKM 1987,
  Liu–Langenaeker, Yamanaka 2005, Glaesemann–Schmidt, Vanquickenborne, Melrose–Scerri, Scerri 1991,
  Ehrenfest 1917, Pauli 1925.
- Distonic test: no adiabatic energies, no solvent, no correlated wavefunction benchmark.
- Experimental claims about specific molecules (Figs 7–9, 11–17) were not re-checked.

## Cycle 2 (slide annotation, audit, website)
- **Sign error re-confirmed by a third, independent method** (T1b): Ŝ² applied as an operator to numerical
  two-electron tensors built from the printed determinants. The printed sum has ⟨S²⟩ = 2 (triplet).
- **Slide audit against the paper:** five Haiku auditors, 29 findings, each re-checked by hand. No mathematical
  error in the slides. One slide error fixed (Fig. 7(b) direction: light switches the trans singlet to the cis
  triplet). New imprecision found in the paper: TriMB is called a "triplet" (p. 444) but has S = 3/2.
  The FINDINGS paraphrase "obsolete" was replaced by the review's own words, "the obsolescence of" (p. 455).
- **T11c checked from its logs** by `t11c_check.py` (8/8 runs; mutation-tested).
- **Slides:** every derivation step now has a short reason; each slide defines its symbols in a strip at the
  foot. Frame count unchanged (136). A latent layout bug was found while doing this: 11 frames began with a
  `{…}` group that beamer read as the frame subtitle; all fixed. Build: no warnings, no bad boxes.
- Tests: 21 entries (T1–T17 with T1b, T9b, T11a–c; T16 by hand). 19 PASS, T16 done by hand, T11b known-failing
  and diagnosed by T11c.
