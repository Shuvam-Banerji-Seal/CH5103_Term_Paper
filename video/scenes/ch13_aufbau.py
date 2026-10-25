"""Chapter 13: the aufbau principle on trial (presentation/sections/15-aufbau.tex)."""
import manimgx as m

from ch01_foundations import explain
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ORANGE, ROSE, Box, Derivation, Frame, M, boxed, bullets, level,
                  pill, rich)


class S94Prosecution(Frame):
    """15-aufbau.tex, frame 1: 'The prosecution'."""

    TITLE = "The prosecution"
    SYMBOLS = (r"aufbau, German “building up”: fill orbitals in order of energy, two electrons each — stationary state: "
               r"eigenstate of $\Hop$, unchanged in time apart from a phase — conserved: its quantum number commutes "
               r"with $\Hop$")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"the aufbau principle, by assuming the existence of unchanging stationary individual electronic '
                      'states, violates the Pauli exclusion principle. Only the many-electron system as a whole '
                      'possesses stationary states." — p. 448', "claim", width=12.6, size=29).move_to([0, 1.45, 0])
        ex = [("Exhibit A", "one-electron quantum numbers are not conserved"),
              ("Exhibit B", "the adiabatic argument behind “building up”"),
              ("Exhibit C", "the 3d/4s paradox")]
        panels = m.VGroup(*[boxed(f"**{a}**\n\n{b}", "plain", width=3.9, size=27) for a, b in ex])
        panels.arrange(m.RIGHT, buff=0.35, aligned_edge=m.UP).move_to([0, -1.0, 0])
        self.say("[Part fourteen puts the aufbau principle on trial. Aufbau is German for building up: fill orbitals in "
                 "order of energy, two electrons each. The prosecution, in the review's words: the aufbau principle, by "
                 "assuming the existence of unchanging stationary individual electronic states, violates the Pauli "
                 "exclusion principle. Only the many-electron system as a whole possesses stationary states.]",
                 m.FadeIn(claim))
        self.say("[We examine three exhibits. Exhibit A: one-electron quantum numbers are not conserved.]",
                 m.FadeIn(panels[0]))
        self.say("[Exhibit B: the adiabatic argument behind building up.]", m.FadeIn(panels[1]))
        self.say("[Exhibit C: the paradox of the three d and four s orbitals.]", m.FadeIn(panels[2]))
        self.wait(0.4)


