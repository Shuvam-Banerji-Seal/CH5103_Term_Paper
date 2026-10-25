"""Chapter 7: static correlation, H2 dissociation and the weak-interaction limit (presentation/sections/09-static.tex)."""
import csv
from pathlib import Path

import numpy as np

import manimgx as m

from ch01_foundations import explain
from ch04_energies import cloud
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ROSE, Box, Derivation, Frame, Plot, M, T, axes, boxed, curve, figure,
                  pill, rich)

DATA = Path(__file__).resolve().parents[2] / "presentation" / "data"


class S52StaticDynamic(Frame):
    """09-static.tex, frame 1: 'Static versus dynamic correlation'."""

    TITLE = "Static versus dynamic correlation"
    SYMBOLS = (r"correlation energy: what a single determinant, Hartree–Fock, misses — configuration: one way of filling "
               r"the orbitals, a determinant or a spin-adapted combination — term symbols such as $^1\Sigma_g^+$ or "
               r"$^3A_2$: spin multiplicity and spatial symmetry of a state")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"The weaker the interaction between the two nonbonding molecular orbitals (MOs), the stronger the '
                      'static correlation (Figure 2)." — p. 442', "claim", width=6.4, size=28).move_to([-3.25, 1.2, 0])
        dyn = rich("dynamic: electrons dodging each other within one configuration", 30, width=6.2)
        sta = rich("static: several configurations of comparable weight", 30, width=6.2)
        defs = m.VGroup(dyn, sta).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3).next_to(claim, m.DOWN, buff=0.45)
        defs.align_to(claim, m.LEFT)
        dyn[0][:8].set_color(GOLD)
        fig = figure("fig02_state_energies_H2_ethylene_TM.png", height=3.3, max_width=6.0).move_to([3.5, 0.5, 0])
        cap = rich("Figure 2: (a) H$_2$ bond breaking, (b) ethylene twist, (c) metal–ligand distance", 26, MUTED,
                   width=6.0).next_to(fig, m.DOWN, buff=0.2)
        self.say("[The next mechanism is static correlation. The review says: the weaker the interaction between the two "
                 "nonbonding molecular orbitals, the stronger the static correlation, and points to its Figure two.]",
                 m.FadeIn(claim))
        self.say("[That figure shows three cases where the orbital interaction weakens: breaking the bond of H two, "
                 "twisting ethylene, and stretching a metal ligand bond.]",
                 m.AnimationGroup(m.FadeIn(fig), m.FadeIn(cap)))
        self.say("[Two kinds of correlation are distinguished. Dynamic correlation is electrons dodging each other "
                 "within one configuration.] [Static correlation means that several configurations have comparable "
                 "weight, so no single determinant is a good starting point.]", m.FadeIn(dyn), m.FadeIn(sta))
        self.wait(0.4)


