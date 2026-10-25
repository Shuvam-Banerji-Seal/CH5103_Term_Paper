"""Chapter 18: every verification script, walked through line by line (verification/*.py and results/*.txt).

Not in the slide deck: the deck shows the test matrix and three excerpts (chapter 16); this chapter explains what
each script computes and what its recorded output says. Code and output are read from the repository at render
time (noir.excerpt), so the video shows exactly what was run.
"""
import manimgx as m

from noir import CYAN, GOLD, GREEN, MUTED, ROSE, ROOT, Box, Frame, boxed, excerpt, pill, rich

V = "verification/"
R = "verification/results/"


MAX_LINES = 18   # a code window taller than this is unreadable at 1080p
WRAP = 100       # recorded output is wrapped at word boundaries to this many characters


def file_lines(path: str) -> list[str]:
    return (ROOT / path).read_text(encoding="utf-8").splitlines()


def window(path: str, first: int, idx: list[int], cur: tuple[int, int] | None) -> tuple[int, int]:
    """File lines to show for a group of excerpt lines: the group's span, extending the current window when the
    two fit together in MAX_LINES; blank lines trimmed from both ends (m.Code would drop them)."""
    lines = file_lines(path)
    lo, hi = first + min(idx), first + max(idx)
    if cur is not None and lo >= cur[0] and hi - cur[0] + 1 <= MAX_LINES:
        lo = cur[0]
    while lo < hi and not lines[lo - 1].strip():
        lo += 1
    while hi > lo and not lines[hi - 1].strip():
        hi -= 1
    return lo, hi


def wrapped_output(path: str, first: int, last: int) -> str:
    """Recorded output, lines first..last, long lines broken at spaces (continuations indented)."""
    import textwrap

    out = []
    for line in file_lines(path)[first - 1:last]:
        if len(line) <= WRAP:
            out.append(line)
        else:
            indent = len(line) - len(line.lstrip())
            out += textwrap.wrap(line, WRAP, subsequent_indent=" " * (indent + 4), break_long_words=False,
                                 break_on_hyphens=False, drop_whitespace=True)
    return "\n".join(out)


class Walk(Frame):
    """A scene made of steps, shown one at a time in the main area:
    ("code", file, first, last, [(line indices, narration), ...]) shows, for each group, a window of the file around
    the group's lines (at most MAX_LINES, line numbers as in the file), the group's lines bright and the rest dimmed;
    ("out", file, first, last, narration) shows recorded output (wrapped); ("note", text, narration, kind) a note."""

    STEPS: list = []

    def construct(self) -> None:
        self.setup_frame()
        current = None
        for step in self.STEPS:
            if current is not None:
                self.play(m.FadeOut(current), run_time=0.5)
                current = None
            kind = step[0]
            if kind == "code":
                _, path, first, last, groups = step
                cur = None
                for idx, text in groups:
                    lo, hi = window(V + path, first, idx, cur)
                    cur = (lo, hi)
                    c = excerpt(V + path, lo, hi, width=12.9, height=4.75).move_to([0, -0.15, 0])
                    for i, line in enumerate(c.code_lines):
                        if (lo + i) - first not in idx:
                            line.set_opacity(0.38)
                    cap = rich(f"`{V}{path}`, lines {lo}–{hi} of the excerpt {first}–{last}", 22, MUTED)
                    cap.next_to(c, m.UP, buff=0.08).align_to(c, m.LEFT)
                    view = m.Group(c, cap)
                    anim = m.FadeIn(view) if current is None else m.AnimationGroup(m.FadeOut(current), m.FadeIn(view))
                    self.say(f"[{text}]", anim)
                    current = view
            elif kind == "out":
                _, path, first, last, text = step
                c = m.Code(code_string=wrapped_output(R + path, first, last), language=None, add_line_numbers=False,
                           background="rectangle")
                if c.width > 12.9:
                    c.scale_to_fit_width(12.9)
                if c.height > 4.6:
                    c.scale_to_fit_height(4.6)
                c.move_to([0, -0.25, 0])
                cap = m.VGroup(pill("pass", size=24) if "FAIL" not in text else pill("fail", size=24),
                               rich(f"recorded output, `{R}{path}`", 22, MUTED)).arrange(m.RIGHT, buff=0.2)
                cap.next_to(c, m.UP, buff=0.12).align_to(c, m.LEFT)
                current = m.Group(c, cap)
                self.say(f"[{text.replace('FAIL', '')}]", m.FadeIn(current))
            else:
                _, body, text, box = step
                current = boxed(body, box, width=12.0, size=30).move_to([0, 0.0, 0])
                self.say(f"[{text}]", m.FadeIn(current))
        self.wait(0.5)


