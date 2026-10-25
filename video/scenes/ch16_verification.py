"""Chapter 16: our verification machinery (presentation/sections/18-verification.tex)."""
import manimgx as m

from noir import (CYAN, FG, GOLD, GREEN, MUTED, ROSE, Box, Frame, M, boxed, bullets, excerpt, pill, rich, table_rows)

TREE = [("CH5103_Term_Paper/", ""), ("  paper/", "the review, PDF"), ("  derivations/", "18 LaTeX sections"),
        ("  verification/", "T1–T15 scripts, logs, results/"), ("    lean_proofs/", "Lean 4 + Mathlib, T17"),
        ("  assets/", "figures, captions, JSONL"), ("  presentation/", "the slide deck"),
        ("  docs/", "findings, test matrix"), ("  plans/", "working log, audit"), ("  site/", "web page, GitHub Pages"),
        ("  video/", "this video: scenes, narration, editor"),
        ("  pyproject.toml, uv.lock", "pinned environment"), ("  Makefile", "one command per artefact")]

MAKE = [("make sync", "uv, locked env"), ("make verify", "T1–T15 > results/"), ("make verify-dft", "T11, T11c"),
        ("make lean", "T17"), ("make derivations", ""), ("make figures", "byte-identical")]


def mono(text: str, size: float = 24, colour: str = FG) -> m.Mobject:
    return rich(f"`{text}`", size, colour)


class S123Repository(Frame):
    """18-verification.tex, frame 1: 'The repository'."""

    TITLE = "The repository"

    def construct(self) -> None:
        self.setup_frame()
        rows = m.VGroup()
        y = 2.05
        for name, what in TREE:
            indent = len(name) - len(name.lstrip())
            left = rich(f"`{name.strip()}`", 27, GOLD if indent == 0 else FG)
            left.move_to([-6.5 + 0.22 * indent + left.width / 2, y - left.height / 2, 0])
            row = m.VGroup(left)
            if what:
                row.add(rich(what, 24, MUTED).move_to([-2.1, left.get_center()[1], 0], aligned_edge=m.LEFT))
            rows.add(row)
            y -= left.height + 0.12
        mk = m.VGroup(*[m.VGroup(mono(c, 29), rich(f"# {w}", 24, MUTED) if w else m.VGroup()).arrange(m.RIGHT, buff=0.3)
                        for c, w in MAKE]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.14)
        panel = Box(mk, "plain").move_to([4.0, 0.85, 0])
        env = rich("Python 3.12 pinned by `uv.lock` · PySCF 2.14, SymPy 1.14 · Lean 4.29.1, Mathlib 4.29.1", 25,
                   width=5.4).next_to(panel, m.DOWN, buff=0.35)
        self.say("[Part seventeen: our verification. Everything is in one repository. The paper itself; eighteen LaTeX "
                 "sections of derivations; the verification scripts, tests one to fifteen, with their logs and results; "
                 "the Lean proofs; the review's figures and captions; the slide deck; documentation of the findings and "
                 "the test matrix; our working plans and audit; the web page; and this video, with its scenes, narration "
                 "and editor.]", m.FadeIn(rows))
        self.say("[Each artefact is one command. make sync builds the locked environment with uv; make verify runs tests "
                 "one to fifteen into the results folder; make verify d f t runs the density functional tests; make lean "
                 "checks the proofs; and make figures regenerates the figures byte for byte.]", m.FadeIn(panel))
        self.say("[Python three point one two is pinned by the lock file, with PySCF two point one four and SymPy one point "
                 "one four; and Lean four point two nine point one with the matching Mathlib.]", m.FadeIn(env))
        self.wait(0.4)


MATRIX1 = [("T1", r"spin functions, Fig. 1 combinations, sign erratum", "SymPy"),
           ("T1b", r"sign erratum again: $\hat S^2$ on numerical tensors", "NumPy"),
           ("T2", r"$2e/2o$ Hamiltonian vs full CI, 5 random sets", "PySCF FCI"),
           ("T3", r"$K_{pq}\ge0$, $J_{pq}\ge K_{pq}$", "RHF/6-31G H₂O"),
           ("T4", r"He $2\,^3S/2\,^1S$: virial, less screening", "exact 2-electron"),
           ("T5", r"H₂ dissociation limits", "STO-3G closed forms"),
           ("T6", r"two-orbital gap model", "SymPy"),
           ("T7", r"kinetic exchange, extended dimer", "SymPy + FCI"),
           ("T8", r"Hückel NBMO rules, disjointness", "NumPy"),
           ("T9", r"Ovchinnikov/Lieb spins; spin alternation", "exact diagonalisation")]

