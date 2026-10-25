"""Chapter 6: Hund's rule, the virial theorem and less screening (presentation/sections/08-hund.tex)."""
import numpy as np

import manimgx as m

from ch01_foundations import explain
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, PANEL, ROSE, Box, Derivation, Frame, M, T, boxed, pill, rich)


def bar_chart(values: list[float], labels: list[str], colours: list[str], y_range: tuple[float, float],
              width: float, height: float, ylabel: str = "", fmt: str = "{:+.4f}", label_size: float = 30):
    """Vertical bars with a zero line, value labels and LaTeX x labels; returns (group, bars, value labels)."""
    lo, hi = y_range
    scale = height / (hi - lo)
    n = len(values)
    slot = width / n
    y0 = -height / 2 - lo * scale  # y of zero
    axis = m.Line([-width / 2, y0, 0], [width / 2, y0, 0], color=MUTED, stroke_width=2)
    yaxis = m.Line([-width / 2, -height / 2, 0], [-width / 2, height / 2, 0], color=MUTED, stroke_width=2)
    bars, vals, labs = m.VGroup(), m.VGroup(), m.VGroup()
    for k, (v, lab, col) in enumerate(zip(values, labels, colours)):
        x = -width / 2 + slot * (k + 0.5)
        h = abs(v) * scale
        bar = m.Rectangle(width=slot * 0.55, height=max(h, 0.01), stroke_width=0, fill_color=col, fill_opacity=1)
        bar.move_to([x, y0 + (h / 2 if v >= 0 else -h / 2), 0])
        bars.add(bar)
        t = M(fmt.format(v), size=24, color=FG)
        t.next_to(bar, m.UP if v >= 0 else m.DOWN, buff=0.08)
        vals.add(t)
        labs.add(M(lab, size=label_size, color=FG).move_to([x, -height / 2 - 0.35, 0]))
    ylab = rich(ylabel, 24, MUTED).rotate(m.PI / 2).next_to(yaxis, m.LEFT, buff=0.2) if ylabel else m.VGroup()
    return m.VGroup(axis, yaxis, labs, ylab), bars, vals


class S43TwoExplanations(Frame):
    """08-hund.tex, frame 1: 'Two explanations of the same rule'."""

    TITLE = "Two explanations of the same rule"
    SYMBOLS = (r"$\Delta X\equiv X(\text{triplet})-X(\text{singlet})$ — $T$: kinetic energy — $V_{ne}$: electron–nucleus "
               r"attraction, negative — $V_{ee}$: electron–electron repulsion, positive — screening: one electron's "
               r"charge partly cancelling the nucleus's pull on another")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('Slater\'s explanation: "less electron–electron Coulomb repulsion in the triplet state" … "However, … '
                      'the electron–electron repulsion is actually greater in the high-spin state" — hence the "less '
                      'screening rule", p. 442', "claim", width=12.6, size=28).move_to([0, 1.55, 0])
        sl = Box(m.VGroup(rich("Slater's argument, read with frozen orbitals", 30, GOLD),
                          M(r"\Delta V_{ee}=-2K<0,\ \Delta T=0,\ \Delta V_{ne}=0", size=34),
                          rich("triplet wins by lower repulsion", 28, MUTED)).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.18),
                 "plain", width=6.1)
        ls = Box(m.VGroup(rich("Less screening, relaxed orbitals", 30, GOLD),
                          M(r"\Delta V_{ee}>0,\ \Delta V_{ne}\ll0,\ \Delta T>0", size=34),
                          rich("triplet wins by stronger nuclear attraction", 28, MUTED)).arrange(m.DOWN, aligned_edge=m.LEFT,
                                                                                               buff=0.18), "plain", width=6.1)
        cols = m.VGroup(sl, ls).arrange(m.RIGHT, buff=0.4, aligned_edge=m.UP).move_to([0, -0.55, 0])
        q = rich("Which is right? The virial theorem plus the computed sign of $\\Delta V_{ee}$ decides.", 32, GOLD)
        q.move_to([0, -2.3, 0])
        self.say("[Hund's rule says the triplet is lower, but why? The review gives two explanations. Slater's original "
                 "explanation was less electron electron repulsion in the triplet state. However, the review continues, "
                 "the electron electron repulsion is actually greater in the high-spin state, and an alternative "
                 "explanation, the less screening rule, has been offered.]", m.FadeIn(claim))
        self.say("[Read with frozen orbitals, Slater's argument is exactly our result: the repulsion changes by minus two "
                 "K, while the kinetic energy and the nuclear attraction do not change. The triplet wins by lower "
                 "repulsion.]", m.FadeIn(sl))
        self.say("[In the less screening picture the orbitals relax. The repulsion goes up, the nuclear attraction "
                 "becomes much more negative, and the kinetic energy rises. The triplet wins by stronger nuclear "
                 "attraction.]", m.FadeIn(ls))
        self.say("[Which is right? The virial theorem, together with the computed sign of the change in repulsion, "
                 "decides.]", m.FadeIn(q))
        self.wait(0.4)


