"""Chapter 1: foundations (presentation/sections/03-foundations.tex)."""
import manimgx as m

from noir import (BLUE, CYAN, EXPL, FG, GOLD, GREEN, MUTED, ROSE, Box, Derivation, Frame, M, T, boxed, level,
                  rich, spin, why)


def explain(text: str, width: float = 6.6, size: float = 26) -> m.Mobject:
    """The slides' \\explain line: a small cyan triangle and blue italic prose."""
    tri = m.Triangle(color=EXPL, fill_color=EXPL, fill_opacity=1, stroke_width=0).scale(0.07).rotate(-m.PI / 2)
    body = rich(text, size=size, color=EXPL, font="EB Garamond", italic=True, width=width)
    tri.next_to(body, m.LEFT, buff=0.15).align_to(body, m.UP).shift(m.DOWN * 0.13)
    return m.VGroup(tri, body)


class S07WhereItStarts(Frame):
    """03-foundations.tex, frame 1: 'Where everything starts'."""

    TITLE = "Where everything starts"
    SUBTITLE = "the molecular Schrödinger equation"
    SYMBOLS = (r"$\Psi$: total wavefunction of all electrons and nuclei — $E$: total energy — $A,B$: nuclei, $i,j$: "
               r"electrons — $M_A$: nuclear mass, in units of $m_e$ — $Z_A$: nuclear charge — $r_{iA},r_{ij},R_{AB}$: "
               r"distances — atomic units $\hbar=m_e=e=1$")

    def construct(self) -> None:
        self.setup_frame()
        top = M(r"\Hop_{\text{mol}}\,\Psi=E\,\Psi", size=46).move_to([0, 2.15, 0])
        H = M(r"\Hop_{\text{mol}}=", r"-\sum_A\frac{\nabla_A^2}{2M_A}", r"-\sum_i\frac{\nabla_i^2}{2}",
              r"-\sum_{i,A}\frac{Z_A}{r_{iA}}", r"+\sum_{i<j}\frac{1}{r_{ij}}", r"+\sum_{A<B}\frac{Z_AZ_B}{R_{AB}}",
              size=42).move_to([0, 1.05, 0])
        labels = [("nuclear\nKE", MUTED), ("electron\nKE", CYAN), ("e–n\nattraction", GOLD), ("e–e\nrepulsion", ROSE),
                  ("n–n\nrepulsion", MUTED)]
        braces = []
        for k, (text, col) in enumerate(labels, start=1):
            b = m.Brace(H[k], m.DOWN, buff=0.16, color=col)
            lab = m.VGroup(*[T(line, 26, col) for line in text.split("\n")]).arrange(m.DOWN, buff=0.06)
            lab.next_to(b, m.DOWN, buff=0.08)
            braces.append(m.VGroup(b, lab))
        # the picture: two nuclei, two electrons and the three kinds of distance
        A, B = [-6.2, -2.35, 0], [-1.9, -2.35, 0]
        ei, ej = [-4.8, -1.05, 0], [-3.0, -1.3, 0]
        dots = m.VGroup(m.Dot(A, radius=0.11, color=GOLD), m.Dot(B, radius=0.11, color=GOLD),
                        m.Dot(ei, radius=0.07, color=CYAN), m.Dot(ej, radius=0.07, color=CYAN))
        names = m.VGroup(M("A", size=30, color=GOLD).next_to(dots[0], m.DOWN, buff=0.1),
                         M("B", size=30, color=GOLD).next_to(dots[1], m.DOWN, buff=0.1),
                         M("i", size=30, color=CYAN).next_to(dots[2], m.UP, buff=0.1),
                         M("j", size=30, color=CYAN).next_to(dots[3], m.UP, buff=0.1))
        riA = m.DashedLine(A, ei, color=GOLD, stroke_width=2.5)
        rij = m.Line(ei, ej, color=ROSE, stroke_width=2.5)
        RAB = m.DashedLine(A, B, color=MUTED, stroke_width=2.5)
        lab_riA = M("r_{iA}", size=26, color=GOLD).next_to(riA.get_center(), m.UL, buff=0.12)
        lab_rij = M("r_{ij}", size=26, color=ROSE).next_to(rij.get_center(), m.UP, buff=0.12)
        lab_RAB = M("R_{AB}", size=26, color=MUTED).next_to(RAB.get_center(), m.DOWN, buff=0.12)
        e1 = explain(r"kinetic energy is $-\tfrac12\nabla^2$, second derivatives: curvature of $\Psi$ costs energy")
        e2 = explain(r"attraction: every electron $i$ to every nucleus $A$ of charge $Z_A$, falling off as $1/r$")
        e3 = explain(r"repulsion: every pair of electrons once; $i<j$ avoids double counting")
        ex = m.VGroup(e1, e2, e3).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.14).move_to([3.1, 0, 0])
        ex.shift(m.UP * (-0.72 - ex.get_top()[1]))
        self.say("[Everything starts from the molecular Schrödinger equation: the molecular Hamiltonian acting on the "
                 "wavefunction Psi gives the total energy E times Psi.] Psi depends on the positions of all the "
                 "electrons and all the nuclei.", m.Write(top))
        self.say("[The Hamiltonian is a sum of five terms.] [The first is the kinetic energy of the nuclei: minus one "
                 "half times the Laplacian with respect to each nucleus, divided by that nucleus's mass.]",
                 m.Write(H), m.GrowFromCenter(braces[0]))
        self.say("[Kinetic energy is minus one half times second derivatives, so a wavefunction that curves sharply "
                 "costs energy.] [The second term is the same thing for the electrons, whose mass is one in atomic "
                 "units.]", m.FadeIn(e1), m.GrowFromCenter(braces[1]))
        self.say("[The third term is the attraction between every electron i and every nucleus A of charge Z A, "
                 "which falls off as one over their distance, r i A.]",
                 m.AnimationGroup(m.GrowFromCenter(braces[2]), m.FadeIn(dots), m.FadeIn(names), m.Create(riA),
                                  m.FadeIn(lab_riA), m.FadeIn(e2)))
        self.say("[The fourth is the repulsion between the electrons: one over r i j for every pair, with i less than "
                 "j, so that each pair is counted once.]",
                 m.AnimationGroup(m.GrowFromCenter(braces[3]), m.Create(rij), m.FadeIn(lab_rij), m.FadeIn(e3)))
        self.say("[The last is the repulsion between the nuclei: Z A times Z B over their distance, capital R A B.]",
                 m.AnimationGroup(m.GrowFromCenter(braces[4]), m.Create(RAB), m.FadeIn(lab_RAB)))
        self.wait(0.4)


