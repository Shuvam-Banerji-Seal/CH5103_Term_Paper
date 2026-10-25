"""Chapter 4: energies of the 2e/2o states, J and K (presentation/sections/06-energies.tex)."""
import manimgx as m

from ch01_foundations import explain
from ch03_two_electrons import AB
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ROSE, VIOLET, Box, Derivation, Frame, M, T, boxed, level,
                  paint_parts, rich, spin)


def cloud(colour: str, center, w: float, h: float) -> m.VGroup:
    """A soft charge cloud: nested translucent ellipses."""
    return m.VGroup(*[m.Ellipse(width=w * k, height=h * k, stroke_width=0, fill_color=colour, fill_opacity=0.16)
                      for k in (1.0, 0.75, 0.5, 0.28)]).move_to(center)


class S31Integrals(Frame):
    """06-energies.tex, frame 1: 'The integrals we need'."""

    TITLE = "The integrals we need"
    SYMBOLS = (r"$\hat h$: one-electron Hamiltonian, kinetic plus nuclear attraction — $h_{pq}$: its matrix element; "
               r"$h_p\equiv h_{pp}$ is the energy of one electron in $\varphi_p$ without the others — $r_{12}="
               r"|\mathbf r_1-\mathbf r_2|$ — chemists' notation $\eri pqrs$: the first pair belongs to electron 1")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"h_{pq}", r"=\int\varphi_p(\mathbf r)\,\hat h\,\varphi_q(\mathbf r)\,\dd\mathbf r", "one electron"),
            (r"\eri pqrs", r"=\iint\frac{\varphi_p(1)\varphi_q(1)\,\varphi_r(2)\varphi_s(2)}{r_{12}}\,\dd\mathbf r_1\dd\mathbf r_2",
             "two electrons"),
            (r"J_{pq}", r"=\eri ppqq", "Coulomb"),
            (r"K_{pq}", r"=\eri pqpq", "exchange"),
        ], size=36).move_to([-2.3, 1.15, 0])
        e1 = explain(r"$\eri pqrs$: electron 1 sits in the “charge” $\varphi_p\varphi_q$, electron 2 in $\varphi_r\varphi_s$; "
                     r"they repel as $1/r_{12}$", width=8.4)
        e2 = explain(r"$J$: two ordinary charge clouds $|\pa|^2$ and $|\pb|^2$ repelling: classical electrostatics", width=8.4)
        e3 = explain(r"$K$: no classical analogue; it comes from antisymmetry, the swapped term $B$, and is the overlap "
                     r"density $\pa\pb$ repelling itself", width=8.4)
        ex = m.VGroup(e1, e2, e3).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15).move_to([-2.0, -1.75, 0])
        ca = cloud(CYAN, [3.9, 1.3, 0], 1.6, 1.6)
        cb = cloud(ROSE, [6.1, 1.3, 0], 1.6, 1.6)
        rep = m.DoubleArrow([4.45, 1.3, 0], [5.55, 1.3, 0], buff=0, color=GOLD, stroke_width=3)
        jl = rich(r"$J$: $|\pa|^2$ repels $|\pb|^2$", 28).move_to([5.0, 2.35, 0])
        ck = cloud(VIOLET, [5.0, -0.85, 0], 2.6, 1.0)
        kl = rich(r"$K$: overlap density $\pa\pb$ repels itself", 28, width=3.6).move_to([5.0, -1.85, 0])
        self.say("[We need two kinds of integral. The first is the one-electron integral h p q: orbital phi p, times "
                 "the one-electron Hamiltonian acting on phi q, integrated over all space.] When p equals q this is "
                 "the energy of one electron alone in that orbital.", m.FadeIn(d.rows[0]))
        self.say("[The second is the two-electron integral, written p q r s in round brackets. Electron one sits in the "
                 "charge distribution phi p phi q, electron two in phi r phi s, and they repel as one over r one two.] "
                 "This is called chemists' notation: the first pair always belongs to electron one.",
                 m.AnimationGroup(m.FadeIn(d.rows[1]), m.FadeIn(e1)))
        self.say("[Two special cases matter. The Coulomb integral J p q is p p q q: two ordinary charge clouds, phi p "
                 "squared and phi q squared, repelling each other.] That is classical electrostatics.",
                 m.AnimationGroup(m.FadeIn(d.rows[2]), m.FadeIn(e2), m.FadeIn(ca), m.FadeIn(cb), m.GrowFromCenter(rep),
                                  m.FadeIn(jl)))
        self.say("[The exchange integral K p q is p q p q. Here the charge distribution is the overlap density, phi p "
                 "times phi q, repelling itself.] It has no classical analogue. It appears only because the "
                 "wavefunction is antisymmetric, through the swapped product B, and it will carry the whole "
                 "singlet triplet splitting.",
                 m.AnimationGroup(m.FadeIn(d.rows[3]), m.FadeIn(e3), m.FadeIn(ck), m.FadeIn(kl)))
        self.wait(0.4)