class S53H2Minimal(Frame):
    """09-static.tex, frame 2: 'H2 in a minimal basis'."""

    TITLE = "H$_2$ in a minimal basis"
    SYMBOLS = (r"$\chi_A,\chi_B$: hydrogen $1s$ atomic orbitals on nuclei $A$ and $B$ — $S=\braket{\chi_A}{\chi_B}$: their "
               r"overlap — $g$ and $u$: even and odd under inversion through the bond centre — indices 1 and 2 below mean "
               r"$\varphi_1,\varphi_2$")

    def construct(self) -> None:
        self.setup_frame()
        one = rich(r"one $1s$ function per atom, $\chi_A,\chi_B$, overlap $S$:", 30)
        d = Derivation([(r"\sigma_g\equiv\varphi_1", r"=\frac{\chi_A+\chi_B}{\sqrt{2(1+S)}}", ""),
                        (r"\sigma_u\equiv\varphi_2", r"=\frac{\chi_A-\chi_B}{\sqrt{2(1-S)}}", "")], size=38)
        e1 = explain(r"$\sqrt{2(1\pm S)}$: $\braket{\chi_A\pm\chi_B}{\chi_A\pm\chi_B}=1+1\pm2S$", width=7.0)
        par = rich(r"$\varphi_1$ even, $\varphi_2$ odd under inversion $\Rightarrow h_{12}=\eri1112=\eri2221=0$", 30, width=7.2)
        e2 = explain("an integral with an odd number of φ2's has an odd integrand: it integrates to zero", width=7.0)
        left = m.VGroup(one, d, e1, par, e2).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.28).move_to([-2.7, 0.2, 0])
        A, B = np.array([3.6, 0.35, 0]), np.array([5.6, 0.35, 0])
        nuclei = m.VGroup(m.Dot(A, radius=0.08, color=GOLD), m.Dot(B, radius=0.08, color=GOLD))
        g = cloud(CYAN, [4.6, 1.55, 0], 3.2, 1.2)
        gl = rich(r"$\sigma_g$, bonding", 28, CYAN).move_to([4.6, 2.45, 0])
        u1, u2 = cloud(ROSE, [3.45, -1.0, 0], 1.15, 1.15), cloud(BLUE, [5.75, -1.0, 0], 1.15, 1.15)
        node = m.DashedLine([4.6, -1.7, 0], [4.6, -0.3, 0], color=MUTED, stroke_width=2)
        ul = rich(r"$\sigma_u$, antibonding, with a node", 28, ROSE).move_to([4.6, -2.05, 0])
        self.say("[Take the simplest model of H two: one hydrogen one s function on each atom, chi A and chi B, with "
                 "overlap S.]", m.AnimationGroup(m.FadeIn(one), m.FadeIn(nuclei)))
        self.say("[The bonding orbital, sigma g, is their normalised sum,] [and the antibonding orbital, sigma u, their "
                 "normalised difference.]", m.AnimationGroup(m.FadeIn(d.rows[0]), m.FadeIn(g), m.FadeIn(gl)),
                 m.AnimationGroup(m.FadeIn(d.rows[1]), m.FadeIn(u1), m.FadeIn(u2), m.Create(node), m.FadeIn(ul)))
        self.say("[The normalisation factors follow from the norm of chi A plus or minus chi B: one plus one plus or "
                 "minus two S.]", m.FadeIn(e1))
        self.say("[Under inversion through the bond centre, sigma g is even and sigma u is odd. Any integral containing "
                 "an odd number of sigma u functions has an odd integrand and integrates to zero. So the mixed one-"
                 "electron integral, and the integrals one one one two and two two two one, all vanish.]",
                 m.AnimationGroup(m.FadeIn(par), m.FadeIn(e2)))
        self.wait(0.4)