class S44Virial1(Frame):
    """08-hund.tex, frame 2: 'The virial theorem by scaling (1/2)'."""

    TITLE = "The virial theorem by scaling (1/2)"
    SUBTITLE = r"assume an atom, nucleus at the origin; $\Psi$ exact, or optimised with respect to scaling"
    SYMBOLS = (r"$\eta$: scaling factor, $\eta=1$ is the original $\Psi$ — $N$: number of electrons — $\dd^{3N}r$: all $3N$ "
               r"position coordinates — $\mathbf s$: rescaled coordinates")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\text{(1)}\ \Psi_\eta(\mathbf r_1,\ldots,\mathbf r_N)", r"=\eta^{3N/2}\,\Psi(\eta\mathbf r_1,\ldots,\eta\mathbf r_N)",
             r"squeeze, $\eta>1$, or stretch, $\eta<1$, the whole cloud"),
            (r"\text{(2)}\ \braket{\Psi_\eta}{\Psi_\eta}", r"=\eta^{3N}\!\int|\Psi(\eta\mathbf r)|^2\dd^{3N}r",
             "the prefactor appears squared"),
            ("", r"=\int|\Psi(\mathbf s)|^2\dd^{3N}s=1", r"substitute $\mathbf s=\eta\mathbf r$, $\dd^{3N}r=\eta^{-3N}\dd^{3N}s$"),
        ], size=36, why_gap=0.4).move_to([0, 0.75, 0])
        e1 = explain(r"the scaled function is still normalised, so it is a legal trial function at every $\eta$", width=12)
        e2 = explain(r"the factor $\eta^{3N/2}$ exists only to keep the norm one: three coordinates per electron, $N$ "
                     r"electrons", width=12)
        ex = m.VGroup(e1, e2).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15).move_to([0, -1.8, 0])
        self.say("The virial theorem decides between them, and it can be derived by scaling. Take an atom with the "
                 "nucleus at the origin, and a wavefunction that is exact, or at least optimised with respect to "
                 "scaling.")
        self.say("[Step one. Define a scaled wavefunction, Psi eta: multiply every electron coordinate by eta, and put a "
                 "prefactor eta to the three N over two in front. Eta greater than one squeezes the whole electron "
                 "cloud, eta less than one stretches it.]", m.FadeIn(d.rows[0]))
        self.say("[Step two. Its norm: the prefactor appears squared, giving eta to the three N times the integral of Psi "
                 "at eta r, squared.]", m.FadeIn(d.rows[1]))
        self.say("[Substitute s equals eta r. The volume element is eta to the minus three N times d s, which cancels "
                 "the prefactor, and the norm is one.]", m.FadeIn(d.rows[2]))
        self.say("[So the scaled function is still normalised and is a legal trial function for every eta.] [The "
                 "prefactor exists only to keep the norm one: three coordinates per electron, N electrons.]",
                 m.FadeIn(e1), m.FadeIn(e2))
        self.wait(0.4)