class S32Elementary(Frame):
    """06-energies.tex, frame 2: 'Two elementary integrals'."""

    TITLE = "Two elementary integrals"
    SUBTITLE = r"assume real orthonormal orbitals, $\braket{\varphi_p}{\varphi_q}=\delta_{pq}$; $\hat h(1)$ acts only on electron 1"
    SYMBOLS = (r"$\braket fg=\int f\,g\,\dd\mathbf r$ for real orbitals — $\mel f{\hat O}g=\int f\,\hat O\,g\,\dd\mathbf r$ "
               r"— $\delta_{qs}=1$ if $q=s$, else 0 — bra $\langle\cdot|$: left function, ket $|\cdot\rangle$: right function")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\mel{\varphi_p(1)\varphi_q(2)}{\hat h(1)}{\varphi_r(1)\varphi_s(2)}",
             r"=\underbrace{\mel{\varphi_p}{\hat h}{\varphi_r}}_{h_{pr}}\ \underbrace{\braket{\varphi_q}{\varphi_s}}_{\delta_{qs}}",
             r"the $\dd\mathbf r_1$ and $\dd\mathbf r_2$ integrals separate"),
            (r"\mel{\varphi_p(1)\varphi_q(2)}{\hat h(2)}{\varphi_r(1)\varphi_s(2)}", r"=\delta_{pr}\,h_{qs}",
             "same, roles swapped"),
            (r"\mel{\varphi_p(1)\varphi_q(2)}{r_{12}^{-1}}{\varphi_r(1)\varphi_s(2)}", r"=\eri prqs",
             r"$1/r_{12}$ ties them: no splitting"),
        ], size=34, why_gap=0.4).move_to([0, 0.75, 0])
        e = explain("bookkeeping rule: electron 1 carries the indices p, r (bra, ket), electron 2 carries q, s",
                    width=11.0).move_to([0, -1.85, 0])
        self.say("Every energy in this chapter is built from three elementary matrix elements between orbital products. "
                 "Assume real orthonormal orbitals.")
        self.say("[First, the one-electron operator for electron one. It acts only on electron one's coordinates, so "
                 "the integral over electron one gives h p r, and the integral over electron two is just the overlap "
                 "of phi q with phi s, which is delta q s.]", m.FadeIn(d.rows[0]))
        self.say("[Second, the operator for electron two: the same with the roles swapped, delta p r times h q s.]",
                 m.FadeIn(d.rows[1]))
        self.say("[Third, the repulsion. One over r one two depends on both electrons at once, so nothing separates, "
                 "and the result is the two-electron integral p r q s.]", m.FadeIn(d.rows[2]))
        self.say("[The bookkeeping rule: electron one carries the indices p and r, from the bra and the ket; electron "
                 "two carries q and s.]", m.FadeIn(e))
        self.wait(0.4)


