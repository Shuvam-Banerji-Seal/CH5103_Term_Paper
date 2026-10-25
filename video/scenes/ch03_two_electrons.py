"""Chapter 3: two electrons in two orbitals, and the sign error (presentation/sections/05-two-electrons.tex)."""
import manimgx as m

from ch01_foundations import explain
from noir import (ROOT, excerpt, BLUE, CYAN, FG, GOLD, GREEN, MUTED, PANEL, ROSE, VIOLET, Box, Derivation, Frame, M, T, boxed,
                  bullets, figure, level, paint_parts, pill, rich, spin, why)

AB = {"A": CYAN, "B": ROSE}


def config(x: float, y: float, lower: str, upper: str) -> m.VGroup:
    """Two levels (φa below, φb above) at x, with spins given as '', 'u', 'd' or 'ud'."""
    g = m.VGroup(level(x, y, 1.0), level(x, y + 1.15, 1.0))
    for yy, occ in ((y, lower), (y + 1.15, upper)):
        if occ == "ud":
            g.add(spin(x, yy, True), spin(x, yy, False))
        elif occ == "u":
            g.add(spin(x, yy, True).shift(m.RIGHT * 0.09))
        elif occ == "d":
            g.add(spin(x, yy, False).shift(m.LEFT * 0.09))
    return g


class S18SixWays(Frame):
    """05-two-electrons.tex, frame 1: 'Six ways to place two electrons'."""

    TITLE = "Six ways to place two electrons"
    SUBTITLE = "Figure 1 of the review, rebuilt"
    SYMBOLS = (r"$\pa,\pb$: the two spatial orbitals, real and orthonormal, for example the two frontier orbitals of a "
               r"diradical — up and down arrows: an electron with spin $\alpha$ or $\beta$ — $M_S$: total $S_z$, "
               r"$+\tfrac12$ per up arrow and $-\tfrac12$ per down arrow")

    def construct(self) -> None:
        self.setup_frame()
        xs = [-4.6, -2.75, -0.9, 0.95, 2.8, 4.65]
        labs = ["i", "ii", "iii", "iv", "v", "vi"]
        occ = [("ud", ""), ("", "ud"), ("u", "d"), ("d", "u"), ("u", "u"), ("d", "d")]
        ms = ["0", "0", "0", "0", "+1", "-1"]
        y0 = -0.35
        empty = m.VGroup(*[m.VGroup(level(x, y0, 1.0), level(x, y0 + 1.15, 1.0)) for x in xs])
        heads = m.VGroup(*[T(l, 32, GOLD, font="EB Garamond", slant="ITALIC").move_to([x, y0 + 1.85, 0])
                           for x, l in zip(xs, labs)])
        msl = m.VGroup(*[M(f"M_S={v}", size=28, color=MUTED).move_to([x, y0 - 0.65, 0]) for x, v in zip(xs, ms)])
        orb = m.VGroup(M(r"\pa", size=34).move_to([xs[0] - 1.05, y0, 0]), M(r"\pb", size=34).move_to([xs[0] - 1.05, y0 + 1.15, 0]))
        fills = [config(x, y0, lo, up)[2:] for x, (lo, up) in zip(xs, occ)]
        groups = [((xs[0], xs[1]), "closed shells", BLUE), ((xs[2], xs[3]), "open shell, $M_S=0$", VIOLET),
                  ((xs[4], xs[5]), "high spin", ROSE)]
        braces = m.VGroup()
        for (a, b), text, col in groups:
            line = m.Line([a - 0.55, y0 - 1.05, 0], [b + 0.55, y0 - 1.05, 0])
            br = m.Brace(line, m.DOWN, color=col)
            braces.add(m.VGroup(br, rich(text, 28, col).next_to(br, m.DOWN, buff=0.08)))
        count = rich(r"four spin orbitals $\pa\alpha,\pa\beta,\pb\alpha,\pb\beta$; choose 2 of 4 $\Rightarrow\binom42=6$ "
                     r"determinants", 30).move_to([0, -2.6, 0])
        self.say("[Now the heart of the matter: two electrons in two orbitals, phi a below and phi b above.] This is "
                 "Figure one of the review, rebuilt. There are exactly six ways to place the electrons.",
                 m.AnimationGroup(m.FadeIn(empty), m.FadeIn(heads), m.FadeIn(orb), m.FadeIn(msl)))
        self.say("[In arrangement one, both electrons sit in phi a with opposite spins.] [In arrangement two, both "
                 "sit in phi b.]", m.FadeIn(fills[0]), m.FadeIn(fills[1]))
        self.say("[In three, phi a holds an up spin and phi b a down spin.] [Four is the same with the spins "
                 "exchanged.] All four of these have M S equal to zero.", m.FadeIn(fills[2]), m.FadeIn(fills[3]))
        self.say("[In five, both spins point up, so M S is plus one,] [and in six both point down, so M S is minus "
                 "one.]", m.FadeIn(fills[4]), m.FadeIn(fills[5]))
        self.say("[One and two are closed shells. Three and four are open shells with M S equal to zero. Five and "
                 "six are high spin.]", m.LaggedStart(*[m.FadeIn(b) for b in braces], lag_ratio=0.3))
        self.say("[Counting confirms there are no others: there are four spin orbitals, phi a alpha, phi a beta, "
                 "phi b alpha and phi b beta, and choosing two of four gives six determinants.]", m.FadeIn(count))
        self.wait(0.4)


