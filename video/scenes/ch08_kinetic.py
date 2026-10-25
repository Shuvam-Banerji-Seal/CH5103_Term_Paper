"""Chapter 8: kinetic exchange and the Hubbard picture (presentation/sections/10-kinetic.tex)."""
import numpy as np

import manimgx as m

from ch01_foundations import explain
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, PANEL, ROSE, VIOLET, Box, Derivation, Frame, Plot, M, T, axes, boxed,
                  curve, figure, level, rich, spin)


class S60Hubbard(Frame):
    """10-kinetic.tex, frame 1: 'The Hubbard picture'."""

    TITLE = "The Hubbard picture"
    SYMBOLS = (r"$l,r$: orthonormal orbitals localised on the left and right radical centres — $t$: hopping, how easily "
               r"an electron moves between them — $U$: cost of two electrons on one site — $V$: repulsion between sites "
               r"— $k$: direct exchange between the sites")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"The kinetic exchange picture based on the Hubbard model … attributes stability of a singlet state '
                      'in the case of orthogonal atomic orbitals (AOs) to the fact that perturbation yielding ionic '
                      'configuration is allowed only from this state, and not from the triplet." — p. 442', "claim",
                      width=12.6, size=28).move_to([0, 1.65, 0])
        L = m.VGroup(m.Circle(radius=0.55, stroke_color=GOLD, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                     M("l", size=40)).move_to([-2.4, -0.6, 0])
        R = m.VGroup(m.Circle(radius=0.55, stroke_color=GOLD, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                     M("r", size=40)).move_to([2.4, -0.6, 0])
        hop = m.DoubleArrow([-1.8, -0.6, 0], [1.8, -0.6, 0], buff=0, color=CYAN, stroke_width=3)
        hl = M(r"\text{hopping } h_{lr}=-t", size=30, color=CYAN).next_to(hop, m.UP, buff=0.12)
        ul = M(r"U=\eri llll", size=28, color=ROSE).next_to(L, m.DOWN, buff=0.15)
        ur = M(r"U=\eri rrrr", size=28, color=ROSE).next_to(R, m.DOWN, buff=0.15)
        vl = M(r"V=\eri llrr", size=28, color=VIOLET).move_to([0, -1.25, 0])
        kl = M(r"k=\eri lrlr\ge0", size=28, color=GREEN).move_to([0, -1.85, 0])
        self.say("[The next mechanism is kinetic exchange. The review says: the kinetic exchange picture based on the "
                 "Hubbard model attributes the stability of a singlet state, for orthogonal atomic orbitals, to the fact "
                 "that the perturbation yielding an ionic configuration is allowed only from the singlet, and not from "
                 "the triplet.]", m.FadeIn(claim))
        self.say("[Set it up with two orthonormal orbitals, l and r, localised on the left and right radical centres.]",
                 m.AnimationGroup(m.FadeIn(L), m.FadeIn(R)))
        self.say("[An electron can hop between them, with matrix element minus t.]",
                 m.AnimationGroup(m.GrowFromCenter(hop), m.FadeIn(hl)))
        self.say("[Putting two electrons on the same site costs the on-site repulsion U,] [two electrons on different "
                 "sites repel by V,] [and there is a direct exchange integral k between the sites, which is never "
                 "negative.]", m.AnimationGroup(m.FadeIn(ul), m.FadeIn(ur)), m.FadeIn(vl), m.FadeIn(kl))
        self.wait(0.4)


class S61IonicSinglets(Frame):
    """10-kinetic.tex, frame 2: 'Step 1: ionic configurations are pure singlets'."""

    TITLE = "Step 1: ionic configurations are pure singlets"
    SYMBOLS = (r"covalent: one electron on each site — ionic: both on one site — $\Theta_{0,0},\Theta_{1,M}$: singlet and "
               r"triplet spin functions, orthogonal to each other — $\propto$: proportional to")

    def construct(self) -> None:
        self.setup_frame()
        items = [r"1. ionic: both electrons in one orbital, $l(1)l(2)$",
                 r"2. that spatial part is symmetric: swapping 1 and 2 changes nothing",
                 r"3. antisymmetry ⇒ its spin part must be the antisymmetric singlet $\Theta_{0,0}$",
                 r"4. $\Hop$ is spin-free, so $\mel{\text{ionic}}{\Hop}{\text{triplet}}\propto\braket{\Theta_{0,0}}{\Theta_{1,M}}=0$"]
        lst = m.VGroup(*[rich(t, 30, width=7.2) for t in items]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3)
        lst.move_to([-2.7, 0.75, 0])
        res = boxed("only the singlet can borrow from ionic configurations", "result", width=7.2, size=30)
        res.next_to(lst, m.DOWN, buff=0.4).align_to(lst, m.LEFT)
        cov = m.VGroup(level(3.4, 1.3, 1.0), level(5.2, 1.3, 1.0), spin(3.4, 1.3, True), spin(5.2, 1.3, False))
        ion = m.VGroup(level(3.4, -0.6, 1.0), level(5.2, -0.6, 1.0), spin(3.4, -0.6, True), spin(3.4, -0.6, False))
        cl = rich("covalent", 26, MUTED).next_to(cov, m.DOWN, buff=0.2)
        il = rich("ionic, $l^2$", 26, MUTED).next_to(ion, m.DOWN, buff=0.2)
        arrow = m.CurvedArrow([6.0, 1.2, 0], [6.0, -0.5, 0], angle=-m.PI / 2, color=CYAN, stroke_width=3)
        tl = M("-t", size=30, color=CYAN).next_to(arrow, m.RIGHT, buff=0.1)
        self.say("[Step one. In an ionic configuration both electrons sit in one orbital, for example l of one times l of "
                 "two.]", m.AnimationGroup(m.FadeIn(lst[0]), m.FadeIn(ion), m.FadeIn(il), m.FadeIn(cov), m.FadeIn(cl)))
        self.say("[That spatial part is symmetric: swapping the electrons changes nothing.]", m.FadeIn(lst[1]))
        self.say("[Since the total must be antisymmetric, its spin part must be the antisymmetric singlet.]",
                 m.FadeIn(lst[2]))
        self.say("[The Hamiltonian contains no spin, so any matrix element between an ionic configuration and a triplet is "
                 "proportional to the overlap of a singlet spin function with a triplet spin function, which is zero.] "
                 "Hopping an electron from one site to the other can connect a covalent singlet to an ionic one, but "
                 "never a triplet.", m.AnimationGroup(m.FadeIn(lst[3]), m.Create(arrow), m.FadeIn(tl)))
        self.say("[So only the singlet can borrow energy from ionic configurations.]", m.FadeIn(res))
        self.wait(0.4)


class S62Matrix(Frame):
    """10-kinetic.tex, frame 3: 'Step 2: the matrix'."""

    TITLE = "Step 2: the matrix"
    SYMBOLS = (r"$ll$, $rr$: the two ionic configurations — cov: the covalent open-shell singlet — $\Phi_\pm$: their "
               r"symmetric and antisymmetric combinations under left–right mirror symmetry")

    def construct(self) -> None:
        self.setup_frame()
        top = rich(r"insert the parameters into the $2e/2o$ Hamiltonian of Part V: $h_{ll}=h_{rr}=0$, $\eri lllr=0$", 30)
        top.move_to([0, 2.2, 0])
        Hs = M(r"E_T=V-k,\qquad \mathbf H_S=\begin{pmatrix}U&k&-\sqrt2t\\k&U&-\sqrt2t\\-\sqrt2t&-\sqrt2t&V+k\end{pmatrix}"
               r"\quad(ll,\ rr,\ \text{cov})", size=36).move_to([0, 1.15, 0])
        e = explain(r"diagonal: $2h+J$ becomes $U$ for $ll$ and $rr$; $h_l+h_r+J+K$ becomes $V+k$ for cov; coupling "
                    r"$\sqrt2(h_{lr}+\eri lllr)=-\sqrt2t$", width=12.4).next_to(Hs, m.DOWN, buff=0.2)
        s3 = rich(r"Step 3: symmetry-adapt the ionic pair, $\Phi_{\pm}=\tfrac1{\sqrt2}(ll\pm rr)$", 30, GOLD)
        s3.move_to([0, -0.55, 0])
        d = Derivation([
            (r"E(\Phi_\pm)", r"=U\pm k", r"$\tfrac12(U+U\pm2k)$"),
            (r"\mel{\Phi_\pm}{\Hop}{\text{cov}}", r"=\tfrac1{\sqrt2}\bigl(-\sqrt2t\mp\sqrt2t\bigr)=\{-2t,\ 0\}",
             "the two couplings add or cancel"),
        ], size=34).move_to([0, -1.55, 0])
        dec = rich(r"$\Phi_-$ decouples; the ground singlet lives in $\{\text{cov},\Phi_+\}$", 30).move_to([0, -2.55, 0])
        self.say("[Step two. Insert these parameters into the two-electron two-orbital Hamiltonian from Part five: the "
                 "site energies are zero, and the mixed integral l l l r vanishes.]", m.FadeIn(top))
        self.say("[The triplet energy is V minus k. The singlets form a three by three matrix in the two ionic "
                 "configurations and the covalent one: U on the ionic diagonal, V plus k on the covalent diagonal, k "
                 "between the two ionic configurations, and minus root two t between each ionic configuration and the "
                 "covalent one.]", m.Write(Hs))
        self.say("[Every entry is one we derived before, with the new names.]", m.FadeIn(e))
        self.say("[Step three. Combine the two ionic configurations into a symmetric and an antisymmetric pair, Phi plus "
                 "and Phi minus.]", m.FadeIn(s3))
        self.say("[Their energies are U plus k and U minus k.]", m.FadeIn(d.rows[0]))
        self.say("[Their couplings to the covalent configuration add for Phi plus, giving minus two t, and cancel for Phi "
                 "minus, giving zero.]", m.FadeIn(d.rows[1]))
        self.say("[So Phi minus decouples, and the ground singlet lives in the two by two space of the covalent "
                 "configuration and Phi plus.]", m.FadeIn(dec))
        self.wait(0.4)


class S63Solve(Frame):
    """10-kinetic.tex, frame 4: 'Step 4: solve and expand'."""

    TITLE = "Step 4: solve and expand"
    SYMBOLS = (r"kinetic exchange: the second-order energy gain $|{-2t}|^2/[(V+k)-(U+k)]$ from virtual hopping into "
               r"$\Phi_+$; the triplet cannot do this — $O(\cdot)$: terms of that order and smaller")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\begin{pmatrix}V+k&-2t\\-2t&U+k\end{pmatrix}\ \Rightarrow\ E_S",
             r"=\tfrac12\Bigl[U+V+2k-\sqrt{(U-V)^2+16t^2}\Bigr]", "lower root"),
            (r"E_S-E_T", r"=\tfrac12(U-V)+2k-\tfrac12\sqrt{(U-V)^2+16t^2}", r"subtract $V-k$"),
            (r"\sqrt{x^2+16t^2}=x+\tfrac{8t^2}{x}+\cdots", r"\Rightarrow\ E_S-E_T=2k-\frac{4t^2}{U-V}+O\!\left(\tfrac{t^4}{(U-V)^3}\right)",
             r"Taylor, $x=U-V\gg t$"),
        ], size=32).move_to([0, 0.95, 0])
        pot = Box(rich("$+2k$: potential exchange, favours the triplet", 30, GREEN, width=5.6), "plain")
        kin = Box(rich("$-4t^2/(U-V)$: kinetic exchange, favours the singlet", 30, ROSE, width=5.6), "plain")
        pair = m.VGroup(pot, kin).arrange(m.RIGHT, buff=0.5, aligned_edge=m.UP).move_to([0, -1.8, 0])
        self.say("[Step four. Solve the two by two problem. Its lower root is one half of U plus V plus two k, minus the "
                 "square root of U minus V squared plus sixteen t squared.]", m.FadeIn(d.rows[0]))
        self.say("[Subtract the triplet energy, V minus k: the gap is one half U minus V, plus two k, minus one half of "
                 "that square root.]", m.FadeIn(d.rows[1]))
        self.say("[Now expand the square root for x equal to U minus V, much larger than t: it is x plus eight t squared "
                 "over x plus smaller terms. The x terms cancel, leaving two k minus four t squared over U minus V.]",
                 m.FadeIn(d.rows[2]))
        self.say("[Two contributions compete. Plus two k is potential exchange, which favours the triplet.] [Minus four t "
                 "squared over U minus V is kinetic exchange: the energy the singlet gains by virtually hopping into the "
                 "ionic configuration, which the triplet cannot do. It favours the singlet.]",
                 m.FadeIn(pot), m.FadeIn(kin))
        self.wait(0.4)