class S136T1(Walk):
    TITLE = "Test T1: spin functions and the Figure 1 combinations"
    SUBTITLE = "exact symbolic algebra with SymPy"
    SYMBOLS = (r"`kron`: Kronecker product, operator on electron 1 times operator on electron 2 — `sp_`, `sm`: one-electron "
               r"raising and lowering matrices — `S2`: total spin squared — `det(o1, o2)`: the 2×2 Slater determinant, "
               r"rows electrons, columns spin orbitals")
    STEPS = [
        ("code", "t01_spin_and_determinants.py", 4, 29, [
            ([0, 1, 2, 3, 4, 5],
             "Test T one starts in the spin space of two electrons, with basis alpha alpha, alpha beta, beta alpha and "
             "beta beta. For one electron, s z is a diagonal matrix of plus and minus one half, s plus raises beta to "
             "alpha, and s minus is its transpose."),
            ([6, 7, 8, 9, 10],
             "Two-electron operators are Kronecker products: an operator on electron one times the identity on electron "
             "two, plus the reverse. The total S squared is built from the identity S squared equals S minus S plus, "
             "plus S z squared, plus S z."),
            ([11, 12, 13, 14, 15, 16, 17, 18, 19],
             "Then the four spin functions: alpha alpha, the symmetric combination, beta beta, and the antisymmetric "
             "combination, each with the S squared and M S value it should have."),
            ([20, 21, 22, 23, 24, 25],
             "For each one the script applies S squared and S z exactly and checks that the result is the expected "
             "multiple of the function: three triplet components and one singlet."),
        ]),
        ("code", "t01_spin_and_determinants.py", 31, 58, [
            ([0, 1, 2, 3, 4], "Next, space times spin. Each orbital value and each spin value at electrons one and two "
                              "is a SymPy symbol, and det builds the two by two Slater determinant."),
            ([5, 6, 7, 8, 9, 10, 11],
             "The six determinants of Figure one are written exactly as in the review: i and ii closed shells, iii and iv "
             "the open-shell pairs, v and vi high spin."),
            ([12, 13, 14, 15, 16, 17, 18, 19, 20],
             "The targets: v and vi are the M S plus and minus one triplets; one half of iii plus iv is the M S zero "
             "triplet; one half of iv minus iii is the open-shell singlet; and the review's printed form, one half of "
             "iii plus iv, is compared with the singlet, expecting false."),
            ([21, 22, 23, 24, 25, 26, 27],
             "Each comparison expands the difference and tests whether it is identically zero. The test passes only if "
             "every true identity holds and the review's version fails."),
        ]),
        ("out", "t01_spin_and_determinants.txt", 1, 11,
         "The recorded output: all four spin functions have the right S squared and M S; the triplet and singlet "
         "combinations are confirmed; and the review's plus combination is not the singlet. T one passes, and it "
         "proves the sign erratum."),
    ]


class S137T1b(Walk):
    TITLE = "Test T1b: the sign erratum, numerically"
    SUBTITLE = "no algebra shared with T1: tensors on a grid and the spin operator applied directly"
    SYMBOLS = (r"`Psi[r1, s1, r2, s2]`: a two-electron state on M grid points and 2 spin values — `einsum`: tensor "
               r"contraction — eigen-residual: $\|\hat S^2\psi-\lambda\psi\|$, zero for an eigenfunction")
    STEPS = [
        ("code", "t01b_sign_error_numeric.py", 15, 32, [
            ([0, 1, 2, 3, 4],
             "Test T one b checks the erratum again with nothing in common with T one. Two random orthonormal vectors "
             "on a grid of seven points play the orbitals phi a and phi b, and spin is a two-vector."),
            ([5, 6, 7, 8, 9, 10, 11, 12, 13],
             "A spin orbital is the outer product of an orbital and a spin vector, and the determinant is chi one of "
             "electron one times chi two of electron two minus the swapped product, as a four-index tensor."),
            ([14, 15, 16, 17], "The two determinants iii and iv are transcribed exactly as printed in the paper."),
        ]),
        ("code", "t01b_sign_error_numeric.py", 34, 72, [
            ([0, 1, 2, 3, 4, 5],
             "The total spin squared is built from the Pauli matrices: the sum over x, y and z of the total component "
             "squared, as a four by four matrix acting on the two spin indices."),
            ([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
             "classify normalises a state, applies S squared, takes the expectation value, and measures the eigen-"
             "residual: zero means a true eigenfunction. It labels zero as singlet and two as triplet."),
            ([20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
             "Then it classifies the paper's plus combination, the corrected minus combination, iii alone, and the "
             "product form printed in the paper's first line, and compares that product form with both combinations."),
        ]),
        ("out", "t01b_sign_error_numeric.txt", 1, 6,
         "The output: the paper's one half of iii plus iv has S squared exactly two, a triplet, with residual ten to "
         "the minus sixteen. One half of iv minus iii has S squared zero: the singlet. Determinant iii alone has "
         "expectation one and a large residual: half singlet, half triplet. And the paper's own product form equals "
         "the minus combination, not the plus one."),
    ]


class S138T2(Walk):
    TITLE = "Test T2: the 2-electron, 2-orbital Hamiltonian against full CI"
    SUBTITLE = "PySCF full configuration interaction, random integrals"
    SYMBOLS = (r"8-fold symmetry: $(pq|rs)=(qp|rs)=(rs|pq)=\dots$ for real orbitals — PSD: positive semidefinite, so "
               r"exchange integrals are non-negative as for a real Coulomb kernel — `spin_square0`: ⟨S²⟩ of a CI vector")
    STEPS = [
        ("code", "t02_two_orbital_hamiltonian.py", 11, 55, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             "Test T two draws random symmetric one-electron integrals, and two-electron integrals built as a positive "
             "semidefinite matrix over orbital pairs, so that they have the full eight-fold symmetry and behave like a "
             "real Coulomb kernel."),
            ([11, 12, 13, 14, 15, 16],
             "For each of five trials it reads off h a, h b, h a b, the Coulomb and exchange integrals, and the mixed "
             "integrals a a a b and b b b a."),
            ([17, 18, 19, 20, 21, 22, 23, 24, 25],
             "Then the formulas derived in Part five: the triplet energy, and the three by three singlet matrix in the "
             "two closed shells and the open-shell singlet."),
            ([26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
             "The brute force: PySCF's full configuration interaction for two electrons in two orbitals, every root "
             "sorted into singlets and triplets by its S squared, plus a separate M S equal to one calculation."),
            ([37, 38, 39, 40, 41, 42, 43, 44],
             "Four checks per trial: the singlet eigenvalues match, the triplet matches, the open-shell singlet sits "
             "two K above the triplet, and K is not negative."),
        ]),
        ("code", "t02_two_orbital_hamiltonian.py", 57, 89, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
             "The second half checks the orbital energies of the quasi-closed shell, Part fifteen. det energy computes "
             "the energy of any single determinant by the Slater Condon rules: every pair pays Coulomb, and same-spin "
             "pairs also pay minus exchange."),
            ([12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
             "With s alpha, h alpha and h beta occupied, each orbital energy is the total energy minus the energy with "
             "that electron removed, and the script compares them with the three formulas, including epsilon h beta "
             "minus epsilon h alpha equal to K."),
            ([27, 28, 29, 30, 31, 32],
             "Finally the cation: after removing h, the open-shell singlet lies two K above the triplet."),
        ]),
        ("out", "t02_two_orbital_hamiltonian.txt", 1, 12,
         "Every trial matches: singlet and triplet eigenvalues, the two K gap, K non-negative, the orbital-energy "
         "relations and the cation splitting. T two passes."),
    ]