class S19PaperFig1(Frame):
    """05-two-electrons.tex, frame 2: 'The paper's Figure 1'."""

    TITLE = "The paper's Figure 1"
    SYMBOLS = r"“secondary spin quantum number” $=M_S$, the projection of the total spin on the $z$ axis"

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig01_two_electron_determinants.png", height=4.6, max_width=6.6).move_to([-3.35, 0.0, 0])
        claim = boxed('"Various arrangements (determinants) of two electrons in two molecular orbitals and the '
                      'corresponding values of the secondary spin quantum number." — p. 441', "claim", width=5.8,
                      size=28).move_to([3.65, 0.6, 0])
        ok = rich("Matches our reconstruction. Now write each one out.", 30, GREEN, width=5.6)
        ok.next_to(claim, m.DOWN, buff=0.4).align_to(claim, m.LEFT)
        self.say("[Here is the review's own Figure one,] [with its caption: various arrangements, or determinants, of "
                 "two electrons in two molecular orbitals and the corresponding values of the secondary spin quantum "
                 "number.] That secondary spin quantum number is M S.", m.FadeIn(fig, shift=m.RIGHT * 0.2),
                 m.FadeIn(claim))
        self.say("[It matches our reconstruction exactly. Now let us write each determinant out in full.]",
                 m.FadeIn(ok))
        self.wait(0.4)


class S20WriteOut(Frame):
    """05-two-electrons.tex, frame 3: 'Writing the determinants out'."""

    TITLE = "Writing the determinants out"
    SYMBOLS = (r"$D_{\text{X}}$: unnormalised determinant of row X; its normalised form is $\tfrac1{\sqrt2}D$ — "
               r"$\pa(1)$: orbital $\pa$ at electron 1's position $\mathbf r_1$ — $\alpha_1\beta_2$: electron 1 up, "
               r"electron 2 down")

    def construct(self) -> None:
        self.setup_frame()
        short = M(r"\text{shorthand:}\quad", r"A", r"\equiv\pa(1)\pb(2),\qquad", r"B", r"\equiv\pb(1)\pa(2)", size=34)
        paint_parts(short, AB)
        short.move_to([0, 2.25, 0])
        rows_tex = [("i", r"\pa\alpha,\ \pa\beta", [r"\pa(1)\pa(2)\,(\alpha_1\beta_2-\beta_1\alpha_2)"]),
                    ("ii", r"\pb\alpha,\ \pb\beta", [r"\pb(1)\pb(2)\,(\alpha_1\beta_2-\beta_1\alpha_2)"]),
                    ("iii", r"\pa\alpha,\ \pb\beta", ["A", r"\,\alpha_1\beta_2-", "B", r"\,\beta_1\alpha_2"]),
                    ("iv", r"\pa\beta,\ \pb\alpha", ["A", r"\,\beta_1\alpha_2-", "B", r"\,\alpha_1\beta_2"]),
                    ("v", r"\pa\alpha,\ \pb\alpha", ["(", "A", "-", "B", r")\,\alpha_1\alpha_2"]),
                    ("vi", r"\pa\beta,\ \pb\beta", ["(", "A", "-", "B", r")\,\beta_1\beta_2"])]
        head = m.VGroup(rich("Row", 30, MUTED), rich(r"spin orbitals $\chi_1,\chi_2$", 30, MUTED),
                        rich(r"$D=\chi_1(1)\chi_2(2)-\chi_2(1)\chi_1(2)$", 30, MUTED))
        cols = [-5.0, -3.2, 1.2]
        for h, x in zip(head, cols):
            h.move_to([x, 1.5, 0])
        head[1].align_to([cols[1] - 1.0, 0, 0], m.LEFT)
        head[2].align_to([cols[2] - 2.3, 0, 0], m.LEFT)
        table = []
        for k, (lab, so, dd) in enumerate(rows_tex):
            y = 0.95 - 0.52 * k
            a = T(lab, 30, GOLD, font="EB Garamond", slant="ITALIC").move_to([cols[0], y, 0])
            b = M(so, size=32).move_to([cols[1], y, 0]).align_to([cols[1] - 1.0, 0, 0], m.LEFT)
            c = M(*dd, size=32)
            paint_parts(c, AB)
            c.move_to([cols[2], y, 0]).align_to([cols[2] - 2.3, 0, 0], m.LEFT)
            table.append(m.VGroup(a, b, c))
        rule = m.Line([-5.6, 1.22, 0], [6.4, 1.22, 0], stroke_width=1.5, color=MUTED)
        eg = M(r"\text{e.g. iii: }\chi_1=\pa\alpha,\ \chi_2=\pb\beta:\quad \pa(1)\alpha_1\,\pb(2)\beta_2-\pb(1)\beta_1\,\pa(2)\alpha_2",
               size=32).move_to([0, -2.15, 0])
        e = explain("in each product the spatial part and the spin part of the same electron travel together",
                    width=11.0).next_to(eg, m.DOWN, buff=0.18)
        self.say("[To keep the algebra readable, write A for phi a of electron one times phi b of electron two, and B "
                 "for the same orbitals with the electrons swapped.]", m.FadeIn(short))
        self.say("[A determinant is chi one of electron one times chi two of electron two, minus the swapped product.] "
                 "[For row one, the spin orbitals are phi a alpha and phi a beta, so both electrons share phi a and the "
                 "spin part is alpha one beta two minus beta one alpha two.] [Row two is the same with phi b.]",
                 m.AnimationGroup(m.FadeIn(head), m.Create(rule)), m.FadeIn(table[0]), m.FadeIn(table[1]))
        self.say("[Row three uses phi a alpha and phi b beta. Written out, that is phi a of one alpha one, phi b of two "
                 "beta two, minus phi b of one beta one, phi a of two alpha two:] [in shorthand, A alpha one beta two "
                 "minus B beta one alpha two.] Notice that in each product the spatial part and the spin part of the "
                 "same electron travel together.",
                 m.AnimationGroup(m.FadeIn(eg), m.FadeIn(e)), m.FadeIn(table[2]))
        self.say("[Row four, with the spins exchanged, is A beta one alpha two minus B alpha one beta two.]",
                 m.FadeIn(table[3]))
        self.say("[Rows five and six have both spins equal, so the spin part factors out: A minus B, times alpha one "
                 "alpha two, or times beta one beta two.]", m.AnimationGroup(m.FadeIn(table[4]), m.FadeIn(table[5])))
        self.wait(0.4)


