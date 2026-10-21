import Mathlib

/-!
# Algebraic identities behind the CH5103 derivations

Machine-checked versions of the purely algebraic steps in `assets/derivations/` for
Gryn'ova, Coote & Corminboeuf, WIREs Comput. Mol. Sci. 2015, 5, 440.
Analytic facts (positivity of the Coulomb kernel, commutators of differential operators,
the adiabatic theorem) are outside the scope of this file and are checked in SymPy instead.
-/

namespace Ch5103

/-! ## §2  Two-determinant combinations (Figure 1) and the sign erratum -/

section Determinants
variable {R : Type*} [CommRing R]

/-- Unnormalised 2×2 Slater determinants iii = |a ᾱ... | and iv, written with
`A = φa(1)φb(2)`, `B = φb(1)φa(2)` and spin products `ab = α₁β₂`, `ba = β₁α₂`. -/
def Diii (A B ab ba : R) : R := A * ab - B * ba
def Div (A B ab ba : R) : R := A * ba - B * ab

/-- `D_iii + D_iv` factorises as (antisymmetric space) × (symmetric spin): the M_S = 0 triplet. -/
theorem sum_is_triplet (A B ab ba : R) :
    Diii A B ab ba + Div A B ab ba = (A - B) * (ab + ba) := by
  unfold Diii Div; ring

/-- `D_iv - D_iii` factorises as (symmetric space) × (antisymmetric spin): the open-shell singlet. -/
theorem diff_is_singlet (A B ab ba : R) :
    Div A B ab ba - Diii A B ab ba = (A + B) * (ba - ab) := by
  unfold Diii Div; ring

end Determinants

/-- The review's printed `+` combination is not the singlet: a concrete counterexample
(A = 1, B = 0, ab = 1, ba = 0). -/
theorem erratum_plus_is_not_singlet :
    ¬ (∀ A B ab ba : ℤ, Diii A B ab ba + Div A B ab ba = (A + B) * (ba - ab)) := by
  intro h
  have := h 1 0 1 0
  simp [Diii, Div] at this

/-! ## §3  Frozen-orbital energies: S–T gap = 2K = HOMO-energy difference (§10) -/

theorem gap_frozen (ha hb J K : ℝ) :
    (ha + hb + J + K) - (ha + hb + J - K) = 2 * K := by ring

theorem gap_as_homo_difference (ha hb J K : ℝ) :
    let ET := ha + hb + J - K
    let ES := ha + hb + J + K
    let Eion := ha
    ES - ET = (ES - Eion) - (ET - Eion) := by
  intro ET ES Eion; ring

/-! ## §5  Virial theorem from uniform scaling -/

/-- `E(η) = η² T + η V` has derivative `2T + V` at `η = 1`. -/
theorem scaling_derivative (T V : ℝ) :
    HasDerivAt (fun η : ℝ => η ^ 2 * T + η * V) (2 * T + V) 1 := by
  have h1 : HasDerivAt (fun η : ℝ => η ^ 2 * T) (2 * T) 1 := by
    simpa using ((hasDerivAt_pow 2 (1 : ℝ)).mul_const T)
  have h2 : HasDerivAt (fun η : ℝ => η * V) V 1 := by
    simpa using ((hasDerivAt_id (1 : ℝ)).mul_const V)
  simpa using h1.add h2

/-- Stationarity under scaling gives E = -T = V/2. -/
theorem virial_consequences (T V : ℝ) (h : 2 * T + V = 0) :
    T + V = -T ∧ T + V = V / 2 := by
  constructor <;> linarith

/-- Less screening: if the triplet is lower (ΔE < 0), both states obey the virial theorem and the
triplet has the larger e–e repulsion (ΔVee > 0), then ΔT > 0 and ΔVne < 2ΔE < 0 with |ΔVne| > ΔVee. -/
theorem less_screening (dT dVne dVee dE : ℝ)
    (hvir : 2 * dT + (dVne + dVee) = 0) (hE : dE = dT + dVne + dVee)
    (hlow : dE < 0) (hee : 0 < dVee) :
    0 < dT ∧ dVne < 2 * dE ∧ dVne < 0 ∧ dVee < -dVne := by
  refine ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- Frozen orbitals (ΔT = 0) are incompatible with the virial theorem unless ΔE = 0. -/
theorem frozen_orbitals_violate_virial (dT dV dE : ℝ)
    (hvir : 2 * dT + dV = 0) (hE : dE = dT + dV) (hfrozen : dT = 0) : dE = 0 := by
  subst hfrozen; linarith

/-! ## §6  H₂ dissociation: 2×2 CI with equal diagonals -/

/-- With equal diagonal elements `E` and coupling `K`, `E - K` is an eigenvalue
(root of the characteristic polynomial). -/
theorem ci_equal_diagonals (E K : ℝ) :
    (E - (E - K)) * (E - (E - K)) - K * K = 0 := by ring