class S45Virial2(Frame):
    """08-hund.tex, frame 3: 'The virial theorem by scaling (2/2)'."""

    TITLE = "The virial theorem by scaling (2/2)"
    SYMBOLS = (r"$\ev T,\ev V$: expectation values of kinetic and total potential energy — $V=V_{ne}+V_{ee}$ for an atom — "
               r"virial ratio $-\ev V/\ev T=2$ — Lean: scaling\_derivative — molecules: the same at equilibrium geometries")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\text{(3)}\ \ev{T}_\eta", r"=\eta^2\ev T", r"$T$ has two derivatives; $\nabla_{\mathbf r}=\eta\nabla_{\mathbf s}$ each"),
            (r"\text{(4)}\ \ev{V}_\eta", r"=\eta\,\ev V", r"every Coulomb term is 1/distance: $\tfrac1r=\eta\tfrac1s$"),
            (r"\text{(5)}\ E(\eta)", r"=\eta^2\ev T+\eta\ev V", "add them"),
            (r"\text{(6)}\ \left.\frac{\dd E}{\dd\eta}\right|_{\eta=1}", r"=2\ev T+\ev V=0",
             "exact state: stationary under any variation"),
        ], size=38).move_to([0, 0.65, 0])
        res = Box(M(r"2\ev T+\ev V=0\quad\Longrightarrow\quad E=\ev T+\ev V=-\ev T=\tfrac12\ev V", size=40), "result")
        res.move_to([0, -2.05, 0])
        self.say("[Step three. The kinetic energy contains two derivatives, and each derivative with respect to r is eta "
                 "times a derivative with respect to s. So the kinetic energy of the scaled function is eta squared "
                 "times the original.]", m.FadeIn(d.rows[0]))
        self.say("[Step four. Every potential term is one over a distance, and one over r is eta times one over s. So the "
                 "potential energy scales with one power of eta.]", m.FadeIn(d.rows[1]))
        self.say("[Step five. Add them: the energy as a function of eta is eta squared times T plus eta times V.]",
                 m.FadeIn(d.rows[2]))
        self.say("[Step six. An exact state is stationary under any variation, including scaling, so the derivative at eta "
                 "equal to one vanishes: two T plus V equals zero.]", m.FadeIn(d.rows[3]))
        self.say("[That is the virial theorem. The total energy equals minus the kinetic energy, and also one half of the "
                 "potential energy.] It is proved in Lean as the theorem scaling derivative, and for molecules the same "
                 "holds at equilibrium geometries.", m.FadeIn(res))
        self.wait(0.4)


class S46FrozenFails(Frame):
    """08-hund.tex, frame 4: 'Frozen orbitals cannot be the mechanism'."""

    TITLE = "Frozen orbitals cannot be the mechanism"
    SYMBOLS = (r"same orbitals $\Rightarrow$ same $\langle T\rangle$, because $T$ is a one-electron operator summed over the "
               r"same occupied orbitals — exact states must obey $E=-\langle T\rangle$, so a different $E$ needs a "
               r"different $\langle T\rangle$")

    def construct(self) -> None:
        self.setup_frame()
        head = rich("Apply the virial theorem to both exact states and subtract:", 30).move_to([0, 2.2, 0])
        eq = M(r"\Delta E\equiv E_T-E_S=-\Delta\ev T=\tfrac12\bigl(\Delta\ev{V_{ne}}+\Delta\ev{V_{ee}}\bigr)", size=40)
        eq.move_to([0, 1.4, 0])
        s1 = rich(r"1. frozen-orbital model: the same orbitals in both states $\Rightarrow\Delta\ev T=0$", 30, width=12.4)
        s2 = rich(r"2. then the virial theorem forces $\Delta E=0$, but the same model gives $\Delta E=-2K<0$: a contradiction",
                  30, width=12.4)
        steps = m.VGroup(s1, s2).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.25).move_to([0, 0.25, 0])
        res = boxed("frozen orbitals violate the virial theorem: they cannot tell which energy component pays", "result",
                    width=12.4, size=30).move_to([0, -1.05, 0])
        hongo = rich("Hongo et al. 2004, full text: “This assumption leaves the kinetic energy T unchanged … which cannot be "
                     "correct as each eigenstate must satisfy the virial theorem.”", 26, MUTED, width=12.4)
        hongo.move_to([0, -2.3, 0])
        self.say("[Apply the virial theorem to both exact states and subtract. The energy difference equals minus the "
                 "kinetic energy difference, and also one half of the change in nuclear attraction plus the change in "
                 "repulsion.]", m.AnimationGroup(m.FadeIn(head), m.Write(eq)))
        self.say("[Now take the frozen-orbital model. If both states use the same orbitals, the kinetic energy is the "
                 "same, because it is a one-electron operator summed over the same occupied orbitals.]", m.FadeIn(s1))
        self.say("[Then the virial theorem forces the energy difference to be zero. But the same model says the triplet "
                 "is lower by two K. That is a contradiction.]", m.FadeIn(s2))
        self.say("[So frozen orbitals violate the virial theorem. They cannot tell us which energy component actually "
                 "pays for the splitting.]", m.FadeIn(res))
        self.say("[Hongo and coworkers make the same point: this assumption leaves the kinetic energy unchanged, which "
                 "cannot be correct, as each eigenstate must satisfy the virial theorem.]", m.FadeIn(hongo))
        self.wait(0.4)