class S139T3(Walk):
    TITLE = "Test T3: exchange integrals are positive, and never exceed Coulomb"
    SUBTITLE = "RHF/6-31G water, every pair of molecular orbitals"
    SYMBOLS = (r"`ao2mo.kernel`: transform the integrals to the molecular-orbital basis — `K[p,q]`$=(pq|pq)$, "
               r"`J[p,q]`$=(pp|qq)$ — Part VI proved $J\ge K\ge0$ for any real orbitals")
    STEPS = [
        ("code", "t03_t05_hund_virial_h2.py", 11, 20, [
            ([0, 1, 2, 3],
             "Test T three: Part six proved that every exchange integral is non-negative and never exceeds the "
             "matching Coulomb integral. The script runs restricted Hartree Fock on water in the six thirty one G basis "
             "and transforms all two-electron integrals to the molecular orbitals."),
            ([4, 5, 6, 7, 8, 9],
             "It tabulates K p q and J p q for every pair, and checks that the smallest K is not negative, to ten to the "
             "minus twelve, and that J is at least K everywhere."),
        ]),
        ("out", "t03_t05_hund_virial_h2.txt", 1, 1,
         "The smallest exchange integral is one point one times ten to the minus three hartree, positive, and every "
         "Coulomb integral exceeds its exchange integral. T three passes."),
    ]


class S140T4(Walk):
    TITLE = "Test T4: helium 1s2s, the virial theorem and less screening"
    SUBTITLE = "an even-tempered 16s7p4d basis, scaled to satisfy the virial theorem, against Drake's exact energies"
    SYMBOLS = (r"even-tempered: exponents in geometric progression — $\eta$: uniform scaling of all exponents by "
               r"$\eta^2$ — $-V/T=2$: virial ratio of an exact or optimally scaled state — Drake: benchmark energies")
    STEPS = [
        ("code", "t03_t05_hund_virial_h2.py", 22, 41, [
            ([0, 1, 2, 3, 4, 5, 6, 7],
             "Test T four. The basis: sixteen s, seven p and four d Gaussian functions with exponents in geometric "
             "progression, all multiplied by eta squared, so the whole basis can be scaled uniformly."),
            ([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
             "For a given scaling and state, it builds the helium atom, orthogonalises the basis symmetrically, "
             "dropping near-linear dependencies, and transforms the kinetic, nuclear and repulsion integrals."),
        ]),
        ("code", "t03_t05_hund_virial_h2.py", 64, 81, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8],
             "The exact two-electron problem we saw in chapter sixteen is solved for each state, and the scaling eta is "
             "optimised to minimise the energy, which enforces the virial theorem."),
            ([9, 10, 11, 12, 13, 14, 15, 16, 17],
             "Then the differences, triplet minus singlet, of the energy, kinetic, attraction and repulsion; and the "
             "check: triplet lower, repulsion higher, attraction more negative by more than the repulsion rises, the "
             "virial ratio two for both states, and both energies within two millihartree of exact."),
        ]),
        ("out", "t03_t05_hund_virial_h2.txt", 2, 5,
         "The output: the triplet at minus two point one seven five two one two hartree, seventeen microhartree from "
         "exact; the singlet at minus two point one four five eight six five; both with virial ratio two. The "
         "triplet is lower by zero point zero two nine three, its kinetic energy higher by the same amount, its "
         "attraction lower by zero point zero seven seven, and its repulsion higher by zero point zero one eight: "
         "less screening, exactly as the review says."),
    ]