class S21HighSpin(Frame):
    """05-two-electrons.tex, frame 4: 'M_S = ±1: one determinant each'."""

    TITLE = r"$M_S=\pm1$: one determinant each"
    SYMBOLS = (r"$^3\Psi$: triplet, $2S+1=3$ — one determinant already factorises into space times a spin function of "
               r"definite $S$ — $\tfrac1{\sqrt2}$ normalises $A-B$, since $\braket{A-B}{A-B}=2$")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\tfrac1{\sqrt2}D_{\text v}", r"=\underbrace{\tfrac1{\sqrt2}\bigl[\pa(1)\pb(2)-\pb(1)\pa(2)\bigr]}_{\text{antisymmetric space}}"
             r"\;\underbrace{\alpha_1\alpha_2}_{\Theta_{1,+1} }", r"row v: $(A-B)\,\alpha_1\alpha_2$"),
            (r"\tfrac1{\sqrt2}D_{\text{vi}}", r"=\tfrac1{\sqrt2}\bigl[\pa(1)\pb(2)-\pb(1)\pa(2)\bigr]\;\beta_1\beta_2",
             "same space, both spins down"),
        ], size=38, why_size=26).move_to([0, 1.2, 0])
        claim = boxed(r'"$^3\Psi(M_s=+1)=\tfrac1{\sqrt2}[\pa(1)\pb(2)-\pb(1)\pa(2)][\alpha_1\alpha_2]$" … "i.e., they can '
                      r'be represented as single determinants v and vi" — p. 441; $M_s=-1$ analogous with $\beta_1\beta_2$',
                      "claim", width=11.5, size=28).move_to([0, -1.2, 0])
        ok = m.VGroup(pill("verified"), rich("exactly right: the high-spin triplet components are single-reference.", 30,
                                             GOLD)).arrange(m.RIGHT, buff=0.3).move_to([0, -2.45, 0])
        self.say("[Row five, normalised, is one over root two times the antisymmetric space function A minus B, times "
                 "alpha one alpha two.] That is a triplet spin function with M S equal to plus one. So a single "
                 "determinant is already a product of a spatial part and a spin eigenfunction.", m.FadeIn(d.rows[0]))
        self.say("[Row six is the same spatial function with both spins down: the M S equals minus one component.]",
                 m.FadeIn(d.rows[1]))
        self.say("[The review says exactly this: the triplet with M S equal to plus one is one over root two times phi "
                 "a of one phi b of two minus phi b of one phi a of two, times alpha one alpha two, and these states "
                 "can be represented as the single determinants five and six.]", m.FadeIn(claim))
        self.say("[That is exactly right: the high-spin components of the triplet are single-reference.]",
                 m.FadeIn(ok))
        self.wait(0.4)