class S08BornOppenheimer(Frame):
    """03-foundations.tex, frame 2: 'Born–Oppenheimer: freeze the nuclei'."""

    TITLE = "Born–Oppenheimer: freeze the nuclei"
    SUBTITLE = r"assume $M_A\gg m_e=1$: electrons adjust instantly; nuclear positions $\{\mathbf R_A\}$ are parameters"
    SYMBOLS = (r"$\mathbf R_A$: position of nucleus $A$ — $V_{nn}$: nuclear repulsion, a number once the nuclei are fixed "
               r"— $N$: number of electrons — $\hat h(i)$: one-electron, or core, Hamiltonian — $\Hop$ has no spin "
               r"operator: spin enters only through the Pauli principle")

    def construct(self) -> None:
        self.setup_frame()
        steps = [(r"drop the nuclear kinetic energy", r"-\sum_A\nabla_A^2/2M_A\to0"),
                 (r"nuclear repulsion becomes a constant", r"V_{nn}(\mathbf R)"),
                 (r"what is left is the electronic Hamiltonian", None)]
        rows = []
        for k, (t, f) in enumerate(steps, 1):
            num = T(f"{k}.", 30, GOLD)
            txt = rich(t, 30, GOLD if f is None else FG)
            row = m.VGroup(num, txt).arrange(m.RIGHT, buff=0.25)
            if f:
                row.add(M(f, size=34).move_to([4.6, 0, 0]))
            rows.append(row)
        lst = m.VGroup(*rows).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.35).move_to([-0.6, 1.35, 0])
        for r in rows[:2]:
            r[2].set_x(4.3)
        Hel = M(r"\Hop=\sum_{i=1}^{N}\hat h(i)+\sum_{i<j}\frac1{r_{ij}},\qquad \hat h(i)=-\tfrac12\nabla_i^2-\sum_A\frac{Z_A}{r_{iA}}",
                size=40)
        frame = m.SurroundingRectangle(Hel, color=GOLD, buff=0.22, stroke_width=2.5)
        box = m.VGroup(Hel, frame).move_to([0, -0.55, 0])
        e1 = explain(r"a proton is about $1836$ times heavier than an electron, so on the electrons' time scale the nuclei "
                     r"stand still", width=11.5)
        e2 = explain(r"$\hat h(i)$ is everything that involves electron $i$ alone; $1/r_{ij}$ couples the electrons in "
                     r"pairs and is the hard part", width=11.5)
        ex = m.VGroup(e1, e2).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.18).move_to([0, -2.2, 0])
        self.say("The first approximation is due to Born and Oppenheimer. [A proton is about eighteen hundred and "
                 "thirty six times heavier than an electron, so on the electrons' time scale the nuclei stand "
                 "still.] The electrons adjust instantly to wherever the nuclei are, and the nuclear positions become "
                 "parameters.", m.FadeIn(e1))
        self.say("[So we drop the nuclear kinetic energy.]", m.FadeIn(rows[0], shift=m.RIGHT * 0.1))
        self.say("[The repulsion between the nuclei becomes a constant, V n n, which depends only on where the nuclei "
                 "sit.]", m.FadeIn(rows[1], shift=m.RIGHT * 0.1))
        self.say("[What is left is the electronic Hamiltonian:] [a sum of one-electron operators, h of i, plus the "
                 "electron repulsion, one over r i j, summed over pairs.]",
                 m.FadeIn(rows[2], shift=m.RIGHT * 0.1), m.AnimationGroup(m.Write(Hel), m.Create(frame)))
        self.say("[Here h of i collects everything that involves electron i alone: its kinetic energy and its "
                 "attraction to every nucleus. The pair repulsion couples the electrons, and it is the hard part.] "
                 "Notice that this Hamiltonian contains no spin operator at all: spin will enter only through the "
                 "Pauli principle.", m.FadeIn(e2))
        self.wait(0.4)