class S141T5(Walk):
    TITLE = "Test T5: H₂ in a minimal basis, closed forms against PySCF"
    SUBTITLE = "STO-3G, R in bohr; RHF, 2×2 CI, triplet and open-shell singlet"
    SYMBOLS = (r"`E_rhf`$=2h_{11}+J_{11}$, `E_ci`: lower root of the 2×2 CI, `E_T`$=h_{11}+h_{22}+J_{12}-K_{12}$, "
               r"`E_OSS`$=\dots+K_{12}$, each plus $V_{nn}$ — $2E(\text{H})$: two separate hydrogen atoms in the same basis")
    STEPS = [
        ("code", "t03_t05_hund_virial_h2.py", 83, 113, [
            ([0, 1, 2, 3, 4, 5, 6, 7],
             "Test T five. At each distance, restricted Hartree Fock in STO three G gives the two molecular orbitals; "
             "the one- and two-electron integrals are transformed to them."),
            ([8, 9, 10, 11, 12],
             "The closed forms of chapter seven: the RHF energy, the lower root of the two by two CI, the triplet and "
             "the open-shell singlet."),
            ([13, 14, 15, 16, 17],
             "Each is compared with PySCF: RHF, full CI, and a separate restricted open-shell triplet calculation; and "
             "the integrals that symmetry should kill, h one two and the mixed repulsion, are checked to vanish."),
            ([18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             "It runs at one point four, three, six and twenty bohr, and at twenty checks the limits: CI and the "
             "triplet reach two hydrogen atoms, and RHF stays more than zero point two hartree too high."),
        ]),
        ("out", "t03_t05_hund_virial_h2.txt", 6, 12,
         "All closed forms agree with PySCF at every distance. At twenty bohr, CI and the triplet equal two hydrogen "
         "atoms, minus zero point nine three three one six four hartree, while RHF is zero point three six two three "
         "too high, which is exactly K one two. T three to T five pass."),
    ]


class S142T6T7(Walk):
    TITLE = "Tests T6 and T7: the gap model and kinetic exchange"
    SUBTITLE = "SymPy limits and series; PySCF full CI for the extended Hubbard dimer"
    SYMBOLS = (r"`Hs`: the 2×2 closed-shell matrix of the two-orbital model — `ratio`: $c_2/c_1$ — `series`: Taylor "
               r"expansion in $t$ — extended Hubbard: on-site $U$, inter-site $V$, exchange $k$, hopping $t$")
    STEPS = [
        ("code", "t06_t09_models.py", 17, 30, [
            ([0, 1, 2, 3, 4, 5, 6],
             "Test T six, the two-orbital gap model of chapter seven. SymPy builds the two by two matrix of the closed "
             "shells, checks that J d minus the square root of delta squared plus K squared is an eigenvalue, and forms "
             "the singlet-triplet gap."),
            ([7, 8, 9, 10, 11, 12, 13],
             "The coefficient ratio c two over c one is computed exactly, and its limits are taken: as delta goes to "
             "zero it must tend to minus one, a pure diradical; as delta goes to infinity, to zero, a closed shell."),
        ]),
        ("code", "t06_t09_models.py", 62, 91, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
             "Test T seven, kinetic exchange. The covalent and symmetric ionic configurations form a two by two block; "
             "its lower root must be the formula of chapter eight, and the Taylor series of the gap, with V and k zero, "
             "must start with minus four t squared over U."),
            ([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
             "Then numbers: t one, U six, V one and a half, k zero point two, as integrals for PySCF full CI. The lowest "
             "singlet and the triplet must match the formulas."),
            ([24, 25, 26, 27, 28, 29],
             "And the exact-diagonalisation engine used for the molecules later is cross-checked on the dimer, against "
             "one half of U minus the square root of U squared plus sixteen."),
        ]),
        ("out", "t06_t09_models.txt", 1, 3,
         "The output: the gap is J d minus J x plus K minus the square root; the ratio tends to minus one and zero; the "
         "Hubbard series is exactly minus four t squared over U; and full CI and the engine agree."),
    ]