MATRIX2 = [("T9b", r"gap $\propto U$ vs $\propto U^2$", "exact diagonalisation", "pass"),
           ("T10", r"S–T gap = HOMO difference", "SymPy", "pass"),
           ("T11a", r"ROHF stationarity, canonicalisation", "ROHF/6-31G∗", "pass"),
           ("T11b", r"distonic anion, B3LYP", "UB3LYP ΔSCF", "fail"),
           ("T11c", r"distonic anions/acids, two functionals", "UKS ΔSCF; `t11c_check.py`", "pass"),
           ("T12", r"3d/4s identity", "SymPy", "pass"),
           ("T13", r"$[\hat l_1,r_{12}^{-1}]\neq0$, $[\hat L,r_{12}^{-1}]=0$", "SymPy", "pass"),
           ("T14", r"Yamaguchi projection", "BS-UHF dimer", "pass"),
           ("T15", r"same- vs opposite-spin correlation", "MP2, He", "pass"),
           ("T17", r"17 algebraic theorems", "Lean 4 + Mathlib", "pass")]


def matrix(rows, size: float = 25) -> m.VGroup:
    """The test matrix as a grid: test id, what, method, result pill; returns rows (header first)."""
    head = m.VGroup(rich("**test**", size, GOLD), rich("**what**", size, GOLD), rich("**method**", size, GOLD),
                    rich("**result**", size, GOLD))
    body = []
    for r in rows:
        tid, what, method = r[:3]
        res = r[3] if len(r) > 3 else "pass"
        body.append(m.VGroup(rich(tid, size, CYAN), rich(what, size, width=6.4), rich(method, size, MUTED),
                             pill(res, size=26)))
    allrows = [head, *body]
    xs = [-6.3, -5.1, 1.55, 5.35]
    y = 2.05
    for row in allrows:
        h = max(c.height for c in row)
        for c, x in zip(row, xs):
            c.move_to([x + c.width / 2, y - h / 2, 0])
        y -= h + 0.13
    rule = m.Line([-6.3, allrows[0].get_bottom()[1] - 0.06, 0], [6.5, allrows[0].get_bottom()[1] - 0.06, 0],
                  color=MUTED, stroke_width=1.5)
    allrows[0].add(rule)
    return m.VGroup(*allrows)


class S124Matrix1(Frame):
    """18-verification.tex, frame 2: 'The test matrix (1/2)'."""

    TITLE = "The test matrix, part 1"
    SYMBOLS = (r"SymPy: exact symbolic algebra — PySCF: quantum-chemistry package — FCI: full configuration interaction, "
               r"exact in the basis — RHF: restricted HF — 6-31G, STO-3G: basis sets — exact diagonalisation: all "
               r"eigenstates of a model Hamiltonian")

    def construct(self) -> None:
        self.setup_frame()
        g = matrix(MATRIX1)
        self.say("[Here is the test matrix. Each test names what it checks, how, and the result.]", m.FadeIn(g[0]))
        self.say("[T one checks the spin functions and the combinations of Figure one, including the sign erratum, in "
                 "SymPy. T one b checks the sign erratum again, numerically, by applying S squared to wavefunction "
                 "tensors in NumPy.]", m.AnimationGroup(m.FadeIn(g[1]), m.FadeIn(g[2])))
        self.say("[T two compares the two-electron two-orbital Hamiltonian with PySCF full configuration interaction for "
                 "five random integral sets. T three checks that no exchange integral is negative and none exceeds "
                 "the Coulomb integral, for water.]", m.AnimationGroup(m.FadeIn(g[3]), m.FadeIn(g[4])))
        self.say("[T four solves helium's one s two s states exactly and checks the virial theorem and less screening. T "
                 "five checks the dissociation limits of H two.]", m.AnimationGroup(m.FadeIn(g[5]), m.FadeIn(g[6])))
        self.say("[T six checks the two-orbital gap model, and T seven kinetic exchange in the extended Hubbard dimer, "
                 "symbolically and against full configuration interaction.]",
                 m.AnimationGroup(m.FadeIn(g[7]), m.FadeIn(g[8])))
        self.say("[T eight checks the Hückel rules for non-bonding orbitals and disjointness, and T nine the spins "
                 "predicted by Ovchinnikov and Lieb, and spin alternation, by exact diagonalisation. All pass.]",
                 m.AnimationGroup(m.FadeIn(g[9]), m.FadeIn(g[10])))
        self.wait(0.4)


