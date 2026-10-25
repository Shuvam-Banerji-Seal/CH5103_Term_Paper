"""Chapter 2: spin and antisymmetry (presentation/sections/04-spin.tex)."""
import manimgx as m

from ch01_foundations import explain
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, PANEL, ROSE, Box, Derivation, Frame, M, T, boxed, bullets,
                  rich, why)


class S12Swap(Frame):
    """04-spin.tex, frame 1: 'Swapping two electrons'."""

    TITLE = "Swapping two electrons"
    SUBTITLE = r"why the exchange eigenvalue is $\pm1$"
    SYMBOLS = (r"$x_i=(\mathbf r_i,\sigma_i)$: all coordinates of electron $i$, position plus spin coordinate — "
               r"$\hat P_{12}$: operator exchanging electrons 1 and 2 — $\lambda$: its eigenvalue — "
               r"$[\hat A,\hat B]=\hat A\hat B-\hat B\hat A$ — fermions: half-integer-spin particles, such as electrons")

    def construct(self) -> None:
        self.setup_frame()
        defn = rich(r"Define $\hat P_{12}\Psi(x_1,x_2)=\Psi(x_2,x_1)$, with $x=(\mathbf r,\sigma)$.", 32)
        d = Derivation([
            (r"\text{(1)}", r"\hat P_{12}^2=\hat 1", "swapping twice restores the order"),
            (r"\text{(2)}", r"\hat P_{12}\Psi=\lambda\Psi\ \Rightarrow\ \Psi=\lambda^2\Psi", r"apply $\hat P_{12}$ twice"),
            (r"\text{(3)}", r"\lambda=\pm1", r"since $\lambda^2=1$"),
            (r"\text{(4)}", r"[\Hop,\hat P_{12}]=0", r"$\Hop$ treats all electrons alike"),
        ], size=38, why_size=26)
        left = m.VGroup(defn, d).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.45).move_to([-2.0, 0.55, 0])
        e1, e2 = m.Dot([3.9, 0.3, 0], radius=0.13, color=CYAN), m.Dot([6.0, 0.3, 0], radius=0.13, color=ROSE)
        n1, n2 = T("1", 28).next_to(e1, m.DOWN, buff=0.15), T("2", 28).next_to(e2, m.DOWN, buff=0.15)
        top = m.CurvedArrow([4.1, 0.5, 0], [5.8, 0.5, 0], angle=-m.PI / 2.2, color=GOLD, stroke_width=3)
        bot = m.CurvedArrow([5.8, 0.1, 0], [4.1, 0.1, 0], angle=-m.PI / 2.2, color=GOLD, stroke_width=3)
        P = M(r"\hat P_{12}", size=34, color=GOLD).move_to([4.95, 1.45, 0])
        lam = M(r"\lambda=-1", size=44, color=ROSE).move_to([4.95, -1.0, 0])
        note = rich("so eigenstates have definite λ; for electrons nature picks −1. The paper: “the wavefunction for a "
                    "system of fermions must be antisymmetric with respect to the interchange of any two particles” "
                    "— p. 441", 28, width=12.6)
        note[0].set_color(FG)
        note.move_to([0, -2.25, 0])
        self.say("[Start with two electrons. Define the exchange operator, P one two, which swaps all the coordinates "
                 "of electrons one and two: position and spin together, written x.]",
                 m.AnimationGroup(m.FadeIn(defn), m.FadeIn(m.VGroup(e1, e2, n1, n2)), m.Create(top), m.Create(bot),
                                  m.FadeIn(P)))
        self.say("[Step one. Swapping twice restores the original order, so P one two squared is the identity.]",
                 m.FadeIn(d.rows[0]))
        self.say("[Step two. If Psi is an eigenfunction of P one two with eigenvalue lambda, applying the operator "
                 "twice gives lambda squared times Psi, and by step one that must equal Psi.]", m.FadeIn(d.rows[1]))
        self.say("[Step three. So lambda squared is one, and lambda is plus one or minus one.]", m.FadeIn(d.rows[2]))
        self.say("[Step four. The Hamiltonian treats all electrons alike, so it commutes with P one two.] That means "
                 "the energy eigenstates can be chosen with a definite exchange symmetry.", m.FadeIn(d.rows[3]))
        self.say("[For electrons, nature picks minus one.] The paper puts it this way: the wavefunction for a system "
                 "of fermions must be antisymmetric with respect to the interchange of any two particles. Fermions "
                 "are particles of half-integer spin, such as electrons.",
                 m.AnimationGroup(m.Write(lam), m.FadeIn(note)))
        self.wait(0.4)