class S143T8(Walk):
    TITLE = "Test T8: Hückel NBMOs, pairing, counting and disjointness"
    SUBTITLE = "NumPy on seven π graphs"
    SYMBOLS = (r"`A`: adjacency matrix — `nz`: number of zero eigenvalues, NBMOs — `T`: maximum matching — "
               r"$\min_\theta\sum_ia_i^2b_i^2$: smallest overlap over all rotations of the NBMO pair — Longuet-Higgins: "
               r"$\#\text{NBMO}\ge N-2T\ge|n_A-n_B|$")
    STEPS = [
        ("code", "t06_t09_models.py", 93, 122, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
             "Test T eight works on seven pi graphs, written as lists of bonds: square cyclobutadiene, T M M, T M E, "
             "meta xylylene, trimethylenebenzene, tetramethylenebenzene and para xylylene."),
            ([13, 14, 15, 16, 17, 18, 19, 20, 21],
             "bipartition stars every other atom by a graph search, and returns nothing if two neighbours get the same "
             "colour, which would mean an odd ring."),
            ([23, 24, 25, 26, 27, 28, 29],
             "max matching finds the largest set of bonds sharing no atom, by trying subsets from the largest down."),
        ]),
        ("code", "t06_t09_models.py", 124, 148, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             "For each molecule: diagonalise the adjacency matrix, count the zero eigenvalues, star the atoms, and find "
             "the maximum matching."),
            ([10, 11, 12],
             "Pairing: the sorted eigenvalues must equal their negatives. Zero sum: the adjacency matrix times every "
             "NBMO must vanish, which is the zero-sum rule."),
            ([13, 14, 15, 16, 17, 18, 19],
             "For a pair of NBMOs it rotates them through every angle, twenty thousand steps, and finds the smallest "
             "sum of a i squared b i squared: zero means disjoint."),
            ([20, 21, 22, 23, 24],
             "And the Longuet-Higgins bound is checked as a lower bound, with the inequality we had first wrongly "
             "assumed to be an equality."),
        ]),
        ("out", "t06_t09_models.txt", 4, 11,
         "The output: cyclobutadiene has two NBMOs although N minus two T is zero; its pair can be made disjoint, to "
         "two times ten to the minus nine. T M E is disjoint; T M M and meta xylylene are not, with minimum overlaps "
         "one sixth and one sixteenth. Pairing and zero sum hold for all seven."),
    ]


class S144T9(Walk):
    TITLE = "Test T9: exact Hubbard diagonalisation, spins and spin density"
    SUBTITLE = "a fermionic exact-diagonalisation engine written for this check"
    SYMBOLS = (r"bit strings: occupation of each site by ↑ or ↓ electrons — Jordan–Wigner sign: $(-1)^{\#\text{electrons "
               r"passed}}$ when an electron hops — $S_{gs}$: largest $S_z$ whose lowest level equals the ground energy")
    STEPS = [
        ("code", "t06_t09_models.py", 33, 60, [
            ([0, 1, 2, 3, 4, 5, 6],
             "The engine. States are pairs of bit strings, one for the up electrons and one for the down electrons, "
             "with fixed numbers of each."),
            ([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
             "Hopping moves an electron along a bond if the target site is empty, with the fermionic sign: minus one to "
             "the number of electrons it passes over. Each hop contributes minus t."),
            ([18, 19, 20, 21, 22],
             "The full Hamiltonian is the up hopping times the identity, plus the identity times the down hopping, plus "
             "U times the number of doubly occupied sites."),
            ([24, 25, 26, 27],
             "Small matrices are diagonalised densely, larger ones with a sparse solver to ten to the minus twelve."),
        ]),
        ("code", "t06_t09_models.py", 150, 183, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
             "Test T nine. At half filling and U equal to three, it finds the lowest energy in every S z sector. The "
             "ground-state spin is the largest S z whose lowest level equals the overall minimum, and it must equal "
             "Ovchinnikov's count."),
            ([18, 19, 20, 21, 22, 23, 24, 25, 26],
             "Then the pentadienyl radical: five sites, three up and two down. The spin density on each site is the "
             "probability-weighted difference of up and down occupations, and it must alternate in sign."),
            ([27, 28, 29, 30, 31, 32, 33],
             "At U equal to zero the unstarred sites must carry exactly zero spin density, the Hückel result."),
        ]),
        ("out", "t06_t09_models.txt", 12, 20,
         "All seven molecules have exactly the spin Ovchinnikov's rule predicts, including spin three halves for "
         "trimethylenebenzene. The pentadienyl spin densities are one third and zero at U equal to zero, and plus zero "
         "point four five, minus zero point one eight, plus zero point four six at three t: alternating, summing to "
         "one."),
    ]