class S47LessScreening(Frame):
    """08-hund.tex, frame 5: 'Less screening, as inequalities'."""

    TITLE = "Less screening, as inequalities"
    SUBTITLE = r"assume the triplet is lower, $\Delta E<0$, both states obey the virial theorem, and $\Delta V_{ee}>0$, as the calculations show"
    SYMBOLS = r"every inequality follows from the two virial identities and the measured sign of $\Delta V_{ee}$; nothing else is assumed"

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\text{(1)}\ \Delta T", r"=-\Delta E>0", r"virial: $E=-T$; the electrons are more compressed"),
            (r"\text{(2)}\ \Delta V", r"=2\Delta E<0", r"virial: $E=\tfrac12V$"),
            (r"\text{(3)}\ \Delta V_{ne}", r"=2\Delta E-\Delta V_{ee}<2\Delta E<0", r"$V=V_{ne}+V_{ee}$, and $\Delta V_{ee}>0$"),
            (r"\text{(4)}\ |\Delta V_{ne}|", r">\Delta V_{ee}", "from step 3"),
        ], size=40).move_to([0, 0.45, 0])
        win = rich("the nucleus wins: stronger attraction over-compensates stronger repulsion — Lean: less\\_screening",
                   32, GOLD, width=12.4).move_to([0, -2.1, 0])
        self.say("Now turn less screening into inequalities. Assume three things: the triplet is lower, both states obey "
                 "the virial theorem, and the repulsion is larger in the triplet, which is what accurate calculations "
                 "show.")
        self.say("[Step one. From E equals minus T, the kinetic energy change is minus the energy change, which is "
                 "positive: the triplet's electrons are more compressed.]", m.FadeIn(d.rows[0]))
        self.say("[Step two. From E equals one half V, the potential energy change is twice the energy change, which is "
                 "negative.]", m.FadeIn(d.rows[1]))
        self.say("[Step three. The potential energy is attraction plus repulsion, so the change in attraction is two delta "
                 "E minus the change in repulsion. Since the repulsion went up, this is even more negative than two "
                 "delta E.]", m.FadeIn(d.rows[2]))
        self.say("[Step four. So the gain in nuclear attraction is larger than the loss from extra repulsion.]",
                 m.FadeIn(d.rows[3]))
        self.say("[The nucleus wins: stronger attraction over-compensates stronger repulsion.] This chain of inequalities "
                 "is proved in Lean as the theorem less screening.", m.FadeIn(win))
        self.wait(0.4)


