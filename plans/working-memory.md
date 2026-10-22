# Working memory
## Decisions
- DEC1: derivations are first-principles [DERIVED] + numerically tested; original papers mostly
  paywalled (agents got only abstracts/metadata) -> attribute only verified claims to originals.
- DEC2: sub-agents use model haiku (user).
## Discoveries
- DIS1: paper's 2-det OSS uses '+' -> actually M_S=0 triplet (sympy, earlier this session).
- DIS2: review cites Kollmar & Staemmler (ref 9) for Hund 1925 + Slater explanation; Slater 1929 not cited directly.
- DIS3: Katriel–Pauncz Adv Quant Chem 10 listed as 1977 by ScienceDirect/S2 (review says 1975) [to verify T16].
- DIS4: PYTHONPATH env leaks py3.14 site-packages; use python -I.
## Reversals
## Open questions
- OQ1: sign convention of paper's Janak statement (eps_T - eps_OSS) -> resolve by derivation D11.
- DIS5: Longuet-Higgins N-2T is a LOWER bound on #NBMO (CBD: 2 NBMOs, N-2T=0) [T8].
- DIS6: Lieb 1989 theorem = rigorous Hubbard version of Ovchinnikov rule; ED confirms for CBD,TMM,TME,MX,TriMB,TetraMB.
- DIS7: RHF dissociation error of H2 (minimal basis) = K12 -> (AA|AA)/2 as R->inf [T5 numbers].
- DIS8: Hongo 2004 Table I numbers verified from arXiv PDF; He 1s2s computed here shows same pattern.
- DIS9: Katriel–Pauncz is 1977 (review says 1975).
- DEC3: GPU (Radeon 780M gfx1103, ROCm) not usable by PySCF (CUDA-only gpu4pyscf); workloads are seconds; use OMP_NUM_THREADS=16.
- DIS10: MP2 SS/OS per-pair correlation ratio 0.32-0.43 (molecules) vs He 0.023 -> "order of magnitude" is system-dependent.
- DIS11: ROHF canonicalisation: SOMO/HOMO flip needs A*~1.04 (outside [0,1]) for H2NO/NO2/CH3/allyl.
- DIS12: Reduction step: diradical formation on reduction requires eps_l < eps_s^beta (separate condition) — corrected in sec11.
- DIS13: T11b anion: orbital-level SOMO-HOMO conversion present, but B3LYP vertical ΔSCF slightly favours closed-shell zwitterion (0.06 eV) for short CH2CH2 linker. [HYPOTHESIS] Coulomb proximity of zwitterion charges and/or B3LYP delocalisation error; test with CAM-B3LYP and longer separation (T11c).
- DEC4: Lean T17 project at verification/lean_proofs (Lean v4.29.1, Mathlib v4.29.1) via elan; user separately building lean4 4.27 from AUR.
## Reversals
- REV1: T8 Longuet-Higgins equality -> inequality (N-2T lower bound).
- REV2: T11a "canonicalisation flips ordering within standard schemes" -> only for weights outside [0,1].
- DIS14 (resolves DIS13): T11b no-crossover is functional-specific. CAM-B3LYP gives diradical 0.36 eV below CS for the short anion; acid stays CS (1.42 eV). Separation not decisive at B3LYP (TEMPO +0.067). Mechanism (delocalisation error) remains [HYPOTHESIS].