class S09Variational(Frame):
    """03-foundations.tex, frame 3: 'The variational principle'."""

    TITLE = "The variational principle"
    SUBTITLE = r"assume exact eigenstates $\Hop\Psi_n=E_n\Psi_n$: orthonormal, complete, $E_0\le E_1\le\cdots$"
    SYMBOLS = (r"$\tilde\Psi$: any trial wavefunction — $c_n$: complex expansion coefficients — "
               r"$\braket fg=\int f^*g\,\dd\tau$: overlap integral over all coordinates — "
               r"$\mel f{\Hop}g=\int f^*\Hop g\,\dd\tau$ — $\delta_{mn}$: one if $m=n$, else zero")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\text{(1)}\ \tilde\Psi", r"=\textstyle\sum_n c_n\Psi_n,\qquad \sum_n|c_n|^2=1",
             "any function is a mix of eigenstates (completeness)"),
            (r"\text{(2)}\ \langle\tilde\Psi|\Hop|\tilde\Psi\rangle", r"=\textstyle\sum_{m,n}c_m^*c_n\,E_n\langle\Psi_m|\Psi_n\rangle",
             r"insert both sums; $\Hop\Psi_n=E_n\Psi_n$"),
            ("", r"=\textstyle\sum_n|c_n|^2E_n", r"orthonormality: only $m=n$ terms survive"),
            (r"\text{(3)}", r"\ge\textstyle\sum_n|c_n|^2E_0=E_0", r"each $E_n\ge E_0$; then use $\sum|c_n|^2=1$"),
        ], size=38, why_size=24)
        d.next_to(self.title_group, m.DOWN, buff=0.55).set_x(0)
        res = rich(r"$E[\tilde\Psi]\ge E_0$ for every normalised $\tilde\Psi$: a lower energy is a better wavefunction",
                   size=32, color=GREEN).next_to(d, m.DOWN, buff=0.55)
        self.say("Next, the variational principle. Assume we know the exact eigenstates Psi n of the Hamiltonian, with "
                 "energies E n in increasing order, and that they are orthonormal and complete.")
        self.say("[Step one. Any normalised trial function, Psi tilde, can be written as a mixture of these "
                 "eigenstates, with coefficients c n whose squared moduli add up to one.] That is what completeness "
                 "means.", m.FadeIn(d.rows[0]))
        self.say("[Step two. Insert both sums into the energy expectation value. The Hamiltonian acting on Psi n gives "
                 "E n times Psi n.] [Orthonormality then removes every term with m different from n, leaving the sum "
                 "of c n squared times E n.]", m.FadeIn(d.rows[1]), m.FadeIn(d.rows[2]))
        self.say("[Step three. Every E n is at least the ground-state energy, E nought. Replacing each E n by E nought "
                 "can only lower the sum, and the weights add up to one, so the result is E nought.]",
                 m.FadeIn(d.rows[3]))
        self.say("[So the energy of any normalised trial function is never below the true ground-state energy.] A "
                 "lower energy means a better wavefunction, and that principle sits behind every method in this "
                 "video.", m.Write(res))
        self.wait(0.4)