/-- Dissociation limits of the minimal-basis integrals (zero differential overlap):
`J₁₁ = (U+V)/2`, `K₁₂ = (U-V)/2`, `h₁₁ = E_H - 1/R`, `V = 1/R`. Then
RHF error = U/2 - 1/(2R), triplet and CI → 2E_H. -/
theorem h2_limits (EH U R : ℝ) (hR : R ≠ 0) :
    let V := 1 / R
    let h11 := EH - 1 / R
    let J11 := (U + V) / 2
    let K12 := (U - V) / 2
    let ERHF := 2 * h11 + J11 + 1 / R
    let ET := 2 * h11 + J11 - K12 + 1 / R
    let ECI := ERHF - K12
    ERHF = 2 * EH + U / 2 - 1 / (2 * R) ∧ ET = 2 * EH ∧ ECI = 2 * EH := by
  intro V h11 J11 K12 ERHF ET ECI
  refine ⟨?_, ?_, ?_⟩ <;> simp only [ERHF, ET, ECI, h11, J11, K12, V] <;> field_simp <;> ring

/-! ## §6  Two-orbital gap model -/

theorem gap_model_root (Jd D K s : ℝ) (hs : s ^ 2 = D ^ 2 + K ^ 2) :
    let E := Jd - s
    (Jd - D - E) * (Jd + D - E) - K ^ 2 = 0 := by
  intro E; simp only [E]; linear_combination hs

/-! ## §7  Extended Hubbard dimer -/

/-- `E_S = (U + V + 2k - s)/2` with `s² = (U-V)² + 16t²` solves the covalent/ionic secular equation. -/
theorem dimer_singlet_root (U V k t s : ℝ) (hs : s ^ 2 = (U - V) ^ 2 + 16 * t ^ 2) :
    let E := (U + V + 2 * k - s) / 2
    (V + k - E) * (U + k - E) - (2 * t) ^ 2 = 0 := by
  intro E; simp only [E]; linear_combination (1 / 4 : ℝ) * hs

/-- The singlet–triplet gap of the extended dimer. -/
theorem dimer_gap (U V k s : ℝ) :
    (U + V + 2 * k - s) / 2 - (V - k) = (U - V) / 2 + 2 * k - s / 2 := by ring

/-! ## §8  Pairing theorem for alternant (bipartite) Hückel matrices -/

/-- If `(u, v)` is an eigenvector of `[[0, B], [Bᵀ, 0]]` with eigenvalue `x`
(i.e. `B v = x u`, `Bᵀ u = x v`), then `(u, -v)` is one with eigenvalue `-x`. -/
theorem pairing {m n : Type*} [Fintype m] [Fintype n]
    (B : Matrix m n ℝ) (u : m → ℝ) (v : n → ℝ) (x : ℝ)
    (h1 : B.mulVec v = x • u) (h2 : B.transpose.mulVec u = x • v) :
    B.mulVec (-v) = (-x) • u ∧ B.transpose.mulVec u = (-x) • (-v) := by
  constructor
  · rw [Matrix.mulVec_neg, h1, neg_smul]
  · rw [h2, neg_smul, smul_neg, neg_neg]

/-! ## §13  3d/4s: Δ = (ε_d − ε_s) + (J̄_dd − J̄_ds) -/

/-- Average-of-configuration energy of `d^nd s^ns` (pair counts written as polynomials). -/
noncomputable def Econf (hd hs Jdd Jds Jss nd ns : ℝ) : ℝ :=
  nd * hd + ns * hs + nd * (nd - 1) / 2 * Jdd + nd * ns * Jds + ns * (ns - 1) / 2 * Jss

theorem three_d_four_s (hd hs Jdd Jds Jss n : ℝ) :
    let E := Econf hd hs Jdd Jds Jss
    let Δ := E (n + 1) 1 - E n 2
    let εd := E n 2 - E (n - 1) 2
    let εs := E n 2 - E n 1
    Δ = (εd - εs) + (Jdd - Jds) := by
  intro E Δ εd εs
  simp only [Δ, εd, εs, E, Econf]; ring

/-! ## §16  Yamaguchi spin projection -/

/-- With `H = -2J S₁·S₂` (E_S = 3J/2, E_T = -J/2), a broken-symmetry state that is a
`cS² : cT²` mixture with `⟨S²⟩_BS = 2 cT²` satisfies
`J = (E_BS − E_HS) / (⟨S²⟩_HS − ⟨S²⟩_BS)` with `⟨S²⟩_HS = 2`. -/
theorem yamaguchi (J cS2 cT2 : ℝ) (hnorm : cS2 + cT2 = 1) (hT : cT2 ≠ 1) :
    let ES := 3 * J / 2
    let ET := -J / 2
    let EBS := cS2 * ES + cT2 * ET
    let S2BS := 2 * cT2
    J = (EBS - ET) / (2 - S2BS) := by
  intro ES ET EBS S2BS
  have h : (2 : ℝ) - 2 * cT2 ≠ 0 := by
    intro h0; apply hT; linarith
  simp only [EBS, ES, ET, S2BS]
  rw [eq_div_iff h]
  have : cS2 = 1 - cT2 := by linarith
  subst this; ring

end Ch5103