class S33Triplet1(Frame):
    """06-energies.tex, frame 3: 'Triplet energy, step by step (1/2)'."""

    TITLE = "Triplet energy, step by step (1/2)"
    SYMBOLS = (r"$\Psi_T$: full triplet wavefunction, space times spin — $\Phi_T$: its spatial part — $A=\pa(1)\pb(2)$, "
               r"$B=\pb(1)\pa(2)$ — $\Theta_{1,M}$: any triplet spin function; the result is the same for $M=0,\pm1$")

    def construct(self) -> None:
        self.setup_frame()
        top = M(r"\Psi_T=", r"\tfrac1{\sqrt2}(", "A", "-", "B", ")", r"\,\Theta_{1,M},\quad"
                r"\Hop=\hat h(1)+\hat h(2)+r_{12}^{-1}\ (\text{no spin})\ \Rightarrow\ E_T=\mel{\Phi_T}{\Hop}{\Phi_T}"
                r"\braket{\Theta}{\Theta}", size=32)
        paint_parts(top, AB)
        brace = m.Brace(m.VGroup(*top[1:6]), m.DOWN, buff=0.06, color=MUTED)
        blabel = M(r"\Phi_T\ (\text{space})", size=24, color=MUTED).next_to(brace, m.DOWN, buff=0.05)
        top = m.VGroup(top, brace, blabel).move_to([0, 2.0, 0])
        head = rich(r"One-electron part — the $\tfrac12$ comes from $(\tfrac1{\sqrt2})^2$; four terms: $AA$, $BB$, $-AB$, $-BA$",
                    30, GOLD, width=12.6).move_to([0, 1.15, 0])
        d = Derivation([
            (r"\mel{A}{\hat h(1)+\hat h(2)}{A}", r"=h_{aa}\cdot1+1\cdot h_{bb}=h_a+h_b", r"$p=r=a$, $q=s=b$"),
            (r"\mel{B}{\hat h(1)+\hat h(2)}{B}", r"=h_{bb}+h_{aa}", "orbitals swapped"),
            (r"\mel{A}{\hat h(1)+\hat h(2)}{B}", r"=h_{ab}\underbrace{\delta_{ba}}_{0}+\underbrace{\delta_{ab}}_{0}h_{ba}=0",
             "orthogonality kills it"),
            (r"\tfrac12\bigl[(h_a+h_b)+(h_a+h_b)-0-0\bigr]", r"=\boxed{h_a+h_b}", ""),
        ], size=34, row_buff=0.25).move_to([0, -0.85, 0])
        self.say("[Now compute the triplet energy. The triplet is one over root two times A minus B, times a triplet spin "
                 "function. The Hamiltonian contains no spin, so the energy is the spatial expectation value times the "
                 "spin overlap, which is one.]", m.FadeIn(top))
        self.say("[Start with the one-electron part. Squaring one over root two gives a factor of one half, and there "
                 "are four terms: A with A, B with B, and minus the two cross terms.]", m.FadeIn(head))
        self.say("[A with A: electron one carries a and a, electron two b and b, so the result is h a a times one, plus "
                 "one times h b b: h a plus h b.]", m.FadeIn(d.rows[0]))
        self.say("[B with B is the same with the orbitals swapped.]", m.FadeIn(d.rows[1]))
        self.say("[The cross term A with B: each piece contains an overlap of a with b, which is zero, so orthogonality "
                 "kills it.]", m.FadeIn(d.rows[2]))
        self.say("[So the one-electron part is one half of h a plus h b, twice: just h a plus h b.]",
                 m.FadeIn(d.rows[3]))
        self.wait(0.4)