class S22NotEigen(Frame):
    """05-two-electrons.tex, frame 5: 'M_S = 0: iii and iv are not spin eigenfunctions'."""

    TITLE = r"$M_S=0$: iii and iv are not spin eigenfunctions"
    SYMBOLS = (r"$\Theta$: a spin eigenfunction, of definite $S$ — $\lambda$: a would-be eigenvalue — eigenfunction: "
               r"$\hat S^2f=\lambda f$ with the same $f$ on both sides")

    def construct(self) -> None:
        self.setup_frame()
        Diii = M(r"D_{\text{iii}}=", "A", r"\,\underbrace{\alpha_1\beta_2}_{\text{not }\Theta}-", "B",
                 r"\,\underbrace{\beta_1\alpha_2}_{\text{not }\Theta}", size=42)
        paint_parts(Diii, AB)
        Diii.move_to([-2.4, 1.6, 0])
        from_spin = rich("From the spin frames:", 30, GOLD).move_to([-2.4, 0.35, 0]).align_to(Diii, m.LEFT)
        s2 = M(r"\hat S^2\alpha_1\beta_2=\alpha_1\beta_2+\beta_1\alpha_2\neq\lambda\,\alpha_1\beta_2", size=38)
        s2.next_to(from_spin, m.DOWN, buff=0.25).align_to(Diii, m.LEFT)
        half = rich("so $D_{\\text{iii}}$ is half singlet, half triplet. Only combinations of iii and iv have definite "
                    "spin.", 30, width=7.6).next_to(s2, m.DOWN, buff=0.35).align_to(Diii, m.LEFT)
        pic = m.VGroup(config(3.6, 0.4, "u", "d"), config(5.6, 0.4, "d", "u"))
        pm = M(r"\pm", size=40).move_to([4.6, 0.95, 0])
        names = m.VGroup(T("iii", 28, MUTED).move_to([3.6, -0.05, 0]), T("iv", 28, MUTED).move_to([5.6, -0.05, 0]))
        q = rich("+ or − ?", 32, GOLD).move_to([4.6, -0.6, 0])
        e = explain(r"half and half: $\alpha_1\beta_2=\tfrac1{\sqrt2}(\Theta_{1,0}+\Theta_{0,0})$, so "
                    r"$\langle\hat S^2\rangle=\tfrac12\cdot2+\tfrac12\cdot0=1$; T1b measures exactly 1", width=12.5)
        e.move_to([0, -2.45, 0])
        self.say("[Now the M S equals zero determinants. Row three is A times alpha one beta two, minus B times beta "
                 "one alpha two.]", m.Write(Diii))
        self.say("[But neither spin product is a spin eigenfunction. From the spin frames, S squared turns alpha one "
                 "beta two into alpha one beta two plus beta one alpha two, which is not a multiple of alpha one beta "
                 "two.]", m.AnimationGroup(m.FadeIn(from_spin), m.FadeIn(s2)))
        self.say("[So determinant three is half singlet and half triplet, and only combinations of three and four can "
                 "have a definite spin.]", m.AnimationGroup(m.FadeIn(half), m.FadeIn(pic), m.FadeIn(pm),
                                                            m.FadeIn(names)))
        self.say("[Half and half is literal: alpha one beta two equals one over root two times the sum of theta one "
                 "zero and theta zero zero, so the expectation value of S squared is one half times two plus one half "
                 "times zero, which is one.] Test T one b measures exactly one.", m.FadeIn(e))
        self.say("[The question is: plus or minus? Which combination is the singlet?]", m.Write(q))
        self.wait(0.4)