class S95ExhibitA(Frame):
    """15-aufbau.tex, frame 2: 'Exhibit A: [l_1z, 1/r_12] != 0'."""

    TITLE = r"Exhibit A: $[\hat l_{1z},1/r_{12}]\neq0$"
    SYMBOLS = (r"$\hat l_{1z}$: $z$-angular momentum of electron 1 alone, $\hbar=1$ — $r_{12}$: distance between electrons "
               r"1 and 2 — $[\hat A,\hat B]=\hat A\hat B-\hat B\hat A$ — $f$: any test function — first-order: "
               r"$\hat l_{1z}(Vf)=(\hat l_{1z}V)f+V\hat l_{1z}f$")

    def construct(self) -> None:
        self.setup_frame()
        defs = M(r"\hat l_{1z}=-i(x_1\partial_{y_1}-y_1\partial_{x_1}),\quad \partial_{y_1}r_{12}^{-1}=-\frac{y_1-y_2}{r_{12}^3},"
                 r"\quad \partial_{x_1}r_{12}^{-1}=-\frac{x_1-x_2}{r_{12}^3}", size=34).move_to([0, 2.0, 0])
        e = explain(r"chain rule on $r_{12}^{-1}=[(x_1-x_2)^2+(y_1-y_2)^2+(z_1-z_2)^2]^{-1/2}$", width=11)
        e.next_to(defs, m.DOWN, buff=0.15)
        d = Derivation([
            (r"\hat l_{1z}\,r_{12}^{-1}", r"=-i\,\frac{-x_1(y_1-y_2)+y_1(x_1-x_2)}{r_{12}^3}", "insert both derivatives"),
            ("", r"=-i\,\frac{-x_1y_1+x_1y_2+y_1x_1-y_1x_2}{r_{12}^3}", "multiply out"),
            ("", r"=-i\,\frac{x_1y_2-x_2y_1}{r_{12}^3}\neq0", "only the cross terms survive"),
        ], size=34, why_size=24).move_to([0, -0.75, 0])
        cancelled = M(r"=-i\,\frac{\cancel{-x_1y_1}+x_1y_2+\cancel{y_1x_1}-y_1x_2}{r_{12}^3}", size=34)
        cancelled.move_to(d.rows[1][1], aligned_edge=m.LEFT)
        first = rich(r"first-order operator: $[\hat l_{1z},V]f=(\hat l_{1z}V)f$ ⇒ $l_{1z}$ is not a constant of motion",
                     28).move_to([0, -2.5, 0])
        self.say("[Exhibit A. The z angular momentum of electron one alone is minus i times x one d by d y one minus y one "
                 "d by d x one. By the chain rule on one over r one two, its derivatives with respect to y one and x one "
                 "are minus y one minus y two over r cubed, and minus x one minus x two over r cubed.]",
                 m.AnimationGroup(m.FadeIn(defs), m.FadeIn(e)))
        self.say("[Apply l one z to one over r one two by inserting both derivatives.]", m.FadeIn(d.rows[0]))
        self.say("[Multiply out the numerator: minus x one y one, plus x one y two, plus y one x one, minus y one x two.]",
                 m.FadeIn(d.rows[1]))
        self.say("[The first and third terms cancel.]", m.Transform(d.rows[1][1], cancelled))
        self.say("[Only the cross terms survive: minus i times x one y two minus x two y one, over r cubed. That is not "
                 "zero.]", m.FadeIn(d.rows[2]))
        self.say("[Because l one z is a first-order differential operator, its commutator with the repulsion acting on "
                 "any function is just l one z applied to the repulsion, times the function. It is not zero, so the "
                 "angular momentum of one electron is not a constant of motion.]", m.FadeIn(first))
        self.wait(0.4)


class S96TotalConserved(Frame):
    """15-aufbau.tex, frame 3: '... but the total is conserved'."""

    TITLE = "… but the total is conserved"
    SYMBOLS = (r"$\hat{\mathbf L}=\sum_i\hat{\mathbf l}_i$: total orbital angular momentum — $\hat S^2$: total spin squared — "
               r"central field: the nuclear attraction depends only on $|\mathbf r_i|$")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\hat l_{2z}\,r_{12}^{-1}", r"=-i\,\frac{x_2y_1-x_1y_2}{r_{12}^3}",
             r"same steps; $\partial_{y_2}r_{12}^{-1}=+\tfrac{y_1-y_2}{r_{12}^3}$ flips the sign"),
            (r"(\hat l_{1z}+\hat l_{2z})\,r_{12}^{-1}", r"=-i\,\frac{(x_1y_2-x_2y_1)+(x_2y_1-x_1y_2)}{r_{12}^3}=0",
             "equal and opposite"),
        ], size=34, why_size=24).move_to([0, 1.3, 0])
        res = boxed(r"atom, central field, spin-free $\Hop$: $[\Hop,\hat{\mathbf L}]=0$, $[\Hop,\hat S^2]=0$, but "
                    r"$[\Hop,\hat{\mathbf l}_i]\neq0$", "result", width=6.0, size=28).move_to([-3.3, -1.2, 0])
        why = rich(r"$\hat{\mathbf L}$ rotates both electrons together, keeping $r_{12}$; $\hat{\mathbf l}_1$ rotates one, "
                   r"changing $r_{12}$. In a molecule even $\hat{\mathbf L}$ is lost; $\hat S^2$ survives.", 27, width=5.8)
        why.move_to([3.4, -0.95, 0])
        t13 = m.VGroup(pill("verified"), rich("T13, SymPy on an arbitrary $f$", 26, MUTED)).arrange(m.RIGHT, buff=0.2)
        t13.next_to(why, m.DOWN, buff=0.3).align_to(why, m.LEFT)
        self.say("[But the total is conserved. For electron two the same steps give the opposite sign, because the "
                 "derivative with respect to y two of one over r one two has a plus sign.]", m.FadeIn(d.rows[0]))
        self.say("[Add the two: the cross terms are equal and opposite, and the sum is zero.]", m.FadeIn(d.rows[1]))
        self.say("[So in an atom, with a central field and a spin-free Hamiltonian, the total orbital angular momentum and "
                 "the total spin squared commute with the Hamiltonian, but the angular momentum of each electron does "
                 "not.]", m.FadeIn(res))
        self.say("[The reason is geometric. The total angular momentum rotates both electrons together and keeps their "
                 "distance; the angular momentum of electron one rotates it alone and changes the distance. In a "
                 "molecule even the total orbital angular momentum is lost, while the total spin survives.]",
                 m.FadeIn(why))
        self.say("[Test T thirteen checked these commutators in SymPy on an arbitrary function.]", m.FadeIn(t13))
        self.wait(0.4)