class S125Matrix2(Frame):
    """18-verification.tex, frame 3: 'The test matrix (2/2)'."""

    TITLE = "The test matrix, part 2"
    SYMBOLS = (r"ΔSCF: energy difference of two separate SCF calculations — UKS: unrestricted Kohn–Sham DFT — MP2: "
               r"second-order perturbation theory — BS-UHF: broken-symmetry unrestricted HF")

    def construct(self) -> None:
        self.setup_frame()
        g = matrix(MATRIX2, size=24)
        note = rich("T11b fails as recorded: B3LYP misses the crossover by 0.06–0.07 eV; T11c shows the outcome depends on "
                    "the functional. T16, citations checked by hand against publisher records, has no script.", 22, MUTED,
                    width=12.6).next_to(g, m.DOWN, buff=0.2)
        self.say("[The second half. T nine b measures how the gap grows with U. T ten checks that the singlet-triplet gap "
                 "is a HOMO difference.]", m.AnimationGroup(m.FadeIn(g[0]), m.FadeIn(g[1]), m.FadeIn(g[2])))
        self.say("[T eleven a checks the stationarity conditions of restricted open-shell Hartree Fock.] [T eleven b, the "
                 "distonic anion with B three L Y P, fails, and we report it as it is.] [T eleven c repeats it for two radicals, "
                 "two protonation states and two functionals, with its own checking script, and passes.]",
                 m.FadeIn(g[3]), m.FadeIn(g[4]), m.FadeIn(g[5]))
        self.say("[T twelve checks the three d four s identity, T thirteen the angular momentum commutators, T fourteen "
                 "the Yamaguchi projection, and T fifteen same-spin against opposite-spin correlation.]",
                 m.AnimationGroup(*[m.FadeIn(g[k]) for k in (6, 7, 8, 9)]))
        self.say("[T seventeen is the Lean file: seventeen algebraic theorems, machine-checked.]", m.FadeIn(g[10]))
        self.say("[T eleven b fails as recorded: B three L Y P misses the crossover by six to seven hundredths of an electron "
                 "volt, and T eleven c shows that the outcome depends on the functional. T sixteen, the citations, were "
                 "checked by hand against publisher records, so it has no script.]", m.FadeIn(note))
        self.wait(0.4)