class S48Picture(Frame):
    """08-hund.tex, frame 6: 'The physical picture'."""

    TITLE = "The physical picture"
    SYMBOLS = (r"dashed circle: size of the electron cloud — shaded region: Fermi hole, where the other same-spin electron "
               r"is absent — $e_1,e_2$: the two electrons")

    def construct(self) -> None:
        self.setup_frame()
        cs, ct = np.array([-3.4, 0.55, 0]), np.array([3.4, 0.55, 0])
        sing = m.VGroup(m.Dot(cs, radius=0.12, color=GOLD),
                        m.DashedVMobject(m.Circle(radius=1.75, color=CYAN, stroke_width=2).move_to(cs), num_dashes=40),
                        m.Dot(cs + [1.4, 0.95, 0], radius=0.09, color=CYAN), m.Dot(cs + [-1.5, -0.65, 0], radius=0.09, color=CYAN))
        out = lambda dot, c, r=0.34: dot.get_center() + r * (dot.get_center() - c) / np.linalg.norm(dot.get_center() - c)  # noqa: E731
        sl = m.VGroup(M("e_1", size=28, color=CYAN).move_to(out(sing[2], cs)),
                      M("e_2", size=28, color=CYAN).move_to(out(sing[3], cs)))
        st = rich("singlet: electrons may overlap, each screens the nucleus", 28, BLUE, width=5.4).move_to(cs + [0, -2.45, 0])
        hole = m.VGroup(*[m.Circle(radius=r, stroke_width=0, fill_color=ROSE, fill_opacity=0.08) for r in (0.62, 0.45, 0.3)])
        hole.move_to(ct + [1.0, 0.9, 0])
        trip = m.VGroup(m.Dot(ct, radius=0.12, color=GOLD),
                        m.DashedVMobject(m.Circle(radius=1.35, color=ROSE, stroke_width=2).move_to(ct), num_dashes=34),
                        hole, m.Dot(ct + [1.0, 0.9, 0], radius=0.09, color=ROSE), m.Dot(ct + [-1.1, -0.6, 0], radius=0.09, color=ROSE))
        tl = m.VGroup(M("e_1", size=28, color=ROSE).move_to(out(trip[3], ct, 0.42)),
                      M("e_2", size=28, color=ROSE).move_to(out(trip[4], ct)),
                      rich("Fermi hole", 26, ROSE).move_to(ct + [2.25, 1.6, 0]))
        tt = rich("triplet: kept apart, less screening, both contract towards the nucleus", 28, ROSE, width=5.4)
        tt.move_to(ct + [0, -2.45, 0])
        foot = rich("contraction lowers $V_{ne}$ • raises $T$ • also raises $V_{ee}$, closer on average", 30, width=12.4)
        foot.move_to([0, -2.55, 0])
        st.shift(m.UP * 0.25)
        tt.shift(m.UP * 0.25)
        self.say("[Here is the physical picture. In the singlet, the two electrons may come close to each other. Each one "
                 "spends part of its time between the nucleus and the other electron, screening the nuclear charge, so "
                 "the cloud stays large.]", m.AnimationGroup(m.FadeIn(sing), m.FadeIn(sl), m.FadeIn(st)))
        self.say("[In the triplet, the Fermi hole keeps the two electrons apart. Each screens the nucleus less, so both "
                 "feel more of its charge and the cloud contracts towards the nucleus.]",
                 m.AnimationGroup(m.FadeIn(trip), m.FadeIn(tl), m.FadeIn(tt)))
        self.say("[The contraction lowers the nuclear attraction energy, raises the kinetic energy, and also raises the "
                 "repulsion, because the electrons are closer on average.] All three signs match the virial analysis.",
                 m.FadeIn(foot))
        self.wait(0.4)