class S97Adiabatic(Frame):
    """15-aufbau.tex, frame 4: 'Exhibit B: the adiabatic theorem'."""

    TITLE = "Exhibit B: the adiabatic theorem"
    SYMBOLS = (r"$\psi_n(t)$, $E_n(t)$: eigenstates/energies of $\Hop$ at time $t$ — $c_n$: amplitudes — $\theta_n$: dynamic "
               r"phase — dot: time derivative — off-diagonal coupling: differentiate $\Hop\psi_n=E_n\psi_n$ and project, "
               r"$m\neq n$")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('Bohr assumed stationary states survive "addition of an electron and a proton"; this rests on '
                      'Ehrenfest\'s adiabatic principle, which "does not apply to aperiodic systems" — p. 448', "claim",
                      width=12.6, size=28).move_to([0, 1.9, 0])
        d = Derivation([
            (r"\Psi(t)", r"=\textstyle\sum_nc_n(t)\,e^{i\theta_n(t)}\psi_n(t),\quad\theta_n=-\int_0^tE_n\,\dd t'",
             "expand in snapshot eigenstates"),
            (r"\dot c_m", r"=-\textstyle\sum_nc_n\braket{\psi_m}{\dot\psi_n}e^{i(\theta_n-\theta_m)}",
             r"insert in $i\dot\Psi=\Hop\Psi$, project on $\psi_m$"),
            (r"\braket{\psi_m}{\dot\psi_n}", r"=\frac{\mel{\psi_m}{\dot{\Hop}}{\psi_n}}{E_n-E_m}",
             r"differentiate $\Hop\psi_n=E_n\psi_n$, $m\neq n$"),
        ], size=32, why_size=24).move_to([0, -0.3, 0])
        concl = rich(r"slow $\dot{\Hop}$, finite gaps ⇒ the system stays in the *continuously connected* eigenstate. "
                     r"**But**: adding a particle changes the Hilbert space, no continuous path, and the conserved labels "
                     r"are $L,S$ of the *whole* system, never one-electron labels.", 27, width=12.4).move_to([0, -2.3, 0])
        self.say("[Exhibit B. The review says that Bohr assumed stationary states survive the addition of an electron "
                 "and a proton; that this rests on Ehrenfest's adiabatic principle; and that the principle does not apply "
                 "to aperiodic systems.]", m.FadeIn(claim))
        self.say("[What does the adiabatic theorem actually say? Expand the state in the eigenstates of the Hamiltonian "
                 "at each instant, with amplitudes c n and dynamic phases theta n, minus the integral of the energy.]",
                 m.FadeIn(d.rows[0]))
        self.say("[Insert this into the time-dependent Schrödinger equation and project on psi m. The phase terms cancel "
                 "the energies, and what is left is: the rate of change of c m is minus the sum over n of c n times the "
                 "overlap of psi m with the time derivative of psi n, times a phase factor.]", m.FadeIn(d.rows[1]))
        self.say("[Differentiate the eigenvalue equation and project on psi m: that overlap is the matrix element of the "
                 "time derivative of the Hamiltonian, divided by the energy gap.]", m.FadeIn(d.rows[2]))
        self.say("[So if the Hamiltonian changes slowly and the gaps stay finite, the couplings are small, and the system "
                 "stays in the continuously connected eigenstate.] But adding a particle changes the Hilbert space "
                 "itself, so there is no continuous path; and the labels that are conserved are L and S of the whole "
                 "system, never one-electron labels.", m.FadeIn(concl))
        self.wait(0.4)