class S13Slater(Frame):
    """04-spin.tex, frame 2: 'Slater determinants'."""

    TITLE = "Slater determinants"
    SUBTITLE = "antisymmetry built in"
    SYMBOLS = (r"$\chi(x)$: spin orbital, a spatial orbital times a spin function, for example $\chi=\pa(\mathbf r)\,"
               r"\alpha(\sigma)$ — $\chi_1(2)$: spin orbital 1 at electron 2's coordinates — $\tfrac1{\sqrt2}$: "
               r"$D$ is two orthogonal products of norm one, so $\braket DD=2$")

    def construct(self) -> None:
        self.setup_frame()
        D = M(r"D[\chi_1,\chi_2]=\begin{vmatrix}\chi_1(1)&\chi_2(1)\\\chi_1(2)&\chi_2(2)\end{vmatrix}"
              r"=\chi_1(1)\chi_2(2)-\chi_2(1)\chi_1(2)", size=40).move_to([0, 2.05, 0])
        e = explain("rows label electrons, columns label spin orbitals; the determinant mixes every assignment with "
                    "a sign", width=11.0).next_to(D, m.DOWN, buff=0.2)
        b = bullets([r"swap electrons ⇔ swap two rows ⇒ $D\to-D$: antisymmetric",
                     r"two equal spin orbitals ⇔ two equal columns ⇒ $D=0$: Pauli exclusion",
                     r"normalised: $\ket{\chi_1\chi_2}=\tfrac1{\sqrt2}D[\chi_1,\chi_2]$"], width=11.5, size=28, buff=0.2)
        b.next_to(e, m.DOWN, buff=0.25).set_x(-0.2)
        res = boxed("Pauli's 1925 rule — no two electrons with all four quantum numbers equal, p. 448 — is a "
                    "consequence of antisymmetry inside the orbital model, not a separate law.", "result", width=11.5,
                    size=27).next_to(b, m.DOWN, buff=0.3)
        self.say("[Antisymmetry is built in automatically by a Slater determinant. For two electrons in spin orbitals "
                 "chi one and chi two, it is chi one of electron one times chi two of electron two, minus chi two of "
                 "electron one times chi one of electron two.]", m.Write(D))
        self.say("[The rows label electrons and the columns label spin orbitals, and the determinant mixes every "
                 "assignment of electrons to orbitals with a sign.]", m.FadeIn(e))
        self.say("[Swapping the two electrons swaps two rows of the determinant, which flips its sign: the function "
                 "is antisymmetric.]", m.FadeIn(b[0], shift=m.RIGHT * 0.1))
        self.say("[If both columns hold the same spin orbital, the determinant has two equal columns and vanishes. "
                 "That is the Pauli exclusion principle.]", m.FadeIn(b[1], shift=m.RIGHT * 0.1))
        self.say("[With a factor of one over root two it is normalised: each product has norm one and the two products "
                 "are orthogonal, so the determinant's squared norm is two.]", m.FadeIn(b[2], shift=m.RIGHT * 0.1))
        self.say("[So Pauli's rule of nineteen twenty five, that no two electrons have all four quantum numbers equal, "
                 "is a consequence of antisymmetry inside the orbital model, not a separate law.]", m.FadeIn(res))
        self.wait(0.4)