class S54CI2x2(Frame):
    """09-static.tex, frame 3: 'The 2x2 CI problem'."""

    TITLE = r"The $2\times2$ CI problem"
    SYMBOLS = (r"CI: configuration interaction, diagonalising $\Hop$ among several configurations — RHF: restricted "
               r"Hartree–Fock, both electrons in $\sigma_g$ — $^3\Sigma_u^+$, $^1\Sigma_u^+$: the triplet and the open-shell "
               r"singlet of $\sigma_g^1\sigma_u^1$")

    def construct(self) -> None:
        self.setup_frame()
        top = rich(r"the open-shell singlet $^1\Sigma_u^+$ is alone; the two closed shells $\sigma_g^2$ and $\sigma_u^2$, "
                   r"$^1\Sigma_g^+$, mix:", 30, width=12.6).move_to([0, 2.2, 0])
        H = M(r"\mathbf H=\begin{pmatrix}E_1&K_{12}\\K_{12}&E_2\end{pmatrix},\qquad E_1=2h_{11}+J_{11}\ (\text{RHF}),"
              r"\quad E_2=2h_{22}+J_{22}", size=38).move_to([0, 1.25, 0])
        e = explain(r"the coupling $K_{12}$ is the closed-shell to closed-shell element $\mel{\Phi_{\text i}}{\Hop}{\Phi_{\text{ii}}}$ "
                    r"derived in Part V", width=12).next_to(H, m.DOWN, buff=0.2)
        d = Derivation([
            (r"\det(\mathbf H-E\mathbf 1)", r"=(E_1-E)(E_2-E)-K_{12}^2=0", "eigenvalue condition"),
            (r"E^2-(E_1+E_2)E+E_1E_2-K_{12}^2", r"=0", "multiply out"),
            (r"E_{\text{CI}}", r"=\tfrac12\Bigl[E_1+E_2-\sqrt{(E_2-E_1)^2+4K_{12}^2}\Bigr]", "lower root of the quadratic"),
        ], size=34).move_to([0, -0.85, 0])
        also = rich(r"also: $E(^3\Sigma_u^+)=h_{11}+h_{22}+J_{12}-K_{12}$, $\ E(^1\Sigma_u^+)=h_{11}+h_{22}+J_{12}+K_{12}$", 30)
        also.move_to([0, -2.45, 0])
        self.say("[By symmetry, the open-shell singlet sigma g sigma u is alone in its symmetry, while the two closed "
                 "shells, sigma g squared and sigma u squared, have the same symmetry and mix.]", m.FadeIn(top))
        self.say("[Their Hamiltonian is a two by two matrix. The diagonal holds the two closed-shell energies, and the "
                 "first one, E one, is the restricted Hartree Fock energy. The coupling is K one two,] [the closed-shell "
                 "to closed-shell element we derived earlier.]", m.Write(H), m.FadeIn(e))
        self.say("[The eigenvalues satisfy the determinant condition: E one minus E, times E two minus E, minus K one two "
                 "squared, equals zero.]", m.FadeIn(d.rows[0]))
        self.say("[Multiplied out, that is a quadratic in E.]", m.FadeIn(d.rows[1]))
        self.say("[Its lower root is the configuration interaction ground state: one half of E one plus E two, minus the "
                 "square root of the gap squared plus four K one two squared.]", m.FadeIn(d.rows[2]))
        self.say("[The triplet and the open-shell singlet of sigma g sigma u keep their earlier forms: h one one plus h "
                 "two two plus J one two, minus or plus K one two.]", m.FadeIn(also))
        self.wait(0.4)


class S55Apart1(Frame):
    """09-static.tex, frame 4: 'Pulling the atoms apart (1/2): the integrals'."""

    TITLE = "Pulling the atoms apart (1/2): the integrals"
    SUBTITLE = (r"assume $R\to\infty$: $S\to0$, every overlap density $\chi_A\chi_B\to0$; $U=\eri AAAA$, "
                r"$V=\eri AABB\to1/R$")
    SYMBOLS = (r"$R$: H–H distance — $U$: repulsion of two electrons on the same atom — $V$: repulsion of electrons on "
               r"different atoms, $\to1/R$, two point charges — $E_H$: energy of an isolated H atom")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\varphi_1^2", r"=\tfrac12(\chi_A^2+\chi_B^2+2\chi_A\chi_B)\to\tfrac12(\chi_A^2+\chi_B^2)", "the atoms no longer overlap"),
            (r"\varphi_2^2", r"\to\tfrac12(\chi_A^2+\chi_B^2)", "same, minus sign gone"),
            (r"\varphi_1\varphi_2", r"\to\tfrac12(\chi_A^2-\chi_B^2)", r"$\tfrac12(\chi_A+\chi_B)(\chi_A-\chi_B)$"),
            (r"J_{11}=J_{22}=J_{12}", r"\to\tfrac14\bigl[U+V+V+U\bigr]=\tfrac12(U+V)", "four cross terms of two half-clouds"),
            (r"K_{12}", r"\to\tfrac14\bigl[U-V-V+U\bigr]=\tfrac12(U-V)", r"the $\chi_B^2$ part enters with a minus"),
        ], size=34, row_buff=0.24).move_to([0, 0.35, 0])
        h = rich(r"and $h_{11}=h_{22}\to E_H-\tfrac1R$: an electron on A still feels nucleus B as a point charge", 30,
                 width=12.4).move_to([0, -2.35, 0])
        self.say("Now pull the two atoms apart, to infinite separation. The overlap goes to zero, and so does every "
                 "overlap density, chi A times chi B. Call U the repulsion of two electrons on the same atom, and V the "
                 "repulsion of electrons on different atoms, which tends to one over R.")
        self.say("[The bonding orbital squared contains a cross term, two chi A chi B, which vanishes: the density "
                 "becomes one half chi A squared plus chi B squared, half an electron on each atom.]", m.FadeIn(d.rows[0]))
        self.say("[The antibonding orbital squared tends to the same thing.]", m.FadeIn(d.rows[1]))
        self.say("[The product of the two orbitals is one half of chi A plus chi B times chi A minus chi B: one half chi A "
                 "squared minus chi B squared.]", m.FadeIn(d.rows[2]))
        self.say("[Every Coulomb integral is then the repulsion of two half-clouds, spread over both atoms: four cross "
                 "terms, U plus V plus V plus U, over four. One half of U plus V.]", m.FadeIn(d.rows[3]))
        self.say("[The exchange integral uses the product density, where chi B squared enters with a minus sign: U minus "
                 "V minus V plus U, over four. One half of U minus V.]", m.FadeIn(d.rows[4]))
        self.say("[And each one-electron integral tends to the hydrogen atom energy minus one over R, because an electron "
                 "on atom A still feels nucleus B as a point charge.]", m.FadeIn(h))
        self.wait(0.4)