class S23Sum(Frame):
    """05-two-electrons.tex, frame 6: 'The sum D_iii + D_iv, every term tracked'."""

    TITLE = r"The sum $D_{\text{iii}}+D_{\text{iv}}$, every term tracked"
    SYMBOLS = (r"$A=\pa(1)\pb(2)$, $B=\pb(1)\pa(2)$ — $A-B$ changes sign under $1\leftrightarrow2$, antisymmetric — "
               r"$\Theta_{1,0}=\tfrac1{\sqrt2}(\alpha_1\beta_2+\beta_1\alpha_2)$: triplet, $M_S=0$")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"D_{\text{iii}}+D_{\text{iv}}",
             ["=", "A", r"\,\alpha_1\beta_2-", "B", r"\,\beta_1\alpha_2+", "A", r"\,\beta_1\alpha_2-", "B",
              r"\,\alpha_1\beta_2"], "rows iii, iv"),
            ("", ["=", "A", r"\,(\alpha_1\beta_2+\beta_1\alpha_2)-", "B", r"\,(\beta_1\alpha_2+\alpha_1\beta_2)"],
             "collect $A$, $B$"),
            ("", ["=(", "A", "-", "B", r")\,(\alpha_1\beta_2+\beta_1\alpha_2)"], "same bracket"),
            ("", [r"=\underbrace{\bigl[\pa(1)\pb(2)-\pb(1)\pa(2)\bigr]}_{\text{antisymmetric space}}"
                  r"\underbrace{(\alpha_1\beta_2+\beta_1\alpha_2)}_{\sqrt2\,\Theta_{1,0} }"], "put $A$, $B$ back"),
        ], size=36)
        for row in d.rows:
            paint_parts(row[1], AB)
        d.next_to(self.title_group, m.DOWN, buff=0.45).set_x(0)
        result = Box(rich(r"antisymmetric space $\times$ symmetric spin: the sum is the $M_S=0$ triplet.", 30), "result")
        result.next_to(d, m.DOWN, buff=0.45)
        self.say("Let us add the two determinants, keeping track of every term.")
        self.say("[Expanding determinants three and four gives four products: A alpha one beta two, minus B beta "
                 "one alpha two, plus A beta one alpha two, minus B alpha one beta two.]",
                 m.AnimationGroup(m.Write(m.VGroup(d.rows[0][0], d.rows[0][1])), m.FadeIn(d.rows[0][2])))
        self.say("[Collect the terms that multiply A, and the terms that multiply B.]",
                 m.AnimationGroup(m.FadeIn(d.rows[1][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[1][2])))
        self.say("Both brackets hold the same spin function, [so it factors out: A minus B, times alpha one beta "
                 "two plus beta one alpha two.]",
                 m.AnimationGroup(m.FadeIn(d.rows[2][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[2][2])))
        self.say("[Now put A and B back.] The spatial factor changes sign when the two electrons swap places, [so it "
                 "is antisymmetric.] The spin factor is root two times theta one zero, [the symmetric triplet "
                 "function with M S equal to zero.]",
                 m.AnimationGroup(m.FadeIn(d.rows[3][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[3][2])),
                 m.Indicate(d.rows[3][1], color=ROSE, scale_factor=1.03),
                 m.Indicate(d.rows[3][1], color=CYAN, scale_factor=1.03))
        self.say("[An antisymmetric space times a symmetric spin is a triplet.] So the sum of determinants three "
                 "and four is the M S equals zero component of the triplet, not the open-shell singlet.",
                 m.FadeIn(result, shift=m.UP * 0.15))
        self.wait(0.4)


class S24Difference(Frame):
    """05-two-electrons.tex, frame 7: 'The difference D_iv − D_iii'."""

    TITLE = r"The difference $D_{\text{iv}}-D_{\text{iii}}$"
    SYMBOLS = (r"$A+B$ is unchanged under $1\leftrightarrow2$, symmetric — $\Theta_{0,0}=\tfrac1{\sqrt2}(\alpha_1\beta_2-"
               r"\beta_1\alpha_2)$: singlet; $\beta_1\alpha_2-\alpha_1\beta_2=-\sqrt2\,\Theta_{0,0}$, and the overall sign "
               r"of a state is irrelevant")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"D_{\text{iv}}-D_{\text{iii}}",
             ["=", "A", r"\,\beta_1\alpha_2-", "B", r"\,\alpha_1\beta_2-", "A", r"\,\alpha_1\beta_2+", "B",
              r"\,\beta_1\alpha_2"], "iv minus iii"),
            ("", ["=", "A", r"\,(\beta_1\alpha_2-\alpha_1\beta_2)+", "B", r"\,(\beta_1\alpha_2-\alpha_1\beta_2)"],
             "collect $A$ and $B$"),
            ("", ["=(", "A", "+", "B", r")\,(\beta_1\alpha_2-\alpha_1\beta_2)"], "common bracket"),
            ("", [r"=\underbrace{\bigl[\pa(1)\pb(2)+\pb(1)\pa(2)\bigr]}_{\text{symmetric space}}"
                  r"\underbrace{(\beta_1\alpha_2-\alpha_1\beta_2)}_{-\sqrt2\,\Theta_{0,0} }"], "put $A$, $B$ back"),
        ], size=36)
        for row in d.rows:
            paint_parts(row[1], AB)
        d.next_to(self.title_group, m.DOWN, buff=0.45).set_x(0)
        result = Box(rich(r"symmetric space $\times$ antisymmetric spin: the difference is the open-shell singlet.", 30),
                     "result")
        result.next_to(d, m.DOWN, buff=0.45)
        self.say("Now the difference: determinant four minus determinant three.")
        self.say("[Four is A beta one alpha two minus B alpha one beta two; subtracting three gives minus A alpha one "
                 "beta two plus B beta one alpha two.]",
                 m.AnimationGroup(m.Write(m.VGroup(d.rows[0][0], d.rows[0][1])), m.FadeIn(d.rows[0][2])))
        self.say("[Collect A and B: each multiplies beta one alpha two minus alpha one beta two.]",
                 m.AnimationGroup(m.FadeIn(d.rows[1][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[1][2])))
        self.say("[So the common bracket factors out, now with A plus B.]",
                 m.AnimationGroup(m.FadeIn(d.rows[2][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[2][2])))
        self.say("[Put A and B back.] [The spatial part, A plus B, does not change when the electrons swap: it is "
                 "symmetric.] [The spin part is minus root two times theta zero zero, the antisymmetric singlet.] The "
                 "overall minus sign of a state is irrelevant.",
                 m.AnimationGroup(m.FadeIn(d.rows[3][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[3][2])),
                 m.Indicate(d.rows[3][1], color=BLUE, scale_factor=1.03),
                 m.Indicate(d.rows[3][1], color=CYAN, scale_factor=1.03))
        self.say("[A symmetric space times an antisymmetric spin: the difference is the open-shell singlet.]",
                 m.FadeIn(result, shift=m.UP * 0.15))
        self.wait(0.4)


class S25Normalisation(Frame):
    """05-two-electrons.tex, frame 8: 'Normalisation'."""

    TITLE = "Normalisation"
    SYMBOLS = (r"$\braket fg=\iint f^*g\,\dd\mathbf r_1\dd\mathbf r_2$, with spin sums for spin functions — "
               r"$\|f\|^2=\braket ff$ — $^3\Psi_0$: triplet, $M_S=0$ — $^1\Psi_{\OSS}$: open-shell singlet")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\braket{A\pm B}{A\pm B}", r"=\braket AA+\braket BB\pm2\braket AB", "expand"),
            (r"\braket AA", r"=\braket{\pa}{\pa}\braket{\pb}{\pb}=1", "split the integrals"),
            (r"\braket AB", r"=\braket{\pa}{\pb}\braket{\pb}{\pa}=0\cdot0=0", "orthogonal"),
            (r"\Rightarrow\ \braket{A\pm B}{A\pm B}", r"=2", ""),
        ], size=34, why_size=26).move_to([-2.3, 1.0, 0])
        need = rich(r"each combination needs $\tfrac1{\sqrt2}\cdot\tfrac1{\sqrt2}=\tfrac12$", 32).move_to([-1.7, -1.05, 0])
        e = explain(r"spin part likewise: $\|\alpha_1\beta_2\pm\beta_1\alpha_2\|^2=2$; one $\tfrac1{\sqrt2}$ for space, "
                    r"one for spin", width=8.0).next_to(need, m.DOWN, buff=0.25)
        res = Box(M(r"{}^3\Psi_0&=\tfrac12(D_{\text{iii}}+D_{\text{iv}})\\ {}^1\Psi_{\OSS}&=\tfrac12(D_{\text{iv}}-D_{\text{iii}})",
                    size=36), "result").move_to([4.95, -1.3, 0])
        self.say("[To normalise, compute the squared norm of A plus or minus B: the norm of A, plus the norm of B, "
                 "plus or minus twice their overlap.]", m.FadeIn(d.rows[0]))
        self.say("[The norm of A splits into the product of the two orbital integrals, each one, because the orbitals "
                 "are normalised.]", m.FadeIn(d.rows[1]))
        self.say("[The overlap of A and B splits into phi a with phi b, times phi b with phi a, and each of those is "
                 "zero, because the orbitals are orthogonal.]", m.FadeIn(d.rows[2]))
        self.say("[So the squared norm is two, for both signs.]", m.FadeIn(d.rows[3]))
        self.say("[The spin parts also have squared norm two, so each combination needs one over root two for space "
                 "and one over root two for spin: a factor of one half overall.]",
                 m.AnimationGroup(m.FadeIn(need), m.FadeIn(e)))
        self.say("[The results: the triplet with M S equal to zero is one half times D three plus D four, and the "
                 "open-shell singlet is one half times D four minus D three.]", m.FadeIn(res))
        self.wait(0.4)


class S26ReadPaper(Frame):
    """05-two-electrons.tex, frame 9: 'Now read the paper'."""

    TITLE = "Now read the paper"
    SUBTITLE = "spot the difference"
    SYMBOLS = (r"the paper writes each determinant with rows for electrons 1 and 2 and columns for spin orbitals, exactly "
               r"our $D_{\text{iii}}$ and $D_{\text{iv}}$; its prefactor $\tfrac1{\sqrt2}\cdot\tfrac1{\sqrt2}=\tfrac12$ "
               r"matches ours")

    def construct(self) -> None:
        self.setup_frame()
        shot = figure("sign_error_raw.png", height=4.2).move_to([0, 0.35, 0])
        cap = rich("Line 1, the product form … then “is a combination of two determinants, iii and iv:”", 30,
                   width=12.0).move_to([0, -2.35, 0])
        self.say("[Now read what the review prints on page four hundred forty one.]",
                 m.FadeIn(shot, shift=m.UP * 0.15))
        self.say("[The first line gives the open-shell singlet in product form: one over root two times phi a of one "
                 "phi b of two plus phi b of one phi a of two, times one over root two times beta one alpha two minus "
                 "alpha one beta two.] Then the text says it is a combination of two determinants, three and four. "
                 "The determinants are written exactly as ours, and the prefactor, one over root two times one over "
                 "root two, is our one half. Look closely at the sign between them.", m.FadeIn(cap))
        self.wait(0.6)


class S27Spotted(Frame):
    """05-two-electrons.tex, frame 10: 'Spotted it'."""

    TITLE = "Spotted it"
    SYMBOLS = (r"the two lines contradict each other: line 1, green, equals $\tfrac12(D_{\text{iv}}-D_{\text{iii}})$; "
               r"line 2, rose, does not")

    def construct(self) -> None:
        self.setup_frame()
        shot = figure("sign_error_marked.png", height=4.4).move_to([-2.6, 0.2, 0])
        g = m.VGroup(rich("green: product form, symmetric space × antisymmetric spin", 28, GREEN, width=4.6),
                     pill("verified")).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15)
        r = m.VGroup(rich(r"rose: $\tfrac12(D_{\text{iii}}+D_{\text{iv}})$ is what we just proved to be the triplet", 28,
                          ROSE, width=4.6), pill("error")).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15)
        err = Box(rich(r"should read $\;\tfrac12(D_{\text{iv}}-D_{\text{iii}})$", 32), "erratum")
        col = m.VGroup(g, r, err).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.45).move_to([4.15, 0.2, 0])
        self.say("[Here it is, marked.]", m.FadeIn(shot))
        self.say("[In green, the product form: symmetric space times antisymmetric spin. That is the open-shell "
                 "singlet, and it is correct.]", m.FadeIn(g))
        self.say("[In rose, the expansion: one half times determinant three plus determinant four. That plus sign "
                 "makes it exactly the combination we just proved to be the triplet.] The two printed lines "
                 "contradict each other.", m.FadeIn(r))
        self.say("[The expansion should read one half times determinant four minus determinant three.]",
                 m.FadeIn(err))
        self.wait(0.6)