class S34Triplet2(Frame):
    """06-energies.tex, frame 4: 'Triplet energy, step by step (2/2)'."""

    TITLE = "Triplet energy, step by step (2/2)"
    SYMBOLS = (r"$\eri abba=\eri abab=K_{ab}$ for real orbitals, by the eightfold symmetry of the integrals — "
               r"$J_{ab}\ge K_{ab}\ge0$, proved in Part VI")

    def construct(self) -> None:
        self.setup_frame()
        head = rich("Two-electron part — the same four terms, now with $1/r_{12}$", 32, GOLD).move_to([0, 2.15, 0])
        d = Derivation([
            (r"\mel{A}{r_{12}^{-1}}{A}", r"=\eri aabb=J_{ab}", r"$p,r=a$; $q,s=b$: two charge clouds"),
            (r"\mel{B}{r_{12}^{-1}}{B}", r"=\eri bbaa=J_{ab}", "same clouds, labels swapped"),
            (r"\mel{A}{r_{12}^{-1}}{B}", r"=\eri abba=K_{ab}", r"$p=a,r=b$; $q=b,s=a$: overlap densities"),
            (r"\tfrac12\bigl[J+J-K-K\bigr]", r"=J_{ab}-K_{ab}", r"the minus of $A-B$"),
        ], size=36).move_to([0, 0.35, 0])
        res = Box(rich(r"$E_T=h_a+h_b+J_{ab}-K_{ab}$ — the cross terms carry the sign of the combination", 32),
                  "result").move_to([0, -2.1, 0])
        self.say("[Now the two-electron part: the same four terms, with one over r one two.]", m.FadeIn(head))
        self.say("[A with A: electron one carries a and a, electron two b and b, giving a a b b: the Coulomb integral J "
                 "a b, two charge clouds repelling.]", m.FadeIn(d.rows[0]))
        self.say("[B with B gives the same clouds with the labels swapped: again J a b.]", m.FadeIn(d.rows[1]))
        self.say("[The cross term A with B: electron one carries a and b, electron two b and a, giving a b b a, which for "
                 "real orbitals equals the exchange integral K a b.] Each electron now sits in an overlap density.",
                 m.FadeIn(d.rows[2]))
        self.say("[Adding up with the factor one half and the minus sign from A minus B gives J a b minus K a b.]",
                 m.FadeIn(d.rows[3]))
        self.say("[So the triplet energy is h a plus h b plus J a b minus K a b.] The cross terms carry the sign of the "
                 "combination, and that sign is the whole story.", m.FadeIn(res))
        self.wait(0.4)


class S35Gap(Frame):
    """06-energies.tex, frame 5: 'Open-shell singlet and the gap'."""

    TITLE = "Open-shell singlet and the gap"
    SYMBOLS = (r"the same orbitals in both states: “frozen orbitals” — the whole singlet–triplet splitting is carried by "
               r"the exchange integral $K_{ab}$")

    def construct(self) -> None:
        self.setup_frame()
        top = M(r"\Psi_{\OSS}=\tfrac1{\sqrt2}(", "A", "+", "B", r")\,\Theta_{0,0}", size=38)
        paint_parts(top, AB)
        tt = m.VGroup(top, rich(": identical steps, but the cross terms enter with +", 30)).arrange(m.RIGHT, buff=0.15)
        tt.move_to([0, 2.1, 0])
        d = Derivation([
            (r"E_{\OSS}", r"=h_a+h_b+\tfrac12\bigl[J+J+K+K\bigr]", r"the $+$ of $A+B$"),
            ("", r"=h_a+h_b+J_{ab}+K_{ab}", ""),
            (r"E_{\OSS}-E_T", r"=(J_{ab}+K_{ab})-(J_{ab}-K_{ab})=\boxed{2K_{ab}}", r"$h$ and $J$ cancel"),
        ], size=38).move_to([0, 0.5, 0])
        lt = m.Line([-2.5, -2.3, 0], [-1.1, -2.3, 0], color=ROSE, stroke_width=4)
        ls = m.Line([-2.5, -1.2, 0], [-1.1, -1.2, 0], color=BLUE, stroke_width=4)
        tl = M(r"E_T=h_a+h_b+J-K", size=32, color=ROSE).next_to(lt, m.RIGHT, buff=0.3)
        sl = M(r"E_{\OSS}=h_a+h_b+J+K", size=32, color=BLUE).next_to(ls, m.RIGHT, buff=0.3)
        gap = m.DoubleArrow([-1.8, -2.25, 0], [-1.8, -1.25, 0], buff=0, color=GOLD, stroke_width=3)
        gl = M("2K", size=32, color=GOLD).next_to(gap, m.LEFT, buff=0.15)
        self.say("[The open-shell singlet is one over root two times A plus B, times the singlet spin function. The "
                 "steps are identical, except that the cross terms now enter with a plus sign.]", m.FadeIn(tt))
        self.say("[So the two-electron part is one half of J plus J plus K plus K,] [and the singlet energy is h a plus "
                 "h b plus J a b plus K a b.]", m.FadeIn(d.rows[0]), m.FadeIn(d.rows[1]))
        self.say("[Subtract the triplet energy: h and J cancel, and the singlet lies above the triplet by exactly two "
                 "K a b.]", m.FadeIn(d.rows[2]))
        self.say("[With the same orbitals in both states, the whole singlet triplet splitting is carried by the exchange "
                 "integral.]", m.AnimationGroup(m.Create(lt), m.Create(ls), m.FadeIn(tl), m.FadeIn(sl),
                                                m.GrowFromCenter(gap), m.FadeIn(gl)))
        self.wait(0.4)