class S10Orbitals(Frame):
    """03-foundations.tex, frame 4: 'Orbitals: the independent-electron picture'."""

    TITLE = "Orbitals: the independent-electron picture"
    SYMBOLS = (r"$\hat f$: Fock, or mean-field, operator — $\varphi_p$: spatial orbital $p$ — $\varepsilon_p$: its "
               r"orbital energy — $\chi_\mu$: atom-centred basis function — $c_{\mu p}$: LCAO coefficient — "
               r"up and down arrows: spin $\alpha$ and $\beta$ — SOMO: singly occupied MO")

    def construct(self) -> None:
        self.setup_frame()
        assume = boxed(r"replace $\sum_{i<j}1/r_{ij}$ by an average field felt by each electron", "assume",
                       width=7.4, size=30, tag="Independent-particle model")
        eq1 = rich(r"one-electron problem: $\quad\hat f\,\varphi_p=\varepsilon_p\,\varphi_p$", 32)
        eq2 = rich(r"LCAO, atom-centred functions: $\quad\varphi_p(\mathbf r)=\sum_\mu c_{\mu p}\,\chi_\mu(\mathbf r)$", 32)
        e1 = explain(r"each electron feels the averaged field of the others; occupations build the configuration",
                     width=7.2)
        left = m.VGroup(assume, eq1, eq2, e1).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.42)
        left.to_edge(m.LEFT, buff=0.7).shift(m.DOWN * 0.15)
        x0 = 4.3
        axis = m.Arrow([x0 - 1.2, -2.3, 0], [x0 - 1.2, 2.2, 0], buff=0, color=MUTED, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.05)
        eps = M(r"\varepsilon", size=32, color=MUTED).next_to(axis, m.UP, buff=0.08)
        ys = [-1.9, -0.9, 0.1, 1.5]
        levels = m.VGroup(*[level(x0, y, 1.1, f"$\\varphi_{k}$" if False else "") for k, y in enumerate(ys, 1)])
        names = m.VGroup(*[M(rf"\varphi_{k}", size=30, color=MUTED).next_to(levels[k - 1], m.RIGHT, buff=0.15)
                           for k in range(1, 5)])
        elec = m.VGroup(spin(x0, ys[0], True), spin(x0, ys[0], False), spin(x0, ys[1], True), spin(x0, ys[1], False),
                        spin(x0, ys[2], True))
        somo = T("SOMO", 26, GOLD).next_to(names[2], m.RIGHT, buff=0.2)
        self.say("[Solving the many-electron problem exactly is hopeless for all but the smallest systems, so the "
                 "orbital model replaces the pair repulsion by an average field that each electron feels from all the "
                 "others.]", m.FadeIn(assume))
        self.say("[Each electron then obeys a one-electron equation: the Fock operator, f, acting on an orbital phi p, "
                 "gives the orbital energy epsilon p times phi p.]",
                 m.AnimationGroup(m.FadeIn(eq1), m.GrowArrow(axis), m.FadeIn(eps), m.FadeIn(levels), m.FadeIn(names),
                                  m.FadeIn(e1)))
        self.say("[In practice each molecular orbital is built as a linear combination of atom-centred basis "
                 "functions, chi mu, with coefficients c mu p. This is the LCAO approximation: linear combination of "
                 "atomic orbitals.]", m.FadeIn(eq2))
        self.say("[Filling the orbitals with electrons, at most two per orbital and with opposite spins, builds the "
                 "configuration.] [An orbital that holds a single electron is called a SOMO, a singly occupied "
                 "molecular orbital.]",
                 m.LaggedStart(*[m.GrowArrow(e) for e in elec], lag_ratio=0.2), m.FadeIn(somo))
        self.wait(0.4)