class S98Paradox(Frame):
    """15-aufbau.tex, frame 5: 'Exhibit C: the 3d/4s paradox'."""

    TITLE = "Exhibit C: the 3d/4s paradox"
    SYMBOLS = (r"$d^{n_d}s^{n_s}$: $n_d$ electrons in 3d, $n_s$ in 4s — $h$: kinetic + nuclear + core terms — $\bar J$: "
               r"repulsion averaged over spin/orbital arrangements, exchange folded in")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('in neutral atoms 4s lies slightly above 3d when both are populated, so 4s is ionised first; '
                      '"however, 4s orbital is also populated first, because it offers less repulsion with a 3d electron '
                      'than that between two 3d electrons" … "re-evaluated in the new configurations" — p. 448', "claim",
                      width=12.6, size=28).move_to([0, 1.6, 0])
        assume = boxed(r"one-electron energies $h_d,h_s$; one average repulsion per pair type: $\bar J_{dd}$, "
                       r"$\bar J_{ds}$, $J_{ss}$; each electron pays $h$ once, each of the $\tbinom n2=n(n-1)/2$ pairs "
                       r"pays its $J$ once", "assume", width=12.6, size=27, tag="Average of configuration")
        assume.move_to([0, -0.3, 0])
        E = M(r"E(d^{n_d}s^{n_s})=n_dh_d+n_sh_s+\tbinom{n_d}{2}\bar J_{dd}+n_dn_s\bar J_{ds}+\tbinom{n_s}{2}J_{ss}",
              size=38).move_to([0, -1.95, 0])
        self.say("[Exhibit C, the three d four s paradox. The review says: in neutral atoms four s lies slightly above "
                 "three d when both are populated, so four s is ionised first; however, four s is also populated first, "
                 "because it offers less repulsion with a three d electron than that between two three d electrons; "
                 "orbital energies must be re-evaluated in the new configurations.] Let us make this precise.",
                 m.FadeIn(claim))
        self.say("[Use the average-of-configuration model. Each orbital type has a one-electron energy, h d or h s, and "
                 "each type of pair has one average repulsion, J bar d d, J bar d s, and J s s. Each electron pays its h "
                 "once, and each pair pays its J once; n electrons form n times n minus one over two pairs.]",
                 m.FadeIn(assume))
        self.say("[So a configuration with n d electrons in three d and n s in four s has energy n d h d plus n s h s, "
                 "plus n d choose two times J bar d d, plus n d times n s times J bar d s, plus n s choose two times J s "
                 "s.]", m.Write(E))
        self.wait(0.4)