class S126InsideT4(Frame):
    """18-verification.tex, frame 4: 'Inside T4: helium, exact in a 16s7p4d basis'."""

    TITLE = "Inside T4: helium, exact in a 16s7p4d basis"
    SUBTITLE = "verification/t03_t05_hund_virial_h2.py, lines 42–62, unedited"
    SYMBOLS = (r"symmetric $C$ ↔ singlet, antisymmetric $C$ ↔ triplet, Part III — `C[p,q]`: coefficient of "
               r"$\phi_p(1)\phi_q(2)$ — `h`, `T`, `V`: one-electron, kinetic, nuclear matrices — `eri`: $(pq|rs)$ — `B`: "
               r"basis of (anti)symmetric pairs — `Tex`, `Vne`, `Vee`: virial components")

    def construct(self) -> None:
        self.setup_frame()
        c = excerpt("verification/t03_t05_hund_virial_h2.py", 42, 62, width=12.8, height=4.9).move_to([0, -0.1, 0])
        L = c.code_lines
        self.say("[Inside test T four. This is the actual code, unedited. The two-electron wavefunction is expanded in "
                 "pairs of basis functions, phi p of electron one times phi q of electron two, with a coefficient matrix "
                 "C.]", m.AnimationGroup(m.FadeIn(c.background), m.FadeIn(c.line_numbers), m.FadeIn(L[0])))
        self.say("[The Hamiltonian in this pair space is h for electron one, h for electron two, and the repulsion "
                 "integral, assembled with einsum and reshaped into a matrix.]",
                 m.AnimationGroup(*[m.FadeIn(L[k]) for k in (1, 3, 4, 5)]))
        self.say("[For the singlet, C must be symmetric; for the triplet, antisymmetric, because the spin factor carries "
                 "the other symmetry. The loop builds a basis of symmetric or antisymmetric pairs.]",
                 m.AnimationGroup(*[m.FadeIn(L[k]) for k in (2, *range(6, 12))]))
        self.say("[The Hamiltonian projected onto that basis is diagonalised. For the singlet the second root is the one s "
                 "two s state; for the triplet it is the lowest.]",
                 m.AnimationGroup(*[m.FadeIn(L[k]) for k in range(12, 15)]))
        self.say("[Then the kinetic, nuclear attraction and repulsion energies are computed from C, and the code asserts "
                 "that they add up to the eigenvalue, to ten to the minus eight.] These are the numbers behind the virial "
                 "analysis of Hund's rule.", m.AnimationGroup(*[m.FadeIn(L[k]) for k in range(15, len(L))]))
        self.wait(0.4)


class S127InsideT11a(Frame):
    """18-verification.tex, frame 5: 'Inside T11a: ROHF Fock blocks'."""

    TITLE = "Inside T11a: ROHF Fock blocks"
    SUBTITLE = "verification/t11_rohf_and_distonic.py, lines 14–24 and 51–54"
    SYMBOLS = (r"`Fa`, `Fb`: $\mathbf F^\alpha,\mathbf F^\beta$ in the MO basis — `c`, `o`, `v`: core, open, virtual indices "
               r"— `g_*`: blocks that must vanish — `n_*`: blocks free to be non-zero")

    def construct(self) -> None:
        self.setup_frame()
        c1 = excerpt("verification/t11_rohf_and_distonic.py", 14, 24, width=12.4, height=3.1).move_to([0, 0.75, 0])
        c2 = excerpt("verification/t11_rohf_and_distonic.py", 51, 54, width=12.4, height=1.25)
        c2.next_to(c1, m.DOWN, buff=0.25)
        note = rich("UHF Fock matrices from the ROHF densities, then the blocks the stationarity table says must vanish", 26,
                    MUTED).next_to(c2, m.DOWN, buff=0.2)
        self.say("[Inside test T eleven a. Run restricted open-shell Hartree Fock to tight convergence, and take its "
                 "density matrices.]", m.AnimationGroup(m.FadeIn(c1.background), m.FadeIn(c1.line_numbers), *[m.FadeIn(c1.code_lines[k]) for k in range(0, 4)]))
        self.say("[Build the alpha and beta Fock matrices from those densities, as unrestricted Hartree Fock would, and "
                 "transform them to the molecular orbital basis. Then sort the orbitals into core, open and virtual by "
                 "their occupations.]", m.AnimationGroup(*[m.FadeIn(c1.code_lines[k]) for k in range(4, len(c1.code_lines))]))
        self.say("[The blocks the stationarity table says must vanish, beta core open, alpha open virtual, and the alpha "
                 "plus beta core virtual sum, must be below ten to the minus five; while the blocks the table leaves free "
                 "must be clearly non-zero, above ten to the minus three, to show the test can tell them apart.]",
                 m.AnimationGroup(m.FadeIn(c2), m.FadeIn(note)))
        self.wait(0.4)