class S36ClosedShells(Frame):
    """06-energies.tex, frame 6: 'The closed shells and their couplings'."""

    TITLE = "The closed shells and their couplings"
    SYMBOLS = (r"$\Phi_{\text i}=\pa(1)\pa(2)$: closed shell i, spin part $\Theta_{0,0}$ — $\Phi_{\OSS}=\tfrac1{\sqrt2}(A+B)$ "
               r"— states of different $S$ never couple, because their spin parts are orthogonal")

    def construct(self) -> None:
        self.setup_frame()
        h1 = rich("Diagonal — both electrons in one orbital", 30, GOLD)
        dg = Derivation([(r"E_{\text i}", r"=2h_a+J_{aa}", ""), (r"E_{\text{ii}}", r"=2h_b+J_{bb}", "")], size=36)
        e1 = explain(r"two electrons in $\pa$: $2h_a$, plus one repulsion $J_{aa}$ of the cloud $|\pa|^2$ with itself",
                     width=6.0)
        h2 = rich(r"i – ii: one-electron terms vanish, $\delta_{ab}=0$", 30, GOLD)
        k = M(r"\mel{\pa\pa}{r_{12}^{-1}}{\pb\pb}=\eri abab=K_{ab}", size=34)
        left = m.VGroup(h1, dg, e1, h2, k).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.28).move_to([-3.45, 0.15, 0])
        h3 = rich("i – OSS", 30, GOLD)
        d = Derivation([
            (r"\mel{\Phi_{\text i}}{\Hop}{\Phi_{\OSS}}", r"=\tfrac1{\sqrt2}\bigl[\mel{\pa\pa}{\Hop}{A}+\mel{\pa\pa}{\Hop}{B}\bigr]", ""),
            (r"\mel{\pa\pa}{\hat h(1)+\hat h(2)}{A}", r"=0+h_{ab}", ""),
            (r"\mel{\pa\pa}{r_{12}^{-1}}{A}", r"=\eri aaab=\mel{\pa\pa}{r_{12}^{-1}}{B}", ""),
            (r"\mel{\Phi_{\text i}}{\Hop}{\Phi_{\OSS}}", r"=\sqrt2\,\bigl(h_{ab}+\eri aaab\bigr)", ""),
        ], size=28, row_buff=0.26)
        e2 = explain(r"$\hat h(1)$ term: $h_{aa}\braket{\pa}{\pb}=0$; $\hat h(2)$ term: $\braket{\pa}{\pa}h_{ab}=h_{ab}$",
                     width=6.2)
        right = m.VGroup(h3, d, e2).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.28).move_to([3.4, 0.15, 0])
        self.say("[Now the closed shells. With both electrons in phi a, the energy is two h a, one for each electron, "
                 "plus a single repulsion, J a a, of the cloud phi a squared with itself.] [The same for phi b.]",
                 m.AnimationGroup(m.FadeIn(h1), m.FadeIn(dg.rows[0]), m.FadeIn(e1)), m.FadeIn(dg.rows[1]))
        self.say("[Between the two closed shells, the one-electron terms vanish by orthogonality, and the repulsion "
                 "gives phi a phi a with phi b phi b, which is a b a b: the exchange integral K a b again.]",
                 m.AnimationGroup(m.FadeIn(h2), m.FadeIn(k)))
        self.say("[The coupling between closed shell one and the open-shell singlet is one over root two times the sum "
                 "of the matrix elements with A and with B.]", m.AnimationGroup(m.FadeIn(h3), m.FadeIn(d.rows[0])))
        self.say("[For the one-electron part with A: the h of one term gives h a a times the overlap of a with b, zero; "
                 "the h of two term gives the overlap of a with a, one, times h a b.]",
                 m.AnimationGroup(m.FadeIn(d.rows[1]), m.FadeIn(e2)))
        self.say("[The repulsion with A gives a a a b, and B gives the same.]", m.FadeIn(d.rows[2]))
        self.say("[Altogether: root two times h a b plus a a a b.] States of different total spin never couple, because "
                 "their spin parts are orthogonal, so the triplet stays on its own.", m.FadeIn(d.rows[3]))
        self.wait(0.4)