class S49Helium(Frame):
    """08-hund.tex, frame 7: 'Test 1: helium 1s2s, near-exact'."""

    TITLE = "Test 1: helium 1s2s, near-exact"
    SUBTITLE = r"T4: $2\,^3S$ versus $2\,^1S$, 16s7p4d basis within $10^{-4}\,\Eh$ of exact, scaled to satisfy the virial theorem"
    SYMBOLS = (r"$2\,^3S$, $2\,^1S$: the $1s2s$ excited states of He, same configuration, triplet and singlet — 16s7p4d: "
               r"Gaussian basis functions of $s$, $p$ and $d$ type — exact energies: Drake's benchmark values")

    def construct(self) -> None:
        self.setup_frame()
        axes, bars, vals = bar_chart([-0.029347, 0.029347, -0.077168, 0.018473],
                                     [r"\Delta E", r"\Delta T", r"\Delta V_{ne}", r"\Delta V_{ee}"],
                                     [GOLD, CYAN, GREEN, ROSE], (-0.09, 0.045), width=6.2, height=4.4,
                                     ylabel="triplet − singlet, hartree")
        chart = m.VGroup(axes, bars, vals).move_to([-3.3, 0.0, 0])
        tab = M(r"\begin{array}{lrr} & 2\,^3S & 2\,^1S\\ \hline E\ (\text{ours}) & -2.175212 & -2.145865\\ "
                r"E\ (\text{exact}) & -2.175229 & -2.145974\\ -\ev V/\ev T & 2.000000 & 2.000000\end{array}", size=32)
        tab.move_to([3.6, 1.2, 0])
        verdict = rich(r"$\Delta V_{ee}>0$: Slater's mechanism fails; $\Delta V_{ne}$ pays for everything. Check: "
                       r"$\tfrac12(-0.0772+0.0185)=-0.0293=\Delta E$", 30, width=5.8).move_to([3.6, -1.2, 0])
        self.say("[Test T four computes this exactly for helium's one s two s states: the triplet two cubed S and the "
                 "singlet two one S, in a large Gaussian basis, within ten to the minus four hartree of the exact "
                 "values.]", m.AnimationGroup(m.FadeIn(tab), m.FadeIn(axes)))
        self.say("[The triplet is lower by zero point zero two nine three hartree.] Both states satisfy the virial "
                 "theorem to six decimal places.", m.GrowFromEdge(bars[0], m.UP))
        self.say("[The kinetic energy goes up by exactly the same amount, as the virial theorem requires.]",
                 m.AnimationGroup(m.GrowFromEdge(bars[1], m.DOWN), m.FadeIn(vals[:2])))
        self.say("[The nuclear attraction drops by zero point zero seven seven hartree,] [while the repulsion goes up, by "
                 "zero point zero one eight five.]", m.AnimationGroup(m.GrowFromEdge(bars[2], m.UP), m.FadeIn(vals[2])),
                 m.AnimationGroup(m.GrowFromEdge(bars[3], m.DOWN), m.FadeIn(vals[3])))
        self.say("[So Slater's mechanism, lower repulsion, fails: the repulsion is higher in the triplet, and the stronger "
                 "nuclear attraction pays for everything. As a check, one half of the two potential changes adds up to "
                 "minus zero point zero two nine three, the energy difference.]", m.FadeIn(verdict))
        self.wait(0.4)


class S50Carbon(Frame):
    """08-hund.tex, frame 8: 'Test 2: the carbon atom (literature)'."""

    TITLE = "Test 2: the carbon atom, from the literature"
    SUBTITLE = "Hongo et al., J. Chem. Phys. 121, 7144, 2004, Table I — read from the arXiv full text"
    SYMBOLS = (r"$^3P$, $^1D$: lowest triplet and singlet terms of the C atom, $2p^2$ — DMC: diffusion quantum Monte Carlo, "
               r"nearly exact correlation — differences computed by us from their Table I")

    def construct(self) -> None:
        self.setup_frame()
        tab = M(r"\begin{array}{lrrr} {}^3P-{}^1D\ (\Eh) & \Delta V_{ee} & \Delta V_{en} & \Delta T\\ \hline "
                r"\text{Hartree–Fock} & +0.032 & -0.145 & +0.057\\ \text{DMC, linear estimator} & +0.074 & -0.169 & +0.048"
                r"\end{array}", size=38).move_to([0, 1.2, 0])
        same = rich("same pattern as helium: higher repulsion, much stronger attraction, higher kinetic energy", 30,
                    width=12).move_to([0, -0.3, 0])
        res = Box(m.VGroup(rich("The review's account — less screening, $V_{ee}$ greater in the high-spin state — agrees "
                                "with He, ours, and C, Hongo.", 30, width=10.6), pill("verified")).arrange(m.RIGHT, buff=0.3),
                  "result").move_to([0, -1.75, 0])
        self.say("[Test two is the carbon atom, from the literature. Hongo and coworkers computed the lowest triplet and "
                 "singlet terms of carbon, three P and one D, with Hartree Fock and with diffusion quantum Monte Carlo, "
                 "which captures nearly all of the correlation.] We read their Table one from the full text and "
                 "computed the differences.", m.FadeIn(tab))
        self.say("[The pattern is the same as in helium: the repulsion is higher in the triplet, the attraction is much "
                 "stronger, and the kinetic energy is higher.]", m.FadeIn(same))
        self.say("[So the review's account, less screening, with the repulsion greater in the high-spin state, agrees "
                 "with our helium result and with carbon. Verified.]", m.FadeIn(res))
        self.wait(0.4)