class S14SpinOps(Frame):
    """04-spin.tex, frame 3: 'Spin operators for two electrons'."""

    TITLE = "Spin operators for two electrons"
    SYMBOLS = (r"$\alpha,\beta$: spin up and down of one electron — $\hat s_+$ flips down to up, $\hat s_-$ flips up "
               r"to down, giving zero if impossible — $\hat S_x,\hat S_y,\hat S_z,\hat S^2$: total spin components and "
               r"squared magnitude — $\hbar=1$")

    def construct(self) -> None:
        self.setup_frame()
        h1 = rich(r"One electron, $s=\tfrac12$:", 32, GOLD)
        ops = [M(r"\hat s_z\alpha=+\tfrac12\alpha,\qquad \hat s_z\beta=-\tfrac12\beta", size=36),
               M(r"\hat s_+\beta=\alpha,\qquad \hat s_+\alpha=0", size=36),
               M(r"\hat s_-\alpha=\beta,\qquad \hat s_-\beta=0", size=36)]
        h2 = rich("Two electrons: add each electron's operator", 32, GOLD)
        two = M(r"\hat S_z=\hat s_{z}(1)+\hat s_{z}(2),\quad \hat S_\pm=\hat s_\pm(1)+\hat s_\pm(2)", size=34)
        left = m.VGroup(h1, *ops, h2, two).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3).move_to([-3.6, 0.3, 0])
        h3 = rich("A useful identity:", 32, GOLD)
        d = Derivation([
            (r"\hat S_-\hat S_+", r"=(\hat S_x-i\hat S_y)(\hat S_x+i\hat S_y)", r"definition of $\hat S_\pm$"),
            ("", r"=\hat S_x^2+\hat S_y^2+i[\hat S_x,\hat S_y]", "multiply out"),
            ("", r"=\hat S^2-\hat S_z^2+i(i\hat S_z)", r"$[\hat S_x,\hat S_y]=i\hat S_z$"),
            ("", r"=\hat S^2-\hat S_z^2-\hat S_z", r"$i\cdot i=-1$"),
        ], size=32, why_size=24, why_gap=0.35)
        box = M(r"\boxed{\hat S^2=\hat S_-\hat S_++\hat S_z^2+\hat S_z}", size=40, color=GREEN)
        right = m.VGroup(h3, d, box).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3).move_to([3.35, 0.2, 0])
        box.set_x(right.get_center()[0])
        self.say("Now spin. [For one electron of spin one half, s z gives plus one half on alpha, spin up, and minus "
                 "one half on beta, spin down.] [The raising operator, s plus, turns beta into alpha and gives zero on "
                 "alpha,] [and the lowering operator, s minus, turns alpha into beta and gives zero on beta.]",
                 m.AnimationGroup(m.FadeIn(h1), m.FadeIn(ops[0])), m.FadeIn(ops[1]), m.FadeIn(ops[2]))
        self.say("[For two electrons we add each electron's operator: S z is s z of electron one plus s z of electron "
                 "two, and the same for S plus and S minus.]", m.AnimationGroup(m.FadeIn(h2), m.FadeIn(two)))
        self.say("[A useful identity follows. Write S minus times S plus using S plus or minus equals S x plus or "
                 "minus i S y.]", m.AnimationGroup(m.FadeIn(h3), m.FadeIn(d.rows[0])))
        self.say("[Multiply out: S x squared plus S y squared, plus i times the commutator of S x and S y.]",
                 m.FadeIn(d.rows[1]))
        self.say("[The commutator of S x and S y is i S z, and S x squared plus S y squared is S squared minus S z "
                 "squared.]", m.FadeIn(d.rows[2]))
        self.say("[And i times i is minus one.]", m.FadeIn(d.rows[3]))
        self.say("[Rearranged: S squared equals S minus S plus, plus S z squared, plus S z.] This form is handy "
                 "because S plus gives zero on many simple spin functions.", m.Write(box))
        self.wait(0.4)


class S15S2Products1(Frame):
    """04-spin.tex, frame 4: 'S² on the four spin products (1/2)'."""

    TITLE = r"$\hat S^2$ on the four spin products (1/2)"
    SYMBOLS = (r"$\alpha_1\equiv\alpha(\sigma_1)$: electron 1 is spin up — $\alpha_1\beta_2$: electron 1 up, electron "
               r"2 down — the eigenvalue of $\hat S^2$ is $S(S+1)$ — $M_S$: eigenvalue of $\hat S_z$, the sum of the "
               r"two $\pm\tfrac12$")

    def construct(self) -> None:
        self.setup_frame()
        hl = rich(r"$\alpha_1\alpha_2$, both up", 32, GOLD)
        dl = Derivation([
            (r"\hat S_+\alpha_1\alpha_2", r"=0", "nothing left to raise"),
            (r"\hat S_z\alpha_1\alpha_2", r"=(\tfrac12+\tfrac12)\alpha_1\alpha_2", r"each adds $+\tfrac12$"),
            (r"\hat S^2\alpha_1\alpha_2", r"=(0+1+1)\,\alpha_1\alpha_2", r"$\hat S_-\hat S_++\hat S_z^2+\hat S_z$"),
            ("", r"=2\,\alpha_1\alpha_2", ""),
        ], size=32, why_size=24, why_gap=0.3)
        rl = rich(r"$S(S+1)=2\Rightarrow S=1,\ M_S=+1$", 30, GREEN)
        left = m.VGroup(hl, dl, rl).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.35).move_to([-3.55, 0.3, 0])
        hr = rich(r"$\beta_1\beta_2$, both down", 32, GOLD)
        dr = Derivation([
            (r"\hat S_+\beta_1\beta_2", r"=\alpha_1\beta_2+\beta_1\alpha_2", "raise 1 or 2"),
            (r"\hat S_-(\ldots)", r"=\beta_1\beta_2+\beta_1\beta_2", "lower the raised one"),
            (r"(\hat S_z^2+\hat S_z)\beta_1\beta_2", r"=(1-1)\beta_1\beta_2", r"$M_S=-1$"),
            (r"\hat S^2\beta_1\beta_2", r"=2\,\beta_1\beta_2", ""),
        ], size=32, why_size=24, why_gap=0.3)
        rr = rich(r"$S=1,\ M_S=-1$", 30, GREEN)
        right = m.VGroup(hr, dr, rr).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.35).move_to([3.5, 0.3, 0])
        self.say("[Now apply S squared to the four products of one-electron spins. First, both electrons up: alpha "
                 "one alpha two.] [S plus gives zero, because there is nothing left to raise.]",
                 m.FadeIn(hl), m.FadeIn(dl.rows[0]))
        self.say("[S z gives one half plus one half, which is one.]", m.FadeIn(dl.rows[1]))
        self.say("[So S squared gives zero from the first term, one from S z squared, and one from S z,] [two in "
                 "total.]", m.FadeIn(dl.rows[2]), m.FadeIn(dl.rows[3]))
        self.say("[The eigenvalue of S squared is S times S plus one, so two means S equals one, with M S equal to "
                 "plus one.]", m.FadeIn(rl))
        self.say("[Next, both down: beta one beta two.] [S plus can raise electron one or electron two, giving alpha "
                 "one beta two plus beta one alpha two.]", m.FadeIn(hr), m.FadeIn(dr.rows[0]))
        self.say("[S minus then lowers whichever spin was raised, giving beta one beta two twice.]",
                 m.FadeIn(dr.rows[1]))
        self.say("[Here M S is minus one, so S z squared plus S z is one minus one, zero.]", m.FadeIn(dr.rows[2]))
        self.say("[So S squared on beta one beta two is two times beta one beta two:] [again S equals one, now with M S "
                 "equal to minus one.]", m.FadeIn(dr.rows[3]), m.FadeIn(rr))
        self.wait(0.4)