class S37FullH(Frame):
    """06-energies.tex, frame 7: 'The full two-electron, two-orbital Hamiltonian'."""

    TITLE = "The full two-electron, two-orbital Hamiltonian"
    SYMBOLS = (r"$\mathbf H_S$: Hamiltonian matrix in the singlet configurations — full CI: exact diagonalisation in all "
               r"determinants — $\Eh$: hartree, $27.211$ eV")

    def construct(self) -> None:
        self.setup_frame()
        basis = rich(r"basis $\{\Phi_{\text i},\Phi_{\text{ii}},\Phi_{\OSS}\}$, the singlets, plus the triplet on its own",
                     30).move_to([0, 2.15, 0])
        H = M(r"\mathbf H_S=\begin{pmatrix}2h_a+J_{aa} & K_{ab} & \sqrt2\,(h_{ab}+\eri aaab)\\ K_{ab} & 2h_b+J_{bb} & "
              r"\sqrt2\,(h_{ab}+\eri bbba)\\ \cdot & \cdot & h_a+h_b+J_{ab}+K_{ab}\end{pmatrix},\qquad "
              r"E_T=h_a+h_b+J_{ab}-K_{ab}", size=34).move_to([0, 0.95, 0])
        e = explain(r"diagonalising $\mathbf H_S$ gives the three exact singlet energies of this model; the matrix is "
                    r"symmetric, dots are mirror entries", width=12.0).next_to(H, m.DOWN, buff=0.25)
        sym = rich(r"orbitals of different symmetry, such as $\sigma_g$ and $\sigma_u$ of H$_2$, give "
                   r"$h_{ab}=\eri aaab=\eri bbba=0$: the open-shell singlet decouples", 30, width=12.4)
        sym.next_to(e, m.DOWN, buff=0.3)
        chk = boxed(r"5 random integral sets, with a positive-definite kernel, into PySCF full CI: the singlet and triplet "
                    r"roots reproduce these closed forms to $2\times10^{-14}\,\Eh$.", "checked", width=12.4, size=28,
                    tag="T2: brute force").next_to(sym, m.DOWN, buff=0.3)
        self.say("[Collecting everything: in the basis of the three singlets, the two closed shells and the open-shell "
                 "singlet, the Hamiltonian is a three by three matrix, and the triplet sits on its own.]",
                 m.AnimationGroup(m.FadeIn(basis), m.Write(H)))
        self.say("[The diagonal holds the three energies we derived. The closed shells couple through K a b, and each "
                 "couples to the open-shell singlet through root two times h a b plus a mixed integral. Diagonalising "
                 "this matrix gives the three exact singlet energies of the model.]", m.FadeIn(e))
        self.say("[If the two orbitals have different symmetry, like the sigma g and sigma u orbitals of H two, the "
                 "mixed integrals vanish and the open-shell singlet decouples from the closed shells.]",
                 m.FadeIn(sym))
        self.say("[Test T two checked this by brute force: five random sets of integrals, built from a positive-definite "
                 "kernel, were diagonalised with PySCF's full configuration interaction, and the singlet and triplet "
                 "roots match these closed forms to two times ten to the minus fourteen hartree.] That is the limit of "
                 "double-precision arithmetic.", m.FadeIn(chk))
        self.wait(0.4)


