"""Chapter 19: the seventeen Lean theorems, read line by line (verification/lean_proofs/Ch5103/Identities.lean).

Not in the slide deck beyond one excerpt (chapter 16). Each scene shows the exact source and explains the statement,
its hypotheses and every tactic of the proof.
"""
import manimgx as m

from ch18_tests import Walk
from noir import CYAN, GOLD, GREEN, MUTED, Box, Frame, boxed, bullets, excerpt, pill, rich

L = "lean_proofs/Ch5103/Identities.lean"


class S153LeanIntro(Walk):
    TITLE = "Lean 4 and Mathlib: what is checked, and how"
    SUBTITLE = "verification/lean_proofs, Lean 4.29.1 with Mathlib v4.29.1"
    SYMBOLS = (r"Lean: a proof assistant; a theorem is accepted only if its proof type-checks — Mathlib: Lean's library "
               r"of formalised mathematics — `CommRing R`: any commutative ring, so the identities hold for numbers, "
               r"polynomials or functions alike — tactic: a command that builds part of a proof")
    STEPS = [
        ("code", L, 1, 17, [
            ([0], "The seventeenth test is a Lean file. Lean is a proof assistant: a theorem is accepted only if its "
                  "proof type-checks against the rules of logic. The file imports Mathlib, Lean's library of formalised "
                  "mathematics."),
            ([2, 3, 4, 5, 6, 7, 8, 9],
             "Its header says what it covers: the purely algebraic steps of the derivations. Analytic facts, such as the "
             "positivity of the Coulomb kernel, commutators of differential operators and the adiabatic theorem, are "
             "outside its scope and are checked in SymPy instead."),
            ([11, 13, 15, 16],
             "Everything lives in the namespace C H fifty one oh three. The first section works over any commutative "
             "ring R, so its identities hold whether the symbols stand for numbers, polynomials or functions."),
        ]),
        ("note", "seventeen theorems: three on the Figure 1 combinations and the erratum; two on the gap as a HOMO "
                 "difference; two on the virial theorem; two on less screening; two on H₂ dissociation; three on the "
                 "gap model and the Hubbard dimer; the pairing theorem; the 3d/4s identity; Yamaguchi's projection",
         "The seventeen theorems: three on the Figure one combinations and the sign erratum; two on the gap as a HOMO "
         "difference; two on the virial theorem; two on less screening; two on the dissociation of H two; three on the "
         "gap model and the Hubbard dimer; the pairing theorem; the three d four s identity; and Yamaguchi's "
         "projection. We read them in order.", "plain"),
    ]


class S154LeanDeterminants(Walk):
    TITLE = "Lean: the Figure 1 combinations and the sign erratum"
    SUBTITLE = "three theorems: sum_is_triplet, diff_is_singlet, erratum_plus_is_not_singlet"
    SYMBOLS = (r"`def`: a definition — `unfold`: replace defined names by their definitions — `ring`: prove an equation "
               r"of commutative-ring expressions by normalising both sides — `¬`: not — `simp ... at this`: simplify a "
               r"hypothesis; a false hypothesis closes the goal")
    STEPS = [
        ("code", L, 19, 42, [
            ([0, 1, 2, 3],
             "Write A for phi a of one times phi b of two, B for the swapped product, and a b and b a for the two spin "
             "products alpha one beta two and beta one alpha two. Then determinant iii is A times a b minus B times b a, "
             "and determinant iv is A times b a minus B times a b: the definitions D iii and D iv."),
            ([5, 6, 7, 8],
             "Theorem sum is triplet: D iii plus D iv equals A minus B, times a b plus b a: antisymmetric space times "
             "symmetric spin, the M S zero triplet. The proof unfolds the two definitions and lets ring normalise both "
             "sides."),
            ([10, 11, 12, 13],
             "Theorem diff is singlet: D iv minus D iii equals A plus B, times b a minus a b: symmetric space times "
             "antisymmetric spin, the open-shell singlet. Same proof."),
            ([15, 17, 18, 19, 20, 21, 22, 23],
             "And theorem erratum plus is not singlet: it is not true that, for all integers, D iii plus D iv equals the "
             "singlet's form. The proof assumes it, as h, and specialises it to A one, B zero, a b one, b a zero. "
             "Then the left side is one and the right side minus one, and simp turns the hypothesis into one equals "
             "minus one, which is false. The review's printed combination is refuted by a concrete counterexample."),
        ]),
    ]