class S56Apart2(Frame):
    """09-static.tex, frame 5: 'Pulling the atoms apart (2/2): the energies'."""

    TITLE = "Pulling the atoms apart (2/2): the energies"
    SYMBOLS = (r"$2E_H$: the correct limit, two separate H atoms — $E_1=2h_{11}+J_{11}$ and $E_2=2h_{22}+J_{22}$ become "
               r"equal as $R\to\infty$")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"E_{\text{RHF}}", r"=2h_{11}+J_{11}+\tfrac1R=2E_H-\tfrac2R+\tfrac U2+\tfrac{V}{2}+\tfrac1R\overset{V=1/R}{=}2E_H+\tfrac U2-\tfrac1{2R}", ""),
            (r"E_T", r"=2h_{11}+J_{12}-K_{12}+\tfrac1R=2E_H-\tfrac2R+V+\tfrac1R\overset{V=1/R}{=}2E_H", ""),
            (r"E_{\text{CI}}", r"=E_1-K_{12}\ (E_1=E_2)=2E_H+\tfrac U2-\tfrac1{2R}-\tfrac{U-V}{2}\to2E_H", ""),
            (r"E(^1\Sigma_u^+)", r"=E_T+2K_{12}\to2E_H+U-V", ""),
        ], size=32, row_buff=0.35).move_to([0, 0.75, 0])
        d.rows[0][1].set_color(FG)
        e = explain(r"RHF keeps $U/2$ because half of $\sigma_g^2$ is H$^+$H$^-$; in CI, $E_1=E_2$, so the root is $E_1-K_{12}$, "
                    r"and $K_{12}=\tfrac{U-V}{2}$ cancels it", width=12.4).move_to([0, -1.35, 0])
        res = rich("RHF misses the dissociation limit by U/2; one extra configuration fixes it exactly.", 32, GREEN,
                   width=12.4).move_to([0, -2.4, 0])
        self.say("[Now the energies, including the nuclear repulsion, one over R. Restricted Hartree Fock gives two h one "
                 "one plus J one one plus one over R: two hydrogen energies, minus two over R, plus U over two plus V "
                 "over two, plus one over R. With V equal to one over R, that is two E H plus U over two minus one over "
                 "two R.] It does not reach two separate hydrogen atoms: it is too high by U over two.", m.FadeIn(d.rows[0]))
        self.say("[The triplet gives two E H minus two over R, plus V, plus one over R, which is exactly two E H: the "
                 "correct limit.]", m.FadeIn(d.rows[1]))
        self.say("[In configuration interaction, E one and E two become equal, so the lower root is simply E one minus K "
                 "one two. Subtracting U minus V over two cancels the error: the result tends to two E H.]",
                 m.FadeIn(d.rows[2]))
        self.say("[The open-shell singlet lies two K above the triplet: two E H plus U minus V, an ionic state.]",
                 m.FadeIn(d.rows[3]))
        self.say("[Why does Hartree Fock fail? Half of sigma g squared describes H plus and H minus, an ion pair, which "
                 "costs U over two. In configuration interaction the two closed shells are degenerate, and the coupling K "
                 "one two cancels exactly that cost.]", m.FadeIn(e))
        self.say("[So restricted Hartree Fock misses the dissociation limit by U over two, and one extra configuration "
                 "fixes it exactly.]", m.FadeIn(res))
        self.wait(0.4)