class S11Box1(Frame):
    """03-foundations.tex, frame 5: 'Box 1: “Much ado about orbitals”'."""

    TITLE = "Box 1: “Much ado about orbitals”"
    SYMBOLS = (r"unitary mixing: replacing the occupied orbitals by orthonormal combinations of themselves — "
               r"$\rho(\mathbf r)$: electron density, the probability of finding an electron at $\mathbf r$, which "
               r"can be measured")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"The reality is that an orbital is a mathematical construct, an approximate, non-unique '
                      'solution to the Schrödinger equation." — p. 448', "claim", width=7.0, size=28)
        nonu = boxed(r"Non-unique: unitary mixing of occupied orbitals leaves the determinant and every observable "
                     r"unchanged.", "plain", width=7.0, size=28)
        appr = boxed(r"Approximate: orbitals are defined within the independent-particle, or orbital, model.",
                     "plain", width=7.0, size=28)
        left = m.VGroup(claim, nonu, appr).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.35)
        left.to_edge(m.LEFT, buff=0.6).shift(m.DOWN * 0.1)
        nature = boxed(r"A 1999 Nature report on “the direct observation of copper's d-orbitals” (p. 448) started a "
                       r"debate: can an orbital be observed? What is observable is the density $\rho(\mathbf r)$, and "
                       r"orbital occupations.", "plain", width=5.6, size=27)
        nature.next_to(left, m.RIGHT, buff=0.45).align_to(left, m.UP)
        keep = rich("Keep this in mind: it returns when ROHF orbital orderings depend on a convention.", 30, GOLD,
                    width=12.5).to_edge(m.DOWN, buff=1.05)
        self.say("[The review has a box called Much ado about orbitals. It says: the reality is that an orbital is a "
                 "mathematical construct, an approximate, non-unique solution to the Schrödinger equation.]",
                 m.FadeIn(claim))
        self.say("[Non-unique, because mixing the occupied orbitals among themselves by a unitary transformation leaves "
                 "the determinant, and so every observable, unchanged.]", m.FadeIn(nonu))
        self.say("[Approximate, because orbitals are defined only within the independent-particle model.]",
                 m.FadeIn(appr))
        self.say("[In nineteen ninety nine a report in Nature claimed the direct observation of copper's d orbitals, "
                 "and started a debate: can an orbital be observed at all?] What can be observed is the electron "
                 "density, the probability of finding an electron at a point, and orbital occupations.",
                 m.FadeIn(nature))
        self.say("[Keep this in mind. It returns later, when the order of restricted open-shell orbital energies "
                 "turns out to depend on a convention.]", m.FadeIn(keep))
        self.wait(0.4)