class S155LeanGap(Walk):
    TITLE = "Lean: the singlet–triplet gap as a HOMO difference"
    SUBTITLE = "two theorems: gap_frozen, gap_as_homo_difference"
    SYMBOLS = (r"`ℝ`: the real numbers — `let`: a local name for an expression — `intro`: bring the local names into the "
               r"proof — chapter 12: $\varepsilon^{\text{OSS}}_{\text{HOMO}}-\varepsilon^{T}_{\text{HOMO}}=2K$")
    STEPS = [
        ("code", L, 44, 54, [
            ([0, 2, 3],
             "Theorem gap frozen: with frozen orbitals, the open-shell singlet energy h a plus h b plus J plus K, minus "
             "the triplet energy h a plus h b plus J minus K, is two K. Ring proves it in one step."),
            ([5, 6, 7, 8, 9, 10],
             "Theorem gap as HOMO difference names the triplet, singlet and ion energies, and states that the gap equals "
             "the singlet's removal energy minus the triplet's: E S minus E ion, minus E T minus E ion. intro brings "
             "the names in, and ring finishes. This is chapter twelve's result."),
        ]),
    ]


class S156LeanVirial(Walk):
    TITLE = "Lean: the virial theorem from uniform scaling"
    SUBTITLE = "two theorems: scaling_derivative, virial_consequences"
    SYMBOLS = (r"`HasDerivAt f f' x`: $f$ is differentiable at $x$ with derivative $f'$ — `hasDerivAt_pow`, `mul_const`, "
               r"`add`: Mathlib's rules for powers, constant multiples and sums — `simpa using`: simplify, then close with "
               r"the given fact — `constructor`: split an ∧ into two goals — `linarith`: linear arithmetic")
    STEPS = [
        ("code", L, 56, 70, [
            ([0, 2, 3, 4],
             "The virial theorem, from uniform scaling. Scale all coordinates by eta: the kinetic energy scales as eta "
             "squared and the Coulomb energy as eta, so the energy is eta squared T plus eta V. Theorem scaling "
             "derivative states that this function has derivative two T plus V at eta equal to one."),
            ([5, 6, 7, 8, 9],
             "The proof differentiates the two terms with Mathlib's rules: the power rule times the constant T gives two "
             "T, the identity times the constant V gives V, and the sum rule adds them. This is real calculus, checked "
             "by Lean, not algebra."),
            ([11, 12, 13, 14],
             "Theorem virial consequences: if the energy is stationary under scaling, so two T plus V is zero, then the "
             "energy T plus V equals minus T and equals V over two. constructor splits the two claims, and linarith "
             "proves each by linear arithmetic."),
        ]),
    ]


class S157LeanScreening(Walk):
    TITLE = "Lean: less screening, and why frozen orbitals fail"
    SUBTITLE = "two theorems: less_screening, frozen_orbitals_violate_virial"
    SYMBOLS = (r"`refine ⟨_, _, _, _⟩`: prove a four-part conjunction part by part — `subst`: replace a variable by its "
               r"value — by hand: $\Delta E=-\Delta T$, $\Delta V=2\Delta E$, $\Delta V_{ne}=2\Delta E-\Delta V_{ee}$")
    STEPS = [
        ("code", L, 72, 83, [
            ([0, 1, 2, 3, 4, 5, 6],
             "Theorem less screening. Four real numbers, the triplet-minus-singlet differences, and four hypotheses: "
             "the virial theorem for the differences, two delta T plus delta V n e plus delta V e e equal to zero; the "
             "energy as the sum of its parts; the triplet lower; and its repulsion higher. Four conclusions, each closed "
             "by linarith."),
            ([8, 9, 10, 11],
             "Theorem frozen orbitals violate virial: if the kinetic energy does not change, the virial theorem forces "
             "the energy gap to be zero. subst puts delta T equal to zero, and linarith finishes."),
        ]),
        ("note", r"by hand: $\Delta E=\Delta T+\Delta V$ and $2\Delta T+\Delta V=0$ give $\Delta T=-\Delta E>0$ and "
                 r"$\Delta V=2\Delta E$; so $\Delta V_{ne}=2\Delta E-\Delta V_{ee}<2\Delta E<0$ and "
                 r"$-\Delta V_{ne}=\Delta V_{ee}-2\Delta E>\Delta V_{ee}$",
         "What linarith finds, by hand: the energy is delta T plus delta V, and the virial theorem says two delta T "
         "plus delta V is zero; so delta T is minus delta E, which is positive, and delta V is two delta E. Then delta "
         "V n e is two delta E minus delta V e e, below two delta E and below zero, and its size exceeds delta V e e by "
         "minus two delta E. Every step is linear, which is why linarith can do it.", "checked"),
    ]