class S51SameSpin(Frame):
    """08-hund.tex, frame 9: 'A side claim: same-spin correlation'."""

    TITLE = "A side claim: same-spin correlation"
    SYMBOLS = (r"correlation energy $=E_{\text{exact}}-E_{\text{Hartree–Fock}}$ — He: $2\,^3S$ has one same-spin pair, "
               r"$1\,^1S$ one opposite-spin pair — MP2: second-order perturbation theory, split into same-spin and "
               r"opposite-spin parts, divided by the number of pairs")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"the absolute value of the correlation energy is approximately an order of magnitude lower for a '
                      'pair of two same-spin electrons compared to that of opposite-spin electrons" — p. 442, citing '
                      'Krylov 2001', "claim", width=12.6, size=28).move_to([0, 1.75, 0])
        names = ["He, 2³S over 1¹S", "C₂H₄, MP2", "N₂, MP2", "H₂O, MP2"]
        vals = [0.023, 0.32, 0.43, 0.43]
        x0, w = -4.0, 4.9
        bars, labs, nums = m.VGroup(), m.VGroup(), m.VGroup()
        for k, (n, v) in enumerate(zip(names, vals)):
            y = 0.35 - 0.62 * k
            bar = m.Rectangle(width=max(v / 0.5 * w, 0.03), height=0.4, stroke_width=0, fill_color=CYAN, fill_opacity=1)
            bar.move_to([x0 + bar.width / 2, y, 0])
            bars.add(bar)
            labs.add(rich(n, 26).next_to([x0, y, 0], m.LEFT, buff=0.2))
            nums.add(M(f"{v}", size=26).next_to(bar, m.RIGHT, buff=0.1))
        axis = m.Line([x0, -2.0, 0], [x0 + w, -2.0, 0], color=MUTED, stroke_width=2)
        xl = rich("same-spin over opposite-spin, per pair", 24, MUTED).next_to(axis, m.DOWN, buff=0.1)
        tenth = m.DashedLine([x0 + 0.1 / 0.5 * w, 0.75, 0], [x0 + 0.1 / 0.5 * w, -2.0, 0], color=ROSE, stroke_width=2.5)
        notes = m.VGroup(rich("dashed: “an order of magnitude”, 0.1", 26, ROSE, width=5.3),
                         rich("He: 0.023, the claim holds", 26, width=5.3),
                         rich("molecular valence shells: about 0.3 to 0.4 per pair, compare SCS-MP2 scaling ⅓ versus ⁶⁄₅", 26,
                              width=5.3),
                         m.VGroup(pill("overstated"), rich("true for compact two-electron systems, overstated in general: "
                                                           "T15", 26, width=3.4)).arrange(m.RIGHT, buff=0.15))
        notes.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.22)
        notes.move_to([1.3 + notes.width / 2, -0.6, 0])
        self.say("[A side claim in the review: the correlation energy for a pair of same-spin electrons is roughly an "
                 "order of magnitude smaller than for an opposite-spin pair.] The correlation energy is the exact energy "
                 "minus the Hartree Fock energy.", m.FadeIn(claim))
        self.say("[Test T fifteen measured this ratio per pair.] [The dashed line marks one tenth, an order of "
                 "magnitude.]", m.AnimationGroup(m.FadeIn(labs), m.Create(axis), m.FadeIn(xl)),
                 m.AnimationGroup(m.Create(tenth), m.FadeIn(notes[0])))
        self.say("[For helium, comparing the triplet two cubed S, with one same-spin pair, to the ground state, with one "
                 "opposite-spin pair, the ratio is zero point zero two three. The claim holds.]",
                 m.AnimationGroup(m.GrowFromEdge(bars[0], m.LEFT), m.FadeIn(nums[0]), m.FadeIn(notes[1])))
        self.say("[But for the valence shells of ethylene, nitrogen and water, second-order perturbation theory gives "
                 "zero point three to zero point four per pair.] That matches the spin-component-scaled M P two method, "
                 "which scales the two parts by one third and six fifths.",
                 m.AnimationGroup(m.LaggedStart(*[m.GrowFromEdge(b, m.LEFT) for b in bars[1:]], lag_ratio=0.3),
                                  m.FadeIn(nums[1:]), m.FadeIn(notes[2])))
        self.say("[So the claim is true for compact two-electron systems, and overstated in general.]",
                 m.FadeIn(notes[3]))
        self.wait(0.4)