class S28LiveInPrint(Frame):
    """05-two-electrons.tex, frame 11: 'Fluctuating multiplicity, live in print'."""

    TITLE = "Fluctuating multiplicity, live in print"

    def construct(self) -> None:
        self.setup_frame()
        plus = T("+", 150, ROSE, font="TeX Gyre Chorus").move_to([-2.6, 1.1, 0])
        minus = m.Rectangle(width=0.9, height=0.13, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([2.6, 1.1, 0])
        arr = m.Arrow([-1.6, 1.1, 0], [1.6, 1.1, 0], color=GOLD, stroke_width=4, buff=0)
        lab = T("one character", 28, GOLD).next_to(arr, m.UP, buff=0.12)
        s1 = M("S=1", size=36, color=ROSE).next_to(plus, m.DOWN, buff=0.3)
        s0 = M("S=0", size=36, color=GREEN).next_to(minus, m.DOWN, buff=0.3)
        l1 = rich("The section is titled “Fluctuating ground-state multiplicity” …", 36, width=12).move_to([0, -0.95, 0])
        l2 = rich("… and between two lines the open-shell singlet fluctuates into a triplet.", 36, GOLD,
                  width=12).move_to([0, -1.75, 0])
        joke = rich("It survived peer review and typesetting. Two referees with parallel spins, presumably: the Fermi "
                    "hole kept them from ever meeting the error.", 28, MUTED, width=12).move_to([0, -2.6, 0])
        self.say("[One character, a plus instead of a minus, turns a spin of zero into a spin of one.]",
                 m.AnimationGroup(m.FadeIn(plus), m.FadeIn(s1), m.GrowArrow(arr), m.FadeIn(lab), m.FadeIn(minus),
                                  m.FadeIn(s0)))
        self.say("[The section of the review is titled Fluctuating ground-state multiplicity,] [and between two lines, "
                 "the open-shell singlet fluctuates into a triplet.]", m.FadeIn(l1), m.FadeIn(l2))
        self.say("[It survived peer review and typesetting. Two referees with parallel spins, presumably: the Fermi "
                 "hole kept them from ever meeting the error.]", m.FadeIn(joke))
        self.wait(0.6)


def code(text: str, lang: str | None = None, width: float | None = None) -> m.Mobject:
    c = m.Code(code_string=text, language=lang, add_line_numbers=False, background="rectangle")
    if width is not None and c.width > width:
        c.scale_to_fit_width(width)
    return c


class S29ThreeWays(Frame):
    """05-two-electrons.tex, frame 12: 'Checked three ways: SymPy, Ŝ², Lean'."""

    TITLE = r"Checked three ways: SymPy, $\hat S^2$, Lean"
    SYMBOLS = (r"T1b builds the two-electron wavefunctions as numerical tensors from random orthonormal orbitals and "
               r"applies $\hat S^2=(\hat{\mathbf s}_1+\hat{\mathbf s}_2)^2$ directly: no algebra is shared with T1 — "
               r"$\langle S^2\rangle=S(S+1)$: 2 triplet, 0 singlet")

    def construct(self) -> None:
        self.setup_frame()
        # recorded output and proof source, read from the repository at render time (not retyped)
        h1 = rich("SymPy, T1: symbolic expansion", 32, GOLD)
        c1 = excerpt("verification/results/t01_spin_and_determinants.txt", 7, 9, width=12.4, numbers=False)
        p1 = m.Group(h1, c1).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3).move_to([0, 0.3, 0])
        h2 = rich(r"$\hat S^2$ as an operator, T1b: the paper's determinants on a grid", 32, GOLD)
        t1b = t1b_table()
        p2 = m.Group(h2, t1b).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3).move_to([0, 0.3, 0])
        h3 = rich("Lean 4 + Mathlib, T17: machine-checked", 32, GOLD)
        c3 = m.Group(excerpt("verification/lean_proofs/Ch5103/Identities.lean", 25, 27, width=12.4),
                     excerpt("verification/lean_proofs/Ch5103/Identities.lean", 38, 42, width=12.4))
        c3.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.2)
        p3 = m.Group(h3, c3).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3).move_to([0, 0.2, 0])
        self.say("[We checked this three independent ways. First, test T one expands the determinants symbolically in "
                 "SymPy: the triplet equals one half of three plus four, the singlet equals one half of four minus "
                 "three, and the paper's version is not the singlet.]", m.FadeIn(p1))
        self.play(m.FadeOut(p1), run_time=0.5)
        self.say("[Second, test T one b shares no algebra with the first. It builds both wavefunctions as numerical "
                 "tensors from random orthonormal orbitals, exactly as the paper prints the determinants, and applies "
                 "the total spin operator directly.] The paper's combination gives an S squared of two, a triplet; "
                 "the corrected one gives zero, a singlet; determinant three alone is half and half, with expectation "
                 "one; and the paper's own product form also gives zero.", m.FadeIn(p2))
        self.play(m.FadeOut(p2), run_time=0.5)
        self.say("[Third, the Lean proof assistant checks it formally. The theorem sum is triplet proves that D three "
                 "plus D four equals A minus B times the symmetric spin sum, by unfolding the definitions and ring "
                 "arithmetic. A second theorem proves the printed plus version cannot be the singlet: it plugs in one "
                 "counterexample and simplifies.]", m.FadeIn(p3))
        self.wait(0.6)