class S145T9b(Walk):
    TITLE = "Test T9b: how the gap grows with U"
    SUBTITLE = "first order for nondisjoint NBMOs, second order for disjoint ones"
    SYMBOLS = (r"lowest singlet: the lowest $S_z=0$ level that is not also an $S_z=1$ level — exponent $p$: slope of "
               r"$\log|\text{gap}|$ against $\log U$ — `polyfit`: least-squares straight line")
    STEPS = [
        ("code", "t09b_t15_correlation.py", 12, 42, [
            ([0, 1, 2, 3, 4, 5, 6],
             "Test T nine b reuses the exact-diagonalisation engine, cut straight out of the T nine file so that both "
             "tests run the same code."),
            ([8, 9, 10, 11, 12],
             "Four graphs: cyclobutadiene and T M E, disjoint, and T M M and meta xylylene, nondisjoint."),
            ([13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
             "At U equal to zero point zero five, zero point one and zero point two, it computes the triplet energy, "
             "and the lowest singlet as the lowest S z zero level that is not also an S z one level, since those "
             "belong to triplets."),
            ([25, 26, 27, 28, 29, 30],
             "The exponent is the slope of the log of the gap against the log of U. It must be two, within zero point "
             "one five, with the singlet lower for disjoint graphs, and one, with the triplet lower, for nondisjoint "
             "ones."),
        ]),
        ("out", "t09b_t15_correlation.txt", 1, 5,
         "The fitted exponents: one point nine seven for cyclobutadiene and one point nine five for T M E, singlets "
         "lower; zero point nine seven for T M M and zero point nine six for meta xylylene, triplets lower. Exactly "
         "the first-order and second-order behaviour derived in chapters nine and ten."),
    ]


class S146T10T12T13(Walk):
    TITLE = "Tests T10, T12, T13: three symbolic identities"
    SUBTITLE = "SymPy: the HOMO difference, the 3d/4s identity, and the angular-momentum commutators"
    SYMBOLS = (r"`binomial(n, 2)`: number of pairs — `expand_func`: write binomials as polynomials — `f`: an arbitrary "
               r"function of all six coordinates — `l1`, `l2`: $-i\,\mathbf r_i\times\nabla_i$")
    STEPS = [
        ("code", "t10_t12_t13_symbolic.py", 9, 46, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             "Test T ten: with symbols for h a, h b, J and K, the triplet and open-shell singlet energies and the ion's "
             "energy give the two HOMO energies, and their difference must equal the gap, two K."),
            ([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
             "Test T twelve: the average energy of a configuration with binomial pair counts; delta and the two orbital "
             "energies of chapter thirteen; and the identity delta equals epsilon d minus epsilon s plus J bar d d "
             "minus J bar d s, with both orbital energies in closed form."),
            ([28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
             "It also checks the ion analogue, and evaluates the illustrative numbers: epsilon d below epsilon s, yet "
             "delta positive."),
        ]),
        ("code", "t10_t12_t13_symbolic.py", 48, 73, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
             "Test T thirteen: the coordinates of both electrons, an arbitrary function f of all six, and the angular "
             "momentum operators of each electron, minus i r cross gradient, component by component."),
            ([14, 15, 16, 17, 18, 19],
             "The commutator of l one with one over r one two, acting on f, must be non-zero; the commutator of the total "
             "L must vanish for all three components."),
            ([20, 21, 22, 23, 24, 25],
             "And the square of l one does not commute with the repulsion either, so even the one-electron l squared is "
             "not conserved."),
        ]),
        ("out", "t10_t12_t13_symbolic.txt", 1, 9,
         "The output: the gap equals the HOMO difference, two K; the three d four s identity holds, with epsilon d "
         "minus one point five, epsilon s minus zero point nine and delta plus zero point one in the example; the l "
         "one z commutator is exactly the cross-term expression of chapter thirteen; and the total commutes."),
    ]