class S57CIWavefunction(Frame):
    """09-static.tex, frame 6: 'What the CI wavefunction is'."""

    TITLE = "What the CI wavefunction is"
    SYMBOLS = (r"covalent: one electron on each atom — ionic: both electrons on one atom, H$^-$ next to H$^+$ — $c_1,c_2$: CI "
               r"coefficients of $\sigma_g^2$ and $\sigma_u^2$; shorthand $\chi_A\chi_B\equiv\chi_A(1)\chi_B(2)$")

    def construct(self) -> None:
        self.setup_frame()
        top = rich(r"at $R\to\infty$ the eigenvector is $c_1=-c_2=\tfrac1{\sqrt2}$: two configurations, equal weight", 30,
                   GOLD).move_to([0, 2.2, 0])
        d = Derivation([
            (r"\varphi_1(1)\varphi_1(2)", r"=\tfrac12\bigl[\underbrace{\chi_A\chi_B+\chi_B\chi_A}_{\text{covalent}}+"
             r"\underbrace{\chi_A\chi_A+\chi_B\chi_B}_{\text{ionic}}\bigr]", r"expand $(\chi_A+\chi_B)^2/2$"),
            (r"\varphi_1\varphi_1-\varphi_2\varphi_2", r"=\tfrac12\bigl[(\chi_A+\chi_B)^2-(\chi_A-\chi_B)^2\bigr]",
             "the CI combination"),
            ("", r"=\chi_A(1)\chi_B(2)+\chi_B(1)\chi_A(2)", "the ionic terms cancel"),
        ], size=36).move_to([0, 0.45, 0])
        rhf = Box(rich("RHF: 50 % ionic — H⁺H⁻ at infinity costs U/2", 30), "plain")
        ci = Box(rich("CI: purely covalent — Heitler–London H· ·H", 30), "plain")
        rhf.panel.set_stroke(ROSE, 2)
        ci.panel.set_stroke(GREEN, 2)
        pair = m.VGroup(rhf, ci).arrange(m.RIGHT, buff=0.8).move_to([0, -2.2, 0])
        self.say("[At infinite separation, the configuration interaction eigenvector has c one equal to minus c two, one "
                 "over root two each: two configurations with equal weight.]", m.FadeIn(top))
        self.say("[Expand sigma g squared in atomic orbitals. It contains covalent terms, one electron on each atom, and "
                 "ionic terms, both electrons on the same atom, with equal weight.]", m.FadeIn(d.rows[0]))
        self.say("[Now take the configuration interaction combination, sigma g squared minus sigma u squared.]",
                 m.FadeIn(d.rows[1]))
        self.say("[The ionic terms cancel, and what remains is purely covalent: chi A of one chi B of two plus chi B of "
                 "one chi A of two.]", m.FadeIn(d.rows[2]))
        self.say("[So Hartree Fock is fifty percent ionic, and the ion pair at infinity costs U over two,] [while "
                 "configuration interaction is purely covalent: the Heitler London wavefunction, one hydrogen atom on "
                 "each side.]", m.FadeIn(rhf), m.FadeIn(ci))
        self.wait(0.4)


def read_h2():
    with open(DATA / "h2_curves.csv") as f:
        rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]
    return rows