def t1b_table() -> m.VGroup:
    """T1b's four classifications as a table, parsed from verification/results/t01b_sign_error_numeric.txt."""
    import re

    path = ROOT / "verification" / "results" / "t01b_sign_error_numeric.txt"
    rows = [m.VGroup(rich("**combination**", 26, GOLD), rich(r"**$\langle S^2\rangle$**", 26, GOLD),
                     rich("**eigen-residual**", 26, GOLD), rich("**verdict**", 26, GOLD))]
    for line in path.read_text(encoding="utf-8").splitlines()[:4]:
        mm = re.match(r"(.+?)\s+<S\^2> = (\S+)\s+eigen-residual = (\S+)\s+antisymmetric = \S+\s+-> (.+)$", line)
        name, s2, res, verdict = mm.groups()
        rows.append(m.VGroup(rich(f"`{name.strip()}`", 28), rich(f"`{s2}`", 28), rich(f"`{res}`", 28),
                             rich(verdict, 25, GREEN if "SINGLET" in verdict else ROSE if "TRIPLET" in verdict else MUTED)))
    xs = [-6.2, -1.2, 2.0, 4.4]
    y = 0.0
    for row in rows:
        for c, x in zip(row, xs):
            c.move_to([x + c.width / 2, y, 0])
        y -= 0.5
    return m.VGroup(*rows)