class S99Algebra(Frame):
    """15-aufbau.tex, frame 6: '3d/4s: the algebra'."""

    TITLE = "3d/4s: the algebra"
    SYMBOLS = (r"$\Delta>0$: $d^ns^2$ is lower — $\varepsilon_d,\varepsilon_s$: orbital energies *in* $d^ns^2$, as "
               r"frozen-orbital removal energies, Koopmans")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"E(d^ns^2)", r"=nh_d+2h_s+\tbinom n2\bar J_{dd}+2n\bar J_{ds}+J_{ss}", r"$n_d=n$, $n_s=2$"),
            (r"E(d^{n+1}s)", r"=(n+1)h_d+h_s+\tbinom{n+1}2\bar J_{dd}+(n+1)\bar J_{ds}", "move one 4s electron to 3d"),
            (r"\Delta\equiv E(d^{n+1}s)-E(d^ns^2)", r"=h_d-h_s+n\bar J_{dd}+(1-n)\bar J_{ds}-J_{ss}",
             r"$\tbinom{n+1}2-\tbinom n2=n$"),
            (r"\varepsilon_d=E(d^ns^2)-E(d^{n-1}s^2)", r"=h_d+(n-1)\bar J_{dd}+2\bar J_{ds}", "remove a 3d electron"),
            (r"\varepsilon_s=E(d^ns^2)-E(d^ns^1)", r"=h_s+n\bar J_{ds}+J_{ss}", "remove a 4s electron"),
        ], size=31, why_size=23).move_to([0, 0.55, 0])
        res = Box(m.VGroup(M(r"\Delta=(\varepsilon_d-\varepsilon_s)+\bigl(\bar J_{dd}-\bar J_{ds}\bigr)", size=40),
                           rich("T12; Lean `three_d_four_s`", 26, MUTED)).arrange(m.RIGHT, buff=0.5),
                  "result").move_to([0, -2.15, 0])
        self.say("[Now the algebra. With n three d electrons and two four s electrons: n h d plus two h s, plus n choose "
                 "two J bar d d, plus two n J bar d s, plus one J s s.]", m.FadeIn(d.rows[0]))
        self.say("[Move one four s electron into three d: n plus one h d plus h s, plus n plus one choose two J bar d d, "
                 "plus n plus one J bar d s, and no s s pair.]", m.FadeIn(d.rows[1]))
        self.say("[Subtract, calling the difference delta. Since n plus one choose two minus n choose two is n, delta is h "
                 "d minus h s, plus n J bar d d, plus one minus n times J bar d s, minus J s s.]", m.FadeIn(d.rows[2]))
        self.say("[The orbital energies in d n s two, as frozen-orbital removal energies: removing a three d electron "
                 "costs h d plus n minus one J bar d d plus two J bar d s,] [and removing a four s electron costs h s "
                 "plus n J bar d s plus J s s.]", m.FadeIn(d.rows[3]), m.FadeIn(d.rows[4]))
        self.say("[Subtract the orbital energies from delta: every h and every J s s cancels, the J bar d d terms leave "
                 "one, the J bar d s terms leave minus one. So delta equals epsilon d minus epsilon s, plus J bar d d "
                 "minus J bar d s.] Test T twelve checks this symbolically, and the Lean theorem three d four s proves "
                 "it.", m.FadeIn(res))
        self.wait(0.4)


class S100Reading(Frame):
    """15-aufbau.tex, frame 7: '3d/4s: reading the identity'."""

    TITLE = "3d/4s: reading the identity"
    SYMBOLS = (r"compact: small mean radius, so two 3d electrons sit close together — diffuse: spread out — IP: ionisation "
               r"potential — numbers in $E_{\mathrm h}$, chosen only to show the mechanism")

    def construct(self) -> None:
        self.setup_frame()
        pts = bullets([r"compact 3d, diffuse 4s suggests $\bar J_{dd}>\bar J_{ds}$ — a heuristic, not derived",
                       r"even with $\varepsilon_d<\varepsilon_s$: $\Delta>0$ if $\bar J_{dd}-\bar J_{ds}>\varepsilon_s-"
                       r"\varepsilon_d$ — **$d^ns^2$ wins**: 4s “fills first”",
                       r"from $d^ns^2$: Koopmans IPs $-\varepsilon_s<-\varepsilon_d$ — **4s leaves first**"],
                      width=6.6, size=28).move_to([-3.0, 0.75, 0])
        arrow = m.Arrow([2.6, -1.5, 0], [2.6, 1.9, 0], buff=0, color=MUTED, stroke_width=3)
        el = rich("energy", 24, MUTED).next_to(arrow, m.UP, buff=0.08)
        ls = level(3.6, 0.85, 1.4, colour=CYAN)
        ld = level(3.6, -0.35, 1.4, colour=GOLD)
        lsl = rich(r"$\varepsilon_s=-0.90$", 26, CYAN).next_to(ls, m.RIGHT, buff=0.15)
        ldl = rich(r"$\varepsilon_d=-1.50$", 26, GOLD).next_to(ld, m.RIGHT, buff=0.15)
        nums = rich(r"illustrative numbers, $n=2$: $\bar J_{dd}=0.8$, $\bar J_{ds}=0.1$", 24, MUTED, width=4.2)
        nums.move_to([4.55, -1.2, 0])
        delta = rich(r"$\Delta=-0.6+0.7=+0.10$", 30, GREEN).move_to([4.55, -1.95, 0])
        moral = rich("orbital energies belong to a *configuration*: the building-up and removal orders need not agree", 28,
                     width=12.4).move_to([0, -2.6, 0])
        self.say("[How to read the identity. A compact three d orbital and a diffuse four s orbital suggest that J bar d "
                 "d is larger than J bar d s; that is a heuristic, not something we derived.]", m.FadeIn(pts[0]))
        self.say("[Then even when epsilon d lies below epsilon s, delta is positive if the repulsion difference exceeds "
                 "the orbital energy gap. The configuration d n s two wins: four s fills first.]", m.FadeIn(pts[1]))
        self.say("[But starting from d n s two, Koopmans' theorem makes the four s ionisation energy the smaller one, so "
                 "four s leaves first.]", m.FadeIn(pts[2]))
        self.say("[Some illustrative numbers, with n equal to two: epsilon s minus zero point nine, epsilon d minus one "
                 "point five, J bar d d zero point eight and J bar d s zero point one hartree. The orbital gap gives minus "
                 "zero point six, the repulsion difference gives plus zero point seven, and delta is plus zero point one: "
                 "d two s two is lower, although three d is the lower orbital.]",
                 m.AnimationGroup(m.GrowArrow(arrow), m.FadeIn(el), m.FadeIn(ls), m.FadeIn(ld), m.FadeIn(lsl),
                                  m.FadeIn(ldl), m.FadeIn(nums), m.FadeIn(delta)))
        self.say("[The moral: orbital energies belong to a configuration, so the order of building up and the order of "
                 "removal need not agree. There is no paradox.]", m.FadeIn(moral))
        self.wait(0.4)