class S38HundFrozen(Frame):
    """06-energies.tex, frame 8: 'Hund's rule at frozen orbitals'."""

    TITLE = "Hund's rule at frozen orbitals"
    SYMBOLS = (r"multiplicity $2S+1$: 3 for the triplet, 1 for the singlet — Hund's rule, 1925, was found empirically "
               r"from atomic spectra; the wording quoted is the review's, citing the IUPAC Gold Book")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"of the different multiplets resulting from different configurations of electrons in degenerate '
                      'orbitals of an atom those with greatest multiplicity have the lowest energy"', "claim", width=7.0,
                      size=28, tag="The review states Hund's rule, p. 442").move_to([-3.0, 1.35, 0])
        same = rich("With the same orbitals in both states:", 30).next_to(claim, m.DOWN, buff=0.4).align_to(claim, m.LEFT)
        eq = M(r"E_T-E_{\OSS}=-2K_{ab}<0\quad\text{if }K_{ab}>0", size=38).next_to(same, m.DOWN, buff=0.25)
        eq.align_to(claim, m.LEFT)
        todo = rich("Two things to prove: K ≥ 0, in the next part, and whether “same orbitals” is legitimate — it is not.",
                    30, GOLD, width=7.0).next_to(eq, m.DOWN, buff=0.35).align_to(claim, m.LEFT)
        pic = m.VGroup(level(3.9, -0.7, 0.9), level(5.4, -0.7, 0.9), spin(3.9, -0.7, True), spin(5.4, -0.7, True),
                       level(3.9, 1.1, 0.9), level(5.4, 1.1, 0.9), spin(3.9, 1.1, True), spin(5.4, 1.1, False))
        lo = rich("lower: $J-K$", 28, ROSE).move_to([4.65, -1.35, 0])
        hi = rich("higher: $J+K$", 28, BLUE).move_to([4.65, 0.45, 0])
        self.say("[The review states Hund's rule in these words: of the different multiplets resulting from different "
                 "configurations of electrons in degenerate orbitals of an atom, those with greatest multiplicity have "
                 "the lowest energy.]", m.FadeIn(claim))
        self.say("[With the same orbitals in both states, our result reproduces it: the triplet lies below the singlet "
                 "by two K, provided K is positive.]",
                 m.AnimationGroup(m.FadeIn(same), m.Write(eq), m.FadeIn(pic), m.FadeIn(lo), m.FadeIn(hi)))
        self.say("[Two things remain to be proved. First, that K is never negative, which comes next. Second, whether "
                 "using the same orbitals in both states is legitimate.] We will see that it is not, and that the true "
                 "reason for Hund's rule is different.", m.FadeIn(todo))
        self.wait(0.4)