class S158LeanH2(Walk):
    TITLE = "Lean: H₂ dissociation"
    SUBTITLE = "two theorems: ci_equal_diagonals, h2_limits"
    SYMBOLS = (r"zero differential overlap at large $R$: $J_{11}=\tfrac{U+V}2$, $K_{12}=\tfrac{U-V}2$, $h_{11}=E_H-\tfrac1R$, "
               r"$V=\tfrac1R$ — `field_simp`: clear denominators, using $R\ne0$ — `<;>`: apply the next tactic to every goal")
    STEPS = [
        ("code", L, 85, 105, [
            ([0, 2, 3, 4, 5],
             "Theorem C I equal diagonals: when the two closed shells have equal diagonal energies E and coupling K, E "
             "minus K is a root of the characteristic polynomial: E minus E minus K, squared, minus K squared, is zero."),
            ([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
             "Theorem h two limits encodes the dissociation of chapter seven: V is one over R, h one one is E H minus one "
             "over R, J one one is U plus V over two, and K one two is U minus V over two; with them the RHF, triplet "
             "and CI energies."),
            ([18, 19, 20],
             "The claims: RHF equals two E H plus U over two minus one over two R; the triplet and CI both equal two E H. "
             "The proof splits the three claims, substitutes the definitions, clears the denominators using R not zero, "
             "and closes each by ring."),
        ]),
    ]


class S159LeanModels(Walk):
    TITLE = "Lean: the gap model and the Hubbard dimer"
    SUBTITLE = "three theorems: gap_model_root, dimer_singlet_root, dimer_gap"
    SYMBOLS = (r"`s` with `s^2 = …`: the square root, introduced by its defining equation — `linear_combination e`: the "
               r"goal minus the combination `e` of hypotheses must be a ring identity — chapter 7: the gap model; chapter "
               r"8: the extended dimer")
    STEPS = [
        ("code", L, 107, 124, [
            ([0, 2, 3, 4, 5],
             "Theorem gap model root. The square root is introduced as a number s whose square is delta squared plus K "
             "squared. Then E equal to J d minus s solves the secular equation: J d minus delta minus E, times J d plus "
             "delta minus E, minus K squared, is zero. The left side equals s squared minus delta squared minus K "
             "squared, so linear combination of the hypothesis proves it."),
            ([7, 9, 10, 11, 12, 13],
             "Theorem dimer singlet root, for the extended Hubbard dimer: with s squared equal to U minus V squared plus "
             "sixteen t squared, the singlet energy U plus V plus two k minus s, over two, solves the covalent-ionic "
             "secular equation. Here the left side is one quarter of the hypothesis, hence the factor one quarter."),
            ([15, 16, 17],
             "Theorem dimer gap: subtracting the triplet energy V minus k gives U minus V over two, plus two k, minus s "
             "over two: chapter eight's gap, by ring."),
        ]),
    ]


class S160LeanPairing(Walk):
    TITLE = "Lean: the pairing theorem"
    SUBTITLE = "for any finite index sets and any real matrix B"
    SYMBOLS = (r"`Matrix m n ℝ`: a real matrix with rows indexed by `m`, columns by `n` — `mulVec`: matrix times vector — "
               r"`•`: scalar multiplication — `rw [...]`: rewrite with equations in order — `mulVec_neg`, `neg_smul`, "
               r"`smul_neg`, `neg_neg`: $B(-v)=-Bv$, $(-x)u=-(xu)$, $x(-v)=-(xv)$, $-(-y)=y$")
    STEPS = [
        ("code", L, 126, 136, [
            ([0, 2, 3],
             "The pairing theorem of chapter nine, in full generality: rows and columns indexed by any finite sets, and "
             "any real matrix B."),
            ([4, 5, 6, 7],
             "Hypotheses: B times v equals x times u, and B transpose times u equals x times v, which says u, v is an "
             "eigenvector of the alternant matrix with eigenvalue x. Conclusion: B times minus v is minus x times u, "
             "and B transpose times u is minus x times minus v; so u, minus v has eigenvalue minus x."),
            ([8, 9, 10],
             "constructor splits the two halves. The first rewrites B times minus v as minus B v, then uses the first "
             "hypothesis and moves the sign onto x. The second uses the second hypothesis, then sign rules: minus x "
             "times minus v is x times v."),
        ]),
    ]


class S161LeanThreeD(Walk):
    TITLE = "Lean: the 3d/4s identity"
    SUBTITLE = "Econf and three_d_four_s"
    SYMBOLS = (r"`noncomputable def`: a definition over the reals, which Lean cannot evaluate but can reason about — pair "
               r"counts written as $n(n-1)/2$ — `simp only [...]`: unfold exactly the listed names")
    STEPS = [
        ("code", L, 138, 151, [
            ([0, 2, 3, 4],
             "The average-of-configuration energy of chapter thirteen, E conf: n d h d plus n s h s, plus n d times n d "
             "minus one over two J d d, plus n d n s J d s, plus n s times n s minus one over two J s s. The pair counts "
             "are written as polynomials, so they make sense for any real n."),
            ([6, 7, 8, 9, 10, 11],
             "Theorem three d four s: with delta the energy of d n plus one s minus that of d n s two, and the two "
             "orbital energies as removal energies, delta equals epsilon d minus epsilon s, plus J d d minus J d s."),
            ([12, 13],
             "The proof unfolds every name down to E conf and lets ring check the polynomial identity."),
        ]),
    ]


class S162LeanYamaguchi(Walk):
    TITLE = "Lean: Yamaguchi's projection"
    SUBTITLE = "the formula of chapter 15, with the division made safe"
    SYMBOLS = (r"`hT : cT2 ≠ 1`: the broken-symmetry state is not a pure triplet, so the denominator is not zero — "
               r"`eq_div_iff h`: $a=b/c\iff ac=b$ when $c\ne0$ — `apply hT`: reduce the goal to $cT2=1$")
    STEPS = [
        ("code", L, 153, 170, [
            ([0, 2, 3, 4],
             "Yamaguchi's projection. The comment states the convention: H equal to minus two J S one dot S two, so the "
             "singlet energy is three J over two and the triplet minus J over two."),
            ([5, 6, 7, 8, 9, 10],
             "The theorem: for weights c S squared and c T squared summing to one, with c T squared not one, the "
             "broken-symmetry energy and S squared give back J through the formula E B S minus E T, over two minus S "
             "squared of the broken-symmetry state."),
            ([11, 12, 13],
             "The proof first shows the denominator two minus two c T squared is not zero: if it were, c T squared would "
             "be one, contradicting the hypothesis."),
            ([14, 15, 16, 17],
             "Then it unfolds the names, turns the division into a multiplication, substitutes c S squared equals one "
             "minus c T squared, and ring checks that J times two minus two c T squared is E B S minus E T."),
        ]),
    ]


class S163LeanAudit(Frame):
    """The axiom audit and how to rebuild the proofs."""

    TITLE = "Lean: the axiom audit, and how to rebuild"

    def construct(self) -> None:
        self.setup_frame()
        audit = boxed("`#print axioms` for each of the 17 theorems lists nothing beyond `propext`, `Classical.choice` "
                      "and `Quot.sound`, the three standard axioms of Lean's logic; the two determinant identities need "
                      "only `propext` and `Quot.sound`. No `sorry`, no extra axiom, no unproved step. Re-checked for this "
                      "video against the built library.", "checked", width=12.4, size=29,
                      tag="Axiom audit").move_to([0, 1.2, 0])
        how = bullets(["`make lean`: `lake exe cache get` downloads Mathlib's compiled files, then `lake build` checks "
                       "the proofs",
                       "pinned: `lean-toolchain` says Lean 4.29.1, `lakefile.toml` pins Mathlib to v4.29.1",
                       "what Lean does not check: the physics — that these algebraic statements are the right ones is "
                       "argued in the derivations and tested numerically by T1–T15"], width=12.4, size=28)
        how.move_to([0, -1.3, 0])
        self.say("[The axiom audit. For each of the seventeen theorems, print axioms lists nothing beyond "
                 "propositional extensionality, classical choice and quotient soundness, the three standard axioms of "
                 "Lean's logic; the two determinant identities need only the first and the last. There is no sorry, no "
                 "extra axiom, and no unproved step. We re-checked this for the video against the built library.]",
                 m.FadeIn(audit))
        self.say("[To rebuild: make lean downloads Mathlib's compiled files and then checks the proofs with lake build.]",
                 m.FadeIn(how[0]))
        self.say("[The versions are pinned: the toolchain file says Lean four point two nine point one, and the lake file "
                 "pins Mathlib to the same version.]", m.FadeIn(how[1]))
        self.say("[And what Lean does not check is the physics. That these algebraic statements are the right ones is "
                 "argued in the derivations, and tested numerically by tests one to fifteen.]", m.FadeIn(how[2]))
        self.wait(0.5)