class S101Verdict(Frame):
    """15-aufbau.tex, frame 8: 'Verdict on the aufbau critique'."""

    TITLE = "Verdict on the aufbau critique"
    SYMBOLS = (r"VO(oep): a vanadyl porphyrin whose unpaired electron is not in the highest occupied orbital — model "
               r"label: a quantum number that is exact only for one electron in a central field")

    def construct(self) -> None:
        self.setup_frame()
        rh = rich("**right**", 32, GREEN).move_to([-3.3, 2.0, 0])
        right = bullets(["one-electron quantum numbers are model labels, Exhibit A",
                         "orbital energies depend on the configuration, Exhibit C",
                         "non-aufbau occupations are observed via measurable properties: VO(oep), quantum dots, LiF "
                         "dissociation, the radicals ahead"], width=6.0, size=27, colour=GREEN)
        rh.move_to([-6.4 + rh.width / 2, 2.0, 0])
        right.next_to(rh, m.DOWN, buff=0.25)
        right.shift(m.RIGHT * (-6.1 - right.get_left()[0]))
        oh = rich("**overstated**", 32, ROSE).move_to([3.4, 2.0, 0])
        over = bullets(["an aufbau-filled *determinant* is fully antisymmetric: within the orbital model it does not "
                        "“violate” Pauli",
                        "“obsolescence” of aufbau and Hund's rule: both remain useful rules of thumb for atomic ground "
                        "states, with known exceptions, e.g. Cr, Cu"], width=6.0, size=27, colour=ROSE)
        oh.move_to([0.4 + oh.width / 2, 2.0, 0])
        over.next_to(oh, m.DOWN, buff=0.25)
        over.shift(m.RIGHT * (0.7 - over.get_left()[0]))
        verdict = pill("overstated").move_to([3.4, -2.2, 0])
        self.say("[The verdict. What the review gets right: one-electron quantum numbers are labels of a model, as "
                 "Exhibit A showed;]", m.AnimationGroup(m.FadeIn(rh), m.FadeIn(right[0])))
        self.say("[orbital energies depend on the configuration, as Exhibit C showed;]", m.FadeIn(right[1]))
        self.say("[and non-aufbau occupations are observed through measurable properties: in the vanadyl porphyrin V O "
                 "o e p, in quantum dots, in the dissociation of lithium fluoride, and in the radicals coming up next.]",
                 m.FadeIn(right[2]))
        self.say("[What is overstated: a determinant filled by aufbau is fully antisymmetric, so within the orbital model "
                 "it does not violate Pauli's principle.]", m.AnimationGroup(m.FadeIn(oh), m.FadeIn(over[0])))
        self.say("[And the obsolescence of aufbau and Hund's rule is too strong: both remain useful rules of thumb for "
                 "atomic ground states, with known exceptions such as chromium and copper.]", m.FadeIn(over[1]))
        self.say("[Overall verdict on the aufbau critique: overstated.]", m.FadeIn(verdict))
        self.wait(0.4)