class S30Teaches(Frame):
    """05-two-electrons.tex, frame 13: 'What the two-electron problem teaches'."""

    TITLE = "What the two-electron problem teaches"
    SYMBOLS = (r"single-reference: one determinant is a good starting point, and the high-spin component suffices — "
               r"multireference: several determinants with comparable weights are needed from the start")

    def construct(self) -> None:
        self.setup_frame()
        b = bullets(["three singlets: i, ii and the open-shell singlet", "one triplet, with three $M_S$ components",
                     r"triplet $M_S=\pm1$: single determinants v and vi; $M_S=0$ needs iii + iv",
                     r"open-shell singlet: irreducibly two determinants, for every $M_S$"], width=6.4, size=30)
        b.move_to([-3.3, 0.3, 0])
        claim = boxed('"their triplet state is therefore accurately described by a single reference determinant, '
                      'however open-shell singlets require multiconfigurational (multireference) treatment." — p. 441',
                      "claim", width=5.9, size=28).move_to([3.55, 0.65, 0])
        ok = m.VGroup(pill("verified"), rich("conclusion right, despite the typo", 30)).arrange(m.RIGHT, buff=0.25)
        ok.next_to(claim, m.DOWN, buff=0.4)
        self.say("[To sum up the two-electron problem. There are three singlets: the two closed shells, one and two, "
                 "and the open-shell singlet.]", m.FadeIn(b[0]))
        self.say("[There is one triplet, with three M S components.]", m.FadeIn(b[1]))
        self.say("[Its M S equals plus and minus one components are single determinants, five and six, while its M S "
                 "equals zero component needs three plus four.]", m.FadeIn(b[2]))
        self.say("[The open-shell singlet is irreducibly two determinants, whatever M S you choose: there is no "
                 "single-determinant component to fall back on.]", m.FadeIn(b[3]))
        self.say("[Hence the review's conclusion: the triplet is accurately described by a single reference "
                 "determinant, but open-shell singlets require a multiconfigurational, or multireference, treatment.]",
                 m.FadeIn(claim))
        self.say("[That conclusion is right, despite the typo.]", m.FadeIn(ok))
        self.wait(0.4)