class S64Dimer(Frame):
    """10-kinetic.tex, frame 5: 'Hubbard dimer: exact versus kinetic exchange'."""

    TITLE = "Hubbard dimer: exact versus kinetic exchange"
    SUBTITLE = r"$V=k=0$: $E_S=\tfrac12\bigl(U-\sqrt{U^2+16t^2}\bigr)$, $E_T=0$"
    SYMBOLS = (r"Hubbard dimer: two sites, hopping $t$, on-site repulsion $U$ only — $J_{\text{AF}}>0$: antiferromagnetic "
               r"coupling, antiparallel favoured — $\hat{\mathbf S}_1\cdot\hat{\mathbf S}_2=-\tfrac34$ in the singlet, "
               r"$+\tfrac14$ in the triplet")

    def construct(self) -> None:
        self.setup_frame()
        ax = Plot([0, 0.5], [-1.1, 0.05], 5.8, 3.7, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                  yticks=[-1, -0.75, -0.5, -0.25, 0]).move_to([-2.85, 0.0, 0])
        xs = np.linspace(0, 0.5, 120)
        exact = curve(ax, xs, (1 - np.sqrt(1 + 16 * xs ** 2)) / 2, CYAN)
        approx = curve(ax, xs[xs <= 0.52], -4 * xs[xs <= 0.52] ** 2, ROSE, dashed=True)
        xl = rich("$t/U$", 26, MUTED).next_to(ax.x_axis, m.DOWN, buff=0.42)
        yl = rich("$(E_S-E_T)/U$", 26, MUTED).next_to(ax.y_axis, m.UP, buff=0.12)
        leg = m.VGroup(m.VGroup(m.Line([0, 0, 0], [0.4, 0, 0], color=CYAN, stroke_width=4), rich("exact", 27)).arrange(m.RIGHT, buff=0.1),
                       m.VGroup(m.Line([0, 0, 0], [0.4, 0, 0], color=ROSE, stroke_width=4), rich("$-4t^2/U$", 27)).arrange(m.RIGHT, buff=0.1))
        leg.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.1).move_to(ax.c2p(0.12, -0.85))
        pts = m.VGroup(rich("agree for $t\\ll U$: strong correlation", 30, width=5.6),
                       rich(r"spin Hamiltonian $J_{\text{AF}}\,\hat{\mathbf S}_1\cdot\hat{\mathbf S}_2$ with $J_{\text{AF}}=4t^2/U$",
                            30, width=5.6),
                       rich("this coupling, bond by bond, will build the topology rules", 30, width=5.6),
                       rich("✓ T7: symbolic + PySCF full CI, $t=1, U=6, V=1.5, k=0.2$", 26, MUTED, width=5.6))
        pts.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.32).move_to([3.5, 0.2, 0])
        self.say("[The simplest case is the Hubbard dimer: set V and k to zero. Then the exact singlet energy is one half "
                 "of U minus the square root of U squared plus sixteen t squared, and the triplet energy is zero. Here is "
                 "the exact gap, in units of U, against t over U.]",
                 m.AnimationGroup(m.Create(ax), m.FadeIn(xl), m.FadeIn(yl), m.Create(exact), m.FadeIn(leg[0])))
        self.say("[The kinetic exchange approximation, minus four t squared over U, agrees with it when t is much smaller "
                 "than U, which is the regime of strong correlation.]",
                 m.AnimationGroup(m.Create(approx), m.FadeIn(leg[1]), m.FadeIn(pts[0])))
        self.say("[In that regime the two electrons behave like two spins coupled by a Heisenberg Hamiltonian, J A F "
                 "times S one dot S two, with J A F equal to four t squared over U.] S one dot S two is minus three "
                 "quarters in the singlet and plus one quarter in the triplet, so the singlet is lower by exactly J A F.",
                 m.FadeIn(pts[1]))
        self.say("[Applied bond by bond, this coupling will build the topology rules later on.]", m.FadeIn(pts[2]))
        self.say("[Test T seven checked the whole derivation symbolically and against PySCF full configuration "
                 "interaction, with t equal to one, U six, V one and a half and k zero point two.]", m.FadeIn(pts[3]))
        self.wait(0.4)