class S128InsideT17(Frame):
    """18-verification.tex, frame 6: 'Inside T17: Lean proves the less-screening logic'."""

    TITLE = "Inside T17: Lean proves the less-screening logic"
    SUBTITLE = "verification/lean_proofs/Ch5103/Identities.lean, lines 72–83"
    SYMBOLS = (r"`dT`, `dVne`, `dVee`, `dE`: triplet minus singlet — `hvir`: virial theorem for both states — `linarith`: "
               r"proves linear inequalities automatically — axioms: the standard three of Lean's logic")

    def construct(self) -> None:
        self.setup_frame()
        c = excerpt("verification/lean_proofs/Ch5103/Identities.lean", 72, 83, width=12.8, height=3.6).move_to([0, 0.75, 0])
        L = c.code_lines
        audit = boxed("`#print axioms`, all 17 theorems: only `propext`, `Classical.choice`, `Quot.sound`", "checked",
                      width=12.0, size=26, tag="Axiom audit").move_to([0, -1.95, 0])
        self.say("[Inside test T seventeen, the Lean proof of the less-screening logic. The comment states it: if the "
                 "triplet is lower, both states obey the virial theorem, and the triplet has the larger repulsion, then "
                 "the kinetic energy rises, and the nuclear attraction falls by more than twice the energy gap and by more "
                 "than the repulsion rises.]", m.AnimationGroup(m.FadeIn(c.background), m.FadeIn(c.line_numbers), *[m.FadeIn(L[k]) for k in range(0, 2)]))
        self.say("[The theorem takes the four differences as real numbers, with four hypotheses: the virial theorem for "
                 "the differences, the energy as the sum of its parts, the triplet lower, and the repulsion higher. Its "
                 "conclusion has four parts, and linarith proves each by linear arithmetic.]",
                 m.AnimationGroup(*[m.FadeIn(L[k]) for k in range(2, 7)]))
        self.say("[The second theorem: frozen orbitals, with no change in kinetic energy, are incompatible with the virial "
                 "theorem unless the energy gap is zero.]", m.AnimationGroup(*[m.FadeIn(L[k]) for k in range(7, len(L))]))
        self.say("[And the axiom audit: for all seventeen theorems, print axioms lists only the three standard axioms of "
                 "Lean's logic, propositional extensionality, classical choice and quotient soundness. No sorry, and no "
                 "extra assumptions.]", m.FadeIn(audit))
        self.wait(0.4)


class S129Caught(Frame):
    """18-verification.tex, frame 7: 'What the tests caught in our own work'."""

    TITLE = "What the tests caught in our own work"

    def construct(self) -> None:
        self.setup_frame()
        pts = bullets([r"**T8**: we assumed $\#\text{NBMO}=N-2T$; cyclobutadiene says $\ge$",
                       r"**T9b**: lowest $S_z=0$ level was the triplet's $M_S=0$ component, not a singlet",
                       r"**T11a**: we expected a SOMO/HOMO flip in standard schemes; it needs $A>1$",
                       r"**T5**: a symmetry tolerance of $10^{-10}$ failed on round-off at $S\sim10^{-16}$",
                       r"**T12**: our illustrative numbers had the wrong sign of $\Delta$"], width=6.6, size=28)
        pts.move_to([-3.0, 0.35, 0])
        res = boxed("every failure was diagnosed before the test changed, and each is logged in `plans/tests.md`",
                    "result", width=5.4, size=28).move_to([3.7, 0.9, 0])
        moral = rich("a check that is able to fail is what turns “I believe” into “checked”", 27, MUTED, width=5.4)
        moral.next_to(res, m.DOWN, buff=0.4)
        self.say("[The tests also caught our own mistakes. T eight: we had assumed the number of non-bonding orbitals was "
                 "exactly N minus two T; cyclobutadiene showed it is only a lower bound.]", m.FadeIn(pts[0]))
        self.say("[T nine b: the lowest level with S z zero was the M S zero component of the triplet, not a singlet.]",
                 m.FadeIn(pts[1]))
        self.say("[T eleven a: we expected the SOMO and HOMO to flip under standard canonicalisation schemes; it needs a "
                 "weight above one.]", m.FadeIn(pts[2]))
        self.say("[T five: a symmetry tolerance of ten to the minus ten failed on round-off, at overlaps near ten to the "
                 "minus sixteen.]", m.FadeIn(pts[3]))
        self.say("[T twelve: our first illustrative numbers had the wrong sign of delta.]", m.FadeIn(pts[4]))
        self.say("[Every failure was diagnosed before the test was changed, and each is logged in the plans folder.]",
                 m.FadeIn(res))
        self.say("[A check that is able to fail is what turns I believe into checked.]", m.FadeIn(moral))
        self.wait(0.4)