class S147T11a(Walk):
    TITLE = "Test T11a: ROHF stationarity and canonicalisation"
    SUBTITLE = "ROHF/6-31G∗ on four ordinary radicals"
    SYMBOLS = (r"`schemes`: weights $A$ for the core, open and virtual diagonal blocks — `canonical_energies`: "
               r"eigenvalues of each block of $A\mathbf F^\alpha+(1-A)\mathbf F^\beta$ — $A^*$: weight where the SOMO "
               r"crosses the closed HOMO")
    STEPS = [
        ("code", "t11_rohf_and_distonic.py", 26, 72, [
            ([0, 1, 2, 3, 4, 5, 6],
             "Test T eleven a. canonical energies builds each diagonal block as a weighted combination of the alpha and "
             "beta Fock matrices and returns its eigenvalues, the orbital energies under that convention."),
            ([8, 9, 10, 11, 12, 13],
             "Four conventions are tried, from PySCF's default average to alpha-like and beta-like open blocks."),
            ([14, 15, 16, 17, 18, 19, 20],
             "Four radicals: H two N O, N O two, methyl and allyl, all with restricted open-shell Hartree Fock in six "
             "thirty one G star."),
            ([21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
             "For each, the stationarity blocks must vanish and the free blocks must not, as in chapter sixteen. Then "
             "for every convention it compares the SOMO with the highest closed orbital."),
            ([36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46],
             "Since the open block is one-dimensional, the SOMO energy is linear in the weight A, so the script solves "
             "for the crossing weight A star and verifies that the order flips exactly there, and that A star exceeds "
             "one."),
        ]),
        ("note", "H₂NO: $E=-130.36970936\\,E_{\\mathrm h}$; required blocks $7.9\\times10^{-8}$, $4.1\\times10^{-8}$, "
                 "$5.3\\times10^{-8}$; free blocks 0.113 and 0.164; SOMO from $+0.2028$, open block $=\\mathbf F^\\beta$, "
                 "to $-0.4397$, open block $=\\mathbf F^\\alpha$, against the closed HOMO at $-0.4666$; in every "
                 "convention tried the SOMO stays above the HOMO",
         "From the recorded log, for H two N O: the energy minus one hundred and thirty point three six nine seven zero "
         "nine three six hartree; the required blocks around five to eight times ten to the minus eight; the free "
         "blocks zero point one one and zero point one six. The SOMO runs from plus zero point two zero, with the beta "
         "open block, to minus zero point four four, with the alpha one, while the closed HOMO stays at minus zero "
         "point four seven. No convention in the natural range puts the SOMO below it.", "checked"),
    ]


class S148T11b(Walk):
    TITLE = "Test T11b: the distonic anion with B3LYP — a recorded failure"
    SUBTITLE = "UB3LYP/6-31+G∗ geometry optimisation, then vertical oxidation"
    SYMBOLS = (r"SMILES: a line notation for molecules — `optimize`: geometry optimisation with geomeTRIC — "
               r"IE: vertical ionisation energy to the triplet diradical, `dT`, or the closed shell, `dCS`, in eV")
    STEPS = [
        ("code", "t11_rohf_and_distonic.py", 75, 121, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
             "Test T eleven b, the distonic radical anion. build turns a SMILES string into three-dimensional "
             "coordinates with RDKit, and uks sets up unrestricted B three L Y P with a tight convergence threshold."),
            ([11, 12, 13, 14, 15],
             "Two systems: a nitroxide with a remote carboxylate, as the anion and as the protonated acid."),
            ([17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
             "For each: optimise the radical's geometry, then find the SOMO as the occupied alpha orbital with the "
             "largest overlap with the spin density, and see where it sits among the occupied orbitals."),
            ([32, 33, 34, 35, 36, 37, 38, 39, 40, 41],
             "Then the two oxidised states at the same geometry: the triplet diradical, and the closed shell, and their "
             "ionisation energies in electron volts."),
            ([42, 43, 44, 45, 46],
             "The test demands the pH switch: the anion oxidises to the diradical, and the acid to the closed shell."),
        ]),
        ("note", "anion: SOMO 3 levels below the α-HOMO, non-aufbau, ε = −2.40 vs −1.62 eV; acid: SOMO = HOMO. But "
                 "B3LYP puts the anion's closed-shell product lower by 0.07 eV: the switch is missed, and T11 is "
                 "recorded as FAIL",
         "The log shows the orbitals behave as the review says: in the anion the SOMO lies three levels below the "
         "alpha HOMO, while in the acid it is the HOMO. But with B three L Y P the anion's closed-shell product comes "
         "out lower, by seven hundredths of an electron volt, so the switch is missed. T eleven b is recorded as a "
         "failure, unedited, and it led to test T eleven c.", "erratum"),
    ]