class S65IonicResonance(Frame):
    """10-kinetic.tex, frame 6: 'Ionic resonance reverses a spin state (Figure 6)'."""

    TITLE = "Ionic resonance reverses a spin state: Figure 6"
    SYMBOLS = (r"“this contribution”: resonance with closed-shell zwitterionic, or ionic, configurations — MX: "
               r"m-xylylene — NBMO: non-bonding MO, Part X")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig06_ionic_resonance_spin_reversal.png", height=4.8, max_width=6.0).move_to([-3.4, 0.0, 0])
        claim = boxed('"In the pyridinium analog of MX (V in Figure 6) this contribution exceeds the exchange and Coulomb '
                      'terms, which formally favor the triplet state of this system with nondisjoint NBMOs." — p. 444–445',
                      "claim", width=6.1, size=28).move_to([3.5, 1.0, 0])
        why1 = rich(r"low-lying zwitterionic structures mean a small effective $U-V$ ⇒ $4t^2/(U-V)$ grows past $2k$ ⇒ "
                    r"singlet", 30, width=6.0).next_to(claim, m.DOWN, buff=0.35)
        why2 = rich("our qualitative mapping: the review gives no numbers", 26, MUTED, width=6.0).next_to(why1, m.DOWN, buff=0.25)
        self.say("[The review's Figure six shows ionic resonance reversing a spin state.] Meta xylylene, a classic "
                 "triplet diradical, sits next to its pyridinium analog, molecule five.", m.FadeIn(fig))
        self.say("[The review says: in the pyridinium analog of meta xylylene, this contribution, resonance with "
                 "closed-shell zwitterionic configurations, exceeds the exchange and Coulomb terms, which formally favour "
                 "the triplet of this system with nondisjoint non-bonding orbitals.]", m.FadeIn(claim))
        self.say("[In our model, low-lying zwitterionic structures mean a small effective U minus V. Then the kinetic "
                 "exchange term, four t squared over U minus V, grows past two k, and the singlet wins.]", m.FadeIn(why1))
        self.say("[That mapping is qualitative: the review gives no numbers to test.]", m.FadeIn(why2))
        self.wait(0.4)