class S16S2Products2(Frame):
    """04-spin.tex, frame 5: 'S² on the four spin products (2/2)'."""

    TITLE = r"$\hat S^2$ on the four spin products (2/2)"
    SYMBOLS = (r"$\hat S_+$ acts on electron 1 or 2 in turn, being a sum; only the $\beta$ of electron 2 can be raised "
               r"here — $(1\pm1)$: $1+1=2$ for the sum, $1-1=0$ for the difference")

    def construct(self) -> None:
        self.setup_frame()
        head = rich(r"$\alpha_1\beta_2$ and $\beta_1\alpha_2$: $M_S=0$, neither is an eigenfunction on its own", 32,
                    GOLD).move_to([0, 2.2, 0])
        d = Derivation([
            (r"\hat S_+\alpha_1\beta_2", r"=\alpha_1\alpha_2", "only electron 2 can be raised"),
            (r"\hat S_-\alpha_1\alpha_2", r"=\beta_1\alpha_2+\alpha_1\beta_2", "lower 1 or 2"),
            (r"\hat S_z\alpha_1\beta_2", r"=(\tfrac12-\tfrac12)\,\alpha_1\beta_2=0", r"so $\hat S_z^2+\hat S_z$ gives 0"),
            (r"\Rightarrow\ \hat S^2\alpha_1\beta_2", r"=\alpha_1\beta_2+\beta_1\alpha_2", r"$\hat S_-\hat S_+$ term only"),
            (r"\hat S^2\beta_1\alpha_2", r"=\alpha_1\beta_2+\beta_1\alpha_2", "same steps"),
        ], size=30, why_size=24, row_buff=0.22).move_to([-0.6, 0.55, 0])
        e = explain(r"$\hat S^2$ turns $\alpha_1\beta_2$ into a different function: it is not an eigenfunction",
                    width=8.0).next_to(d, m.DOWN, buff=0.18)
        addsub = M(r"\hat S^2(\alpha_1\beta_2\pm\beta_1\alpha_2)=(1\pm1)\,(\alpha_1\beta_2\pm\beta_1\alpha_2)",
                   size=34).move_to([0, -1.85, 0])
        plus = Box(rich("+: eigenvalue 2 ⇒ S = 1", 30), "plain")
        minus = Box(rich("−: eigenvalue 0 ⇒ S = 0", 30), "plain")
        plus.panel.set_stroke(ROSE, 2)
        minus.panel.set_stroke(BLUE, 2)
        verdict = m.VGroup(plus, minus).arrange(m.RIGHT, buff=1.2).move_to([0, -2.6, 0])
        self.say("[That leaves the two mixed products, alpha one beta two and beta one alpha two, both with M S equal "
                 "to zero.]", m.FadeIn(head))
        self.say("[S plus on alpha one beta two can only raise electron two, giving alpha one alpha two.] [S minus "
                 "then lowers either electron, giving beta one alpha two plus alpha one beta two.]",
                 m.FadeIn(d.rows[0]), m.FadeIn(d.rows[1]))
        self.say("[S z gives one half minus one half, zero, so the S z terms contribute nothing.]",
                 m.FadeIn(d.rows[2]))
        self.say("[So S squared on alpha one beta two gives alpha one beta two plus beta one alpha two.] [It has turned "
                 "the function into a different one, so alpha one beta two is not an eigenfunction.]",
                 m.FadeIn(d.rows[3]), m.FadeIn(e))
        self.say("[By the same steps, S squared on beta one alpha two gives the same sum.]", m.FadeIn(d.rows[4]))
        self.say("[Now add and subtract the two results: S squared on the sum, or the difference, of the two products "
                 "is one plus or minus one times that same combination.]", m.Write(addsub))
        self.say("[The sum has eigenvalue two, so S is one: a triplet.] [The difference has eigenvalue zero, so S is "
                 "zero: a singlet.]", m.FadeIn(plus), m.FadeIn(minus))
        self.wait(0.4)


