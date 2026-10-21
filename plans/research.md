# Research archive (append-only)
## Cycle 1 — 4 haiku agents (paywall-limited)
- Krylov CPL 2001 338:375 intro: correlation energy "about order of magnitude smaller for a pair of
  two electrons with the same spins than ... opposite spins" [VERIFIED: ScienceDirect preview via agent].
- SCS-MP2 c_os=6/5, c_ss=1/3 (Grimme JCP 2003 118:9095) [secondary: manuals].
- Balkova & Bartlett JCP 1994 101:8972 doi 10.1063/1.468057: square CBD singlet 6.9 kcal/mol below triplet [abstract].
- Yamaguchi projection J=(E_BS-E_HS)/(<S2>_HS-<S2>_BS) [secondary: IntechOpen chapter, ORCA manual].
- Boyd Nature 1984 310:480 doi 10.1038/310480a0 abstract: Hund's rule from Fermi correlation -> less screening of nucleus in high-spin state.
- Hongo et al JCP 2004 121:7144 doi 10.1063/1.1795151 abstract: triplet energy gain due to greater e-n attraction; virial satisfied; arXiv cond-mat/0408147.
- He exact NR energies: 2^1S -2.1459740460544, 2^3S -2.1752293782367 Eh (Drake, via arXiv 2301.05442).
- Ovchinnikov TCA 1978 47:297 doi 10.1007/BF00549259: S=(N_A-N_B)/2 (as quoted in arXiv 1906.08544).
- Janak PRB 1978 18:7165 abstract: dE/dn_i = eps_i independent of xc functional.
- Liu & Langenaeker TCA 2003 110:338 doi 10.1007/s00214-003-0487-6: Delta E_ST = Delta eps_HOMO [search summary only].
- Westcott et al JACS 2000 122:8083 doi 10.1021/ja994018p VO(oep) non-aufbau PES.
- Glaesemann & Schmidt JPCA 2010 114:8772 doi 10.1021/jp101758y (content not accessed).
- Not accessed: Borden–Davidson 1977 (doi 10.1021/ja00456a010), Kollmar–Staemmler 1978 (doi 10.1007/BF00549021),
  Gallup 1987, Salem–Rowland 1972 (doi 10.1002/anie.197200921), BKM 1987 (doi 10.1002/anie.198701701),
  Vanquickenborne 1989, Melrose–Scerri 1996, Scerri 1991, Ehrenfest 1917, Pauli 1925.
## Cycle 1 — own searches (T16)
- Lieb EH, PRL 62, 1201 (1989) (+erratum 62, 1927): repulsive Hubbard, bipartite, half filling:
  unique ground state with S = ½||B|−|A|| [VERIFIED: WebSearch summary of Princeton/INSPIRE/arXiv 1712.02694].
- Katriel & Pauncz, Adv Quantum Chem 10, 143–185, Academic Press, **1977**, doi 10.1016/S0065-3276(08)60580-8
  [VERIFIED: arXiv 2505.21455 ref list + Springer ref list]. Review's "1975" is a citation error.
- Hongo et al. JCP 121, 7144 (2004), arXiv cond-mat/0408147 [VERIFIED: PDF read]. Table I (Eh), C atom triplet(3P)/singlet(1D):
  HF: E −37.689/−37.631; Vee 12.760/12.728; Ven −88.137/−87.992; T 37.689/37.632.
  DMC (linear est.): Vee 12.538/12.464; Ven −88.231/−88.062; T 37.811/37.763; virial 2.002.
  Text: Slater mechanism = reduced Vee in high-S state; "incorrect as it is based on ... frozen orbitals ... leaves T unchanged,
  which cannot be correct as each eigenstate must satisfy the virial theorem". Davidson: He-like series HF -> reduction of Ven.
  Boyd: larger exclusion holes -> electrons closer to nucleus -> lower Ven ("less screening"); Vee higher in high-S state.
- Liu & Langenaeker 2003 abstract NOT retrievable this session [UNKNOWN content beyond review's paraphrase].
- PySCF rohf.get_roothaan_fock source (read this session): off-diagonal blocks c-o: Fb, o-v: Fa, c-v: Fc=(Fa+Fb)/2;
  diagonal blocks Fc (Roothaan/Ross-thesis choice).