class S66TwoViews(Frame):
    """10-kinetic.tex, frame 7: 'Delocalised and localised: two views of one state'."""

    TITLE = "Delocalised and localised: two views of one state"
    SYMBOLS = (r"$a,b$: delocalised orbitals, bonding- and antibonding-like — $l,r$: localised site orbitals — the "
               r"unitary rotation between them leaves the two-electron state unchanged")

    def construct(self) -> None:
        self.setup_frame()
        eq = M(r"a,b=\tfrac1{\sqrt2}(l\pm r)\quad\Rightarrow\quad a(1)a(2)-b(1)b(2)=l(1)r(2)+r(1)l(2)", size=40)
        eq.move_to([0, 1.8, 0])
        e = explain(r"expand: $\tfrac12[(l+r)(l+r)-(l-r)(l-r)]$; the $ll$ and $rr$, ionic, terms cancel, and the cross "
                    r"terms add", width=12).next_to(eq, m.DOWN, buff=0.25)
        de = Box(m.VGroup(rich("delocalised orbitals $a,b$", 30, GOLD),
                          rich("two closed-shell configurations of equal weight: static correlation", 28, width=5.3))
                 .arrange(m.DOWN, buff=0.15), "plain", width=5.9)
        lo = Box(m.VGroup(rich("localised orbitals $l,r$", 30, GOLD),
                          rich("one covalent configuration with no ionic part", 28, width=5.3)).arrange(m.DOWN, buff=0.15),
                 "plain", width=5.9)
        pair = m.VGroup(de, lo).arrange(m.RIGHT, buff=0.5, aligned_edge=m.UP).move_to([0, -0.5, 0])
        same = rich("same state, different bookkeeping: the static-correlation and kinetic-exchange descriptions agree",
                    30, width=12.4).move_to([0, -2.35, 0])
        self.say("[Finally, these two pictures are the same physics. Build delocalised orbitals a and b as the sum and "
                 "difference of l and r. Then a of one a of two minus b of one b of two equals l of one r of two plus r of "
                 "one l of two.]", m.Write(eq))
        self.say("[Expand it: the l l and r r terms, the ionic ones, cancel, and the cross terms add.]", m.FadeIn(e))
        self.say("[In delocalised orbitals, the state looks like two closed-shell configurations of equal weight: static "
                 "correlation.] [In localised orbitals, it is a single covalent configuration with no ionic part.]",
                 m.FadeIn(de), m.FadeIn(lo))
        self.say("[It is the same state with different bookkeeping, so the static-correlation and kinetic-exchange "
                 "descriptions agree.]", m.FadeIn(same))
        self.wait(0.4)