class S17SpinFunctions(Frame):
    """04-spin.tex, frame 6: 'Triplet and singlet spin functions'."""

    TITLE = "Triplet and singlet spin functions"
    SYMBOLS = (r"$\Theta_{S,M_S}$: two-electron spin function with total spin $S$ and projection $M_S$ — symmetric: "
               r"unchanged when $1\leftrightarrow2$; antisymmetric: changes sign — antisymmetric times symmetric is "
               r"antisymmetric, as required")

    def construct(self) -> None:
        self.setup_frame()
        th = M(r"\Theta_{1,+1}&=\alpha_1\alpha_2\\ \Theta_{1,0}&=\tfrac1{\sqrt2}(\alpha_1\beta_2+\beta_1\alpha_2)\\"
               r"\Theta_{1,-1}&=\beta_1\beta_2\\ \Theta_{0,0}&=\tfrac1{\sqrt2}(\alpha_1\beta_2-\beta_1\alpha_2)", size=40)
        res = Box(th, "result", tag="The four two-electron spin states").move_to([-3.4, 0.55, 0])
        e = explain(r"$\tfrac1{\sqrt2}$: the two products are orthonormal, so their sum has squared norm 2", width=6.3)
        e.next_to(res, m.DOWN, buff=0.3)
        b = bullets(["triplet spin functions are symmetric under 1 ↔ 2", "the singlet is antisymmetric",
                     "the total must be antisymmetric, so:"], width=5.6, size=30).move_to([3.5, 1.3, 0])
        rows = [("", "space", "spin"), ("triplet", "anti", "sym"), ("singlet", "sym", "anti")]
        cells = m.VGroup()
        for r, (a, s_, p) in enumerate(rows):
            for c, (txt, col) in enumerate([(a, FG), (s_, ROSE if r == 1 else BLUE if r == 2 else MUTED),
                                            (p, FG if r else MUTED)]):
                cells.add(T(txt, 30, col).move_to([2.2 + 1.7 * c, -0.75 - 0.6 * r, 0]))
        rule = m.VGroup(m.Line([1.4, -1.05, 0], [6.4, -1.05, 0], color=MUTED, stroke_width=1.5))
        check = rich("✓ T1: $\\hat S^2$ and $\\hat S_z$ as 4 × 4 matrices in SymPy; all eigen-relations exact.", 28,
                     MUTED, width=12.5).move_to([0, -2.55, 0])
        self.say("[Normalising the results gives the four two-electron spin states: three triplet functions with M S "
                 "equal to plus one, zero and minus one, and one singlet.]", m.FadeIn(res))
        self.say("[The factor one over root two appears because the two products are orthonormal, so their sum has "
                 "squared norm two.]", m.FadeIn(e))
        self.say("[All three triplet spin functions are symmetric when the electrons are swapped,] [while the singlet "
                 "is antisymmetric.]", m.FadeIn(b[0]), m.FadeIn(b[1]))
        self.say("[The total wavefunction must be antisymmetric, so] [a triplet must have an antisymmetric spatial "
                 "part, and a singlet a symmetric one.] This pairing of space and spin decides everything that "
                 "follows.", m.FadeIn(b[2]), m.AnimationGroup(m.FadeIn(cells), m.Create(rule)))
        self.say("[Test T one checked all of this exactly: S squared and S z were built as four by four matrices in "
                 "SymPy, and every eigenvalue relation holds exactly.]", m.FadeIn(check))
        self.wait(0.4)