class S149T11c(Walk):
    TITLE = "Test T11c: two radicals, two protonation states, two functionals"
    SUBTITLE = "the follow-up to T11b, and its own checking script"
    SYMBOLS = (r"TEMPO-4-COO⁻: the anion of a TEMPO carboxylic acid — `--reuse-geom`: resume without re-optimising — "
               r"`somo_rank_from_top`: how many occupied α orbitals lie above the SOMO — `t11c_check.py`: parses the logs")
    STEPS = [
        ("code", "t11c_distonic_functionals.py", 18, 39, [
            ([0, 1, 2, 3, 4, 5, 6],
             "Test T eleven c asks whether T eleven b's verdict depends on the functional and on the distance between "
             "the radical and the anion. Four systems: the short nitroxide and a TEMPO carboxylate, each as anion and "
             "acid; and two functionals, B three L Y P and range-separated CAM B three L Y P."),
            ([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
             "Geometries are optimised in six thirty one G star and saved, so that interrupted runs can resume; the "
             "energies are then computed with diffuse functions, six thirty one plus G star."),
        ]),
        ("code", "t11c_distonic_functionals.py", 65, 84, [
            ([0, 1, 2, 3, 4],
             "For every system and functional: the radical, its oxidised triplet, and its oxidised closed shell."),
            ([5, 6, 7, 8, 9],
             "The SOMO's rank among the occupied orbitals is found from the spin density, as before."),
            ([10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
             "And the two ionisation energies, their difference, the SOMO rank and the triplet's S squared are written "
             "to the log and to a JSON file."),
        ]),
        ("code", "t11c_check.py", 47, 71, [
            ([0, 1, 2],
             "The DFT runs took hours and were resumed several times, so a separate script, t eleven c check, parses "
             "every log and checks the claims without re-running anything: all eight runs present;"),
            ([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
             "the differences consistent; the triplets clean, with S squared within zero point zero five of two; the "
             "acids aufbau and the anions non-aufbau; the acids oxidising to closed shells; and with CAM B three L Y P "
             "the anions oxidising to diradicals."),
            ([15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
             "The B three L Y P anions are reported as a finding, not hidden; and the numbers copied into the slides' "
             "data file are checked against the logs to a thousandth of an electron volt."),
        ]),
        ("out", "t11c_check.txt", 1, 21,
         "The result: every check passes. CAM B three L Y P reproduces the pH switch, with differences of minus zero "
         "point three six and minus zero point three zero electron volts for the anions; B three L Y P gives plus zero "
         "point zero seven and plus zero point zero seven; and the slide data match the logs. T eleven c passes."),
    ]


class S150T14(Walk):
    TITLE = "Test T14: broken-symmetry UHF and the Yamaguchi projection"
    SUBTITLE = "self-consistent BS-UHF for the half-filled Hubbard dimer"
    SYMBOLS = (r"`na`, `nb`: α and β occupations of the two sites — `Fa`, `Fb`: UHF Fock matrices, mean-field $U\,n$ on "
               r"the diagonal — damping: mixing half of the new densities — $J=\tfrac12(E_S-E_T)$, exact")
    STEPS = [
        ("code", "t06_t09_models.py", 185, 209, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             "Test T fourteen. Broken-symmetry unrestricted Hartree Fock for the half-filled Hubbard dimer: start with "
             "the alpha electron mostly on site one and the beta electron mostly on site two, build the mean-field Fock "
             "matrices, and iterate with damping until the densities stop changing."),
            ([10, 11, 12],
             "The energy subtracts the double-counted repulsion, and S squared is one minus the overlap of the alpha and "
             "beta orbitals squared, the formula of chapter fifteen."),
            ([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
             "Then Yamaguchi's formula with the exact triplet as the high-spin reference, against the exact coupling, "
             "at U equal to three, six, twelve and twenty four; for U of twelve and above, the error must be under "
             "fifteen percent."),
        ]),
        ("out", "t06_t09_models.txt", 21, 26,
         "The output: at U equal to three t, S squared of the broken-symmetry state is zero point five six and "
         "Yamaguchi's J is minus zero point four six, against the exact minus zero point five, an error of seven point "
         "seven percent; at six t, zero point nine percent; at twelve t, a tenth of a percent; at twenty four t, "
         "essentially exact."),
    ]


class S151T15(Walk):
    TITLE = "Test T15: same-spin against opposite-spin correlation"
    SUBTITLE = "MP2/cc-pVTZ for three molecules, and exact helium"
    SYMBOLS = (r"`e_corr_ss`, `e_corr_os`: MP2 correlation energy of same-spin and opposite-spin pairs — per pair: divided "
               r"by $2\binom{n}{2}$ and $n^2$ for $n$ doubly occupied orbitals — $E_{\text{corr}}=E_{\text{exact}}-E_{\text{HF}}$")
    STEPS = [
        ("code", "t09b_t15_correlation.py", 44, 75, [
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
             "Test T fifteen checks the claim that same-spin correlation is an order of magnitude smaller. First, "
             "second-order perturbation theory in the cc p V T Z basis for water, nitrogen and ethylene, split into "
             "same-spin and opposite-spin parts, in total and per pair."),
            ([17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
             "Then helium, where both pair types can be compared exactly: the one one S ground state is one opposite-spin "
             "pair, and the two three S state one same-spin pair. Each correlation energy is the exact benchmark energy "
             "minus Hartree Fock."),
        ]),
        ("out", "t09b_t15_correlation.txt", 6, 11,
         "For the molecules, the same-spin share per pair is zero point three to zero point four three of the opposite-"
         "spin share, not a tenth. For helium the ratio is zero point zero two three, well below a tenth. So the claim "
         "holds for compact two-electron systems and is overstated in general."),
    ]


class S152T16(Frame):
    """T16: citations, checked by hand."""

    TITLE = "Test T16: the citations, by hand"

    def construct(self) -> None:
        self.setup_frame()
        body = boxed("every reference used in the derivations and the slides was looked up in the publisher's record: "
                     "authors, journal, volume, first page and year. One error found: Katriel & Pauncz, *Adv. Quantum "
                     "Chem.* 10, 143, is from 1977, not 1975 as the review's reference 11 says. The access status of each "
                     "source, full text, abstract only or not accessed, is listed in section 17 of the derivations.",
                     "checked", width=12.0, size=30, tag="T16, no script").move_to([0, 0.4, 0])
        self.say("[Test T sixteen has no script. Every reference used in the derivations and the slides was looked up "
                 "in the publisher's record: authors, journal, volume, first page and year.] [One error turned up: "
                 "Katriel and Pauncz, Advances in Quantum Chemistry volume ten, page one hundred and forty three, is from "
                 "nineteen seventy seven, not nineteen seventy five as the review's reference eleven says. And the access "
                 "status of every source is listed in section seventeen of the derivations.]",
                 m.FadeIn(body), m.Indicate(body))
        self.wait(0.5)