class S58H2Curves(Frame):
    """09-static.tex, frame 7: 'H2 curves from our calculation'."""

    TITLE = "H$_2$ curves from our calculation"
    SUBTITLE = r"STO-3G, PySCF; the closed forms agree to $4\times10^{-16}\,\Eh$: T5"
    SYMBOLS = (r"STO-3G: minimal Gaussian basis, one $1s$ function per H — FCI: full CI, exact in this basis — "
               r"one bohr is $0.529$ Å — $2E_H=-0.9332\,\Eh$ in STO-3G")

    def construct(self) -> None:
        self.setup_frame()
        rows = read_h2()
        R = [r["R"] for r in rows]
        ax = Plot([0.8, 8], [-1.2, 0.2], 8.2, 3.8, xticks=range(1, 9), yticks=[-1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0, 0.2],
                  yfmt="{:.1f}").move_to([-0.85, 0.42, 0])
        xl = rich("R, bohr", 26, MUTED).next_to(ax.x_axis, m.DOWN, buff=0.45)
        yl = rich("E, hartree", 26, MUTED).rotate(m.PI / 2).next_to(ax.y_axis, m.LEFT, buff=0.8)
        clip = lambda ys: [min(y, 0.2) for y in ys]  # noqa: E731 - the slide's y range ends at 0.2
        series = [("twoEH", MUTED, True, "$2E_H$"), ("RHF", GOLD, False, "RHF"), ("CI", CYAN, False, "CI = FCI, $^1\\Sigma_g^+$"),
                  ("T", ROSE, False, "triplet $^3\\Sigma_u^+$"), ("OSS", BLUE, False, "OSS $^1\\Sigma_u^+$")]
        lines, legend = [], m.VGroup()
        for key, col, dashed, name in series:
            xs, ys = zip(*[(r["R"], r[key]) for r in rows if r[key] <= 0.2])
            lines.append(curve(ax, xs, ys, col, dashed=dashed))
            sw = m.Line([0, 0, 0], [0.45, 0, 0], color=col, stroke_width=4)
            legend.add(m.VGroup(sw, rich(name, 24, col)).arrange(m.RIGHT, buff=0.12))
        legend.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.16).next_to(ax, m.RIGHT, buff=0.35).shift(m.UP * 0.6)
        note = rich("CI and the triplet converge on $2E_H$; RHF does not — T5: still $0.362\\,\\Eh=K_{12}$ too high at "
                    "R = 20 bohr", 28, width=12.6).move_to([0, -2.62, 0])
        self.say("[Here are the curves from our own PySCF calculation of H two in the minimal STO three G basis. The "
                 "dashed line is two separate hydrogen atoms,] [and the gold curve is restricted Hartree Fock.]",
                 m.AnimationGroup(m.Create(ax), m.FadeIn(xl), m.FadeIn(yl), m.Create(lines[0]), m.FadeIn(legend[0])),
                 m.AnimationGroup(m.Create(lines[1]), m.FadeIn(legend[1])))
        self.say("[The two-configuration result, which here equals full configuration interaction, bends over and "
                 "approaches the dashed line.]", m.AnimationGroup(m.Create(lines[2]), m.FadeIn(legend[2])))
        self.say("[The triplet is repulsive and also reaches two E H,] [and the open-shell singlet lies above it.]",
                 m.AnimationGroup(m.Create(lines[3]), m.FadeIn(legend[3])),
                 m.AnimationGroup(m.Create(lines[4]), m.FadeIn(legend[4])))
        self.say("[Configuration interaction and the triplet converge on two separate atoms, but Hartree Fock does not: "
                 "test T five finds it still zero point three six two hartree too high at twenty bohr, exactly K one "
                 "two.] The closed forms derived above agree with PySCF to four times ten to the minus sixteen hartree.",
                 m.FadeIn(note))
        self.wait(0.4)


