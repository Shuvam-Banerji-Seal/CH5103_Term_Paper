# Are the claims in the review correct?

Assessment of Gryn'ova, Coote & Corminboeuf, *WIREs Comput. Mol. Sci.* **2015**, 5, 440–459
([doi:10.1002/wcms.1233](https://doi.org/10.1002/wcms.1233)).

The full derivations are in [`derivations/derivations.pdf`](../derivations/derivations.pdf). The
test IDs (T1…T17) refer to [`VERIFICATION.md`](VERIFICATION.md).

**Summary.** The physics holds up wherever it could be tested. There is one mathematical error and one
citation error. A few statements are overstated. The review's central chemical claim (the energetics of
oxidising a distonic radical anion) is only partly reproduced by our model calculation.

## Confirmed

| Claim (page) | Evidence |
|---|---|
| The triplet M_S = ±1 components are single determinants; the open-shell singlet needs two (p. 441). | Symbolic expansion (T1); Lean `sum_is_triplet`, `diff_is_singlet` (T17). |
| Hund's rule: the high-spin state is stabilised by stronger electron–nucleus attraction ("less screening"), not by lower e–e repulsion (p. 442). | Exact He 1s2s calculation (T4): the triplet has **higher** V_ee (+0.0185 E_h) and lower V_ne (−0.0772 E_h). Virial ratio = 2.000000. Matches Hongo et al. 2004, Table I (carbon). Lean `less_screening`, `frozen_orbitals_violate_virial`. |
| Static correlation grows as the orbital interaction weakens (H₂ dissociation, twisted ethylene; Fig. 2) (p. 442). | Closed-form H₂ minimal-basis limits vs PySCF to 4×10⁻¹⁶ E_h (T5); two-orbital gap model (T6). |
| Kinetic exchange: ionic configurations mix only into the singlet (p. 442). | Spin-symmetry proof and extended-Hubbard dimer, analytic vs full CI (T7). |
| Disjoint NBMOs make the open-shell singlet competitive; non-disjoint NBMOs give high spin (CBD, TME vs TMM, MX, TriMB) (p. 443–444). | Explicit disjoint NBMOs for TME and CBD; proof that TMM has none (§8). Hückel tests (T8). Hubbard model: the gap is linear in U for non-disjoint and ∝ U² for disjoint diradicals (T9b). |
| Spin-polarisation alternation; odd/even topology rule; Ovchinnikov's rule (p. 443). | Exact diagonalisation for 7 π systems reproduces S = ½\|n_A − n_B\| (T9). Lieb's 1989 theorem makes the rule rigorous for the Hubbard model. |
| The 3d/4s ordering and ionisation paradox (p. 448). | Average-of-configuration identity Δ = (ε_d − ε_s) + (J̄_dd − J̄_ds) (T12; Lean `three_d_four_s`). |
| Individual electrons have no good quantum numbers; only total L, S are conserved (p. 448). | [l₁, 1/r₁₂] ≠ 0 but [L, 1/r₁₂] = 0, symbolically (T13). |
| ROHF orbital energies are not unique (p. 449). | Stationarity blocks derived and checked; the SOMO/HOMO order depends on canonicalisation (T11a). |
| The S–T gap equals a HOMO-energy difference at the Hartree–Fock level (p. 443). | Frozen-orbital derivation: E_S − E_T = ε_HOMO(S) − ε_HOMO(T) = 2K (T10, T17). |

## Errors

1. **Sign error, p. 441.** The open-shell singlet is printed as ½(D_iii **+** D_iv). That combination is
   the M_S = 0 **triplet**. The singlet is ½(D_iv − D_iii). (The product form on the line above is correct.)
2. **Citation year.** Katriel & Pauncz, *Adv. Quantum Chem.* 10, 143–185 is from **1977**, not 1975
   ([doi:10.1016/S0065-3276(08)60580-8](https://doi.org/10.1016/S0065-3276(08)60580-8)).

## Overstated or imprecise

- **"Same-spin pair correlation is an order of magnitude smaller."** True for He (ratio ≈ 0.023). For
  molecular valence shells at MP2 the per-pair ratio is ≈ 0.3–0.4 (T15).
- **"The aufbau principle violates the Pauli principle."** This is rhetorical. An aufbau-filled
  determinant is fully antisymmetric. The real issue is that orbital energies from different
  configurations cannot be compared (§13).
- **"Aufbau and Hund's rule are obsolete" (conclusion).** Too strong. Hund's rule holds for nearly all
  atoms; the review's exceptions involve special topologies or charge effects.
- **ROHF canonicalisation.** The ordering is indeed convention-dependent. But for common radicals
  (H₂NO, NO₂, CH₃, allyl) a SOMO/HOMO flip needs a mixing weight slightly outside the usual [0, 1]
  range (A* ≈ 1.04) (T11a).
- **Janak/Koopmans statement.** The sign convention is not stated in the review; the derivation fixes it.

## Reproduced, but functional-dependent: SOMO–HOMO conversion in distonic radical anions

Model: •ON(Me)CH₂CH₂COO⁻ and its conjugate acid, plus TEMPO-4-carboxylate. Vertical oxidation from the
radical geometry to the triplet diradical (T) or the closed-shell singlet (CS). Tests T11b and T11c.

| radical | functional | α-SOMO | Δ(T − CS) |
|---|---|---|---|
| short acid | B3LYP / CAM-B3LYP | is the HOMO | +1.41 / +1.42 eV |
| short anion | B3LYP | 3 levels below α-HOMO | +0.07 eV |
| short anion | **CAM-B3LYP** | 3 levels below α-HOMO | **−0.36 eV** |
| TEMPO-4-COO⁻ | B3LYP | 2 levels below α-HOMO | +0.07 eV |

- **Orbital inversion and its removal on protonation:** reproduced with both functionals.
- **Energetic switch (anion oxidised to a diradical, acid to a closed shell):** reproduced with the
  range-separated CAM-B3LYP. B3LYP misses it by ~0.07 eV, and lowers the closed-shell product
  disproportionately (0.61 vs 0.17 eV). Delocalisation error is a plausible cause, but this is untested.
- **Incomplete:** the TEMPO-4-carboxylate runs at CAM-B3LYP and for the TEMPO acid were stopped by a
  low-memory condition.

## Not checked

- The experimental claims about specific molecules in Figs. 7–9 and 11–17.
- The historical statements (Bohr, Ehrenfest, Pauli) and the maximum-hardness interpretation.

Most of these originals are paywalled. The access status of every source is listed in §17 of the
derivations.