class S59GeneralRule(Frame):
    """09-static.tex, frame 8: 'The general rule: orbital gap versus exchange'."""

    TITLE = "The general rule: orbital gap versus exchange"
    SYMBOLS = (r"Figure 2b: twisting ethylene to $90^\circ$ closes the $\pi$/$\pi^*$ gap, $\Delta\to0$ — $\Delta=h_b-h_a$ — "
               r"$J_d$: same-orbital repulsion, $J_x$: different-orbital — $c_2/c_1=-1$: two configurations of equal "
               r"weight, a pure diradical; $\to0$: one configuration")

    def construct(self) -> None:
        self.setup_frame()
        model = rich(r"model: $h_a=-\tfrac\Delta2$, $h_b=+\tfrac\Delta2$, $J_{aa}=J_{bb}=J_d$, $J_{ab}=J_x$", 30)
        d = Derivation([
            (r"\mathbf H", r"=\begin{pmatrix}J_d-\Delta&K\\K&J_d+\Delta\end{pmatrix}", ""),
            (r"E_S", r"=J_d-\sqrt{\Delta^2+K^2}", ""),
            (r"\frac{c_2}{c_1}", r"=\frac{\Delta-\sqrt{\Delta^2+K^2}}{K}", ""),
            (r"E_S-E_T", r"=(J_d-J_x)+K-\sqrt{\Delta^2+K^2}", ""),
        ], size=34, row_buff=0.25)
        e = explain(r"diagonal $2h+J$; $E_S$ is the lower root; $c_2/c_1$ from row 1, $(J_d-\Delta-E_S)c_1+Kc_2=0$; "
                    r"$E_T=J_x-K$", width=6.4)
        left = m.VGroup(model, d, e).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3).move_to([-3.2, 0.1, 0])
        ax = Plot([0, 6], [-1.05, 0.05], 5.0, 3.4, xticks=range(0, 7), yticks=[-1, -0.75, -0.5, -0.25, 0]).move_to([3.85, 0.6, 0])
        xs = np.linspace(0, 6, 120)
        c = curve(ax, xs, xs - np.sqrt(xs ** 2 + 1), CYAN)
        xl = rich(r"$\Delta/K$", 26, MUTED).next_to(ax.x_axis, m.DOWN, buff=0.42)
        yl = rich(r"$c_2/c_1$", 26, MUTED).next_to(ax.y_axis, m.UP, buff=0.12)
        dl = rich("diradical: equal weights", 24, ROSE).move_to(ax.c2p(1.9, -0.9))
        cl = rich("closed shell", 24, GREEN).move_to(ax.c2p(4.6, -0.38))
        ok = m.VGroup(pill("verified"), rich("weak interaction ⇒ strong static correlation: T6", 28, width=4.8))
        ok.arrange(m.RIGHT, buff=0.2).move_to([3.7, -2.4, 0])
        self.say("[The same mechanism works for any two orbitals. Take a model with orbital energies minus and plus delta "
                 "over two, same-orbital repulsion J d, and different-orbital repulsion J x.]", m.FadeIn(model))
        self.say("[The two closed shells have energies J d minus delta and J d plus delta, coupled by K.]",
                 m.FadeIn(d.rows[0]))
        self.say("[The lower root is J d minus the square root of delta squared plus K squared.]", m.FadeIn(d.rows[1]))
        self.say("[From the first row of the eigenvalue equation, the ratio of the two coefficients is delta minus that "
                 "square root, over K.]", m.AnimationGroup(m.FadeIn(d.rows[2]), m.FadeIn(e), m.Create(ax), m.FadeIn(xl),
                                                           m.FadeIn(yl)))
        self.say("[Plot it against delta over K. When the gap is large, the ratio goes to zero: one configuration, a "
                 "closed shell. When the gap closes, the ratio goes to minus one: two configurations of equal weight, a "
                 "pure diradical.] Twisting ethylene to ninety degrees closes the gap between pi and pi star, which is "
                 "the case of Figure two b.",
                 m.AnimationGroup(m.Create(c), m.FadeIn(dl), m.FadeIn(cl)))
        self.say("[The singlet triplet gap becomes J d minus J x, plus K, minus that square root.]", m.FadeIn(d.rows[3]))
        self.say("[So the weaker the interaction, the stronger the static correlation, exactly as the review says. Test T "
                 "six checked the model symbolically.]", m.FadeIn(ok))
        self.wait(0.4)
