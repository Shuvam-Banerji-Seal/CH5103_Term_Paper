"""Chapter 10: spin polarisation, topology rules, Ovchinnikov and Lieb (presentation/sections/12-spinpol.tex)."""
import csv

import numpy as np

import manimgx as m

from ch06_hund import bar_chart
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ROSE, ROOT, Box, Frame, M, boxed, bullets, figure, pill, rich)


def ring_with_arms(attach: tuple[int, int], colours: tuple[str, str], radius: float = 0.75) -> m.VGroup:
    """A benzene ring (vertex k at angle 90 - 60k degrees) with CH2 arms on two vertices, tipped with spin dots."""
    pts = [radius * np.array([np.cos(np.radians(90 - 60 * k)), np.sin(np.radians(90 - 60 * k)), 0]) for k in range(6)]
    ring = m.Polygon(*pts, color=MUTED, stroke_width=4)
    arms, dots = m.VGroup(), m.VGroup()
    for k, col in zip(attach, colours):
        tip = pts[k] * 1.9
        arms.add(m.Line(pts[k], tip, color=MUTED, stroke_width=4))
        dots.add(m.Dot(tip, radius=0.12, color=col))
    return m.VGroup(ring, arms, dots)


class S76DynamicSpinPol(Frame):
    """12-spinpol.tex, frame 1: 'Dynamic spin polarisation'."""

    TITLE = "Dynamic spin polarisation"
    SYMBOLS = (r"spin density $\rho_s=\rho_\uparrow-\rho_\downarrow$ on each atom — ferromagnetic: parallel spins; "
               r"antiferromagnetic: antiparallel — “sites” = atoms; “separated by an odd number of sites” = odd number "
               r"of atoms in between")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"A damped spin wave so formed generates ferromagnetic coupling between the spins separated by an '
                      'odd number of sites, and antiferromagnetic between those separated by an even number of sites, '
                      'thus yielding the topology rules of spin coupling." — p. 443', "claim", width=7.0, size=27)
        claim.move_to([-2.85, 1.25, 0])
        fig = figure("scheme01_dynamic_spin_polarization.png", height=2.9, max_width=4.6).move_to([4.2, 1.25, 0])
        cap = rich("Scheme 1", 22, MUTED).next_to(fig, m.DOWN, buff=0.1)
        items = [r"1. Hückel: the unpaired electron sits in the NBMO, which is **zero on unstarred atoms**",
                 r"2. add on-site repulsion $U$: an ↑ electron pushes ↓ density onto its neighbours",
                 r"3. negative spin density appears between positive ones: **a correlation effect**"]
        lst = m.VGroup(*[rich(t, 28, width=12.4) for t in items]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.18)
        lst.move_to([0, -1.55, 0])
        self.say("[Part eleven: spin polarisation, and the topology rules it produces. The review says: a damped spin "
                 "wave so formed generates ferromagnetic coupling between the spins separated by an odd number of sites, "
                 "and antiferromagnetic between those separated by an even number of sites, thus yielding the topology "
                 "rules of spin coupling.] Ferromagnetic means parallel spins; antiferromagnetic means antiparallel; "
                 "and sites are atoms.", m.AnimationGroup(m.FadeIn(claim), m.FadeIn(fig), m.FadeIn(cap)))
        self.say("[Here is the mechanism in three steps. First, in Hückel theory the unpaired electron sits in the non-"
                 "bonding orbital, which is exactly zero on the unstarred atoms.]", m.FadeIn(lst[0]))
        self.say("[Second, switch on the on-site repulsion U. An up-spin electron on an atom repels down-spin density "
                 "less than up-spin density, so it pushes down-spin density onto its neighbours.]", m.FadeIn(lst[1]))
        self.say("[Third, negative spin density appears on the unstarred atoms, between the positive ones. Hückel theory "
                 "cannot produce it: it is a correlation effect.]", m.FadeIn(lst[2]))
        self.wait(0.4)


class S77Pentadienyl(Frame):
    """12-spinpol.tex, frame 2: 'Measured on the pentadienyl radical'."""

    TITLE = "Measured on the pentadienyl radical"
    SUBTITLE = r"T9: exact Hubbard diagonalisation, 5 sites, 5 electrons, $S_z=\tfrac12$"
    SYMBOLS = (r"pentadienyl: chain of 5 carbons, one unpaired electron — $U/t$: strength of on-site repulsion relative "
               r"to hopping — $S_z=\tfrac12$: three ↑, two ↓ electrons — starred sites 1, 3, 5")

    def construct(self) -> None:
        self.setup_frame()
        with open(ROOT / "presentation" / "data" / "spin_density.csv") as fh:
            rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(fh)]
        stages = [(0.0, MUTED, r"$U=0$, Hückel: unstarred sites exactly $0$"),
                  (1.0, CYAN, r"$U=t$: small negative dips"),
                  (3.0, GOLD, r"$U=3t$: $-0.18$ on sites 2, 4"),
                  (6.0, ROSE, r"$U=6t$: $-0.25$; the “damped spin wave”")]
        charts = []
        for U, col, _ in stages:
            r = next(r for r in rows if r["U"] == U)
            vals = [r[f"s{i}"] for i in range(1, 6)]
            frame, bars, nums = bar_chart(vals, ["1", "2", "3", "4", "5"], [col] * 5, (-0.3, 0.6), width=6.4,
                                          height=4.2, ylabel="spin density $\\rho_s$", fmt="{:+.2f}", label_size=26)
            charts.append(m.VGroup(frame, bars, nums).move_to([-2.7, 0.15, 0]))
        site = rich("site", 24, MUTED).next_to(charts[0], m.DOWN, buff=0.1)
        notes = [rich(t, 30, col, width=5.2).move_to([3.9, 0.9, 0]) for _, col, t in stages]
        total = rich("total is always $1$; positive on starred, negative on unstarred atoms", 28, width=5.2)
        total.move_to([3.9, -0.8, 0])
        self.say("[Test T nine measured this on the pentadienyl radical, a chain of five carbons with one unpaired "
                 "electron, by exact diagonalisation of the Hubbard model: five sites, five electrons, three up and two "
                 "down. At U equal to zero, which is Hückel theory, the spin density is one third on the starred sites "
                 "one, three and five, and exactly zero on sites two and four.]",
                 m.AnimationGroup(m.FadeIn(charts[0]), m.FadeIn(site), m.FadeIn(notes[0])))
        self.say("[At U equal to t, small negative dips appear on the unstarred sites.]",
                 m.AnimationGroup(m.Transform(charts[0], charts[1]), m.Transform(notes[0], notes[1])))
        self.say("[At U equal to three t, they reach minus zero point one eight on sites two and four.]",
                 m.AnimationGroup(m.Transform(charts[0], charts[2]), m.Transform(notes[0], notes[2])))
        self.say("[At six t, minus zero point two five: the damped spin wave of the review.]",
                 m.AnimationGroup(m.Transform(charts[0], charts[3]), m.Transform(notes[0], notes[3])))
        self.say("[At every U the total stays one, positive on the starred atoms and negative on the unstarred ones.]",
                 m.FadeIn(total))
        self.wait(0.4)


class S78BondsToTopology(Frame):
    """12-spinpol.tex, frame 3: 'From bonds to topology'."""

    TITLE = "From bonds to topology"
    SYMBOLS = (r"Néel state: neighbours antiparallel everywhere — meta / para: $m$- / $p$-xylylene, CH₂ groups at ring "
               r"positions 1,3 / 1,4 — a path of an even number of bonds returns to the same set")

    def construct(self) -> None:
        self.setup_frame()
        items = [r"1. strong $U$: each bond carries $J_{\text{AF}}=4t^2/U$ — kinetic exchange, Part IX",
                 r"2. bipartite graph: every bond joins $\mathcal A$ to $\mathcal B$",
                 r"3. lowest energy: $\mathcal A$ spins one way, $\mathcal B$ spins the other — Néel",
                 r"4. same set ⇔ even number of bonds ⇔ odd number of atoms in between"]
        lst = m.VGroup(*[rich(t, 28, width=6.6) for t in items]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.28)
        lst.move_to([-2.95, 0.7, 0])
        rule = rich("**same set: parallel; different sets: antiparallel**", 28, GOLD, width=6.6)
        rule.next_to(lst, m.DOWN, buff=0.35).align_to(lst, m.LEFT)
        meta = ring_with_arms((0, 2), (ROSE, ROSE)).move_to([2.6, 0.75, 0])
        para = ring_with_arms((0, 3), (ROSE, BLUE)).move_to([5.2, 0.6, 0])
        ml = m.VGroup(rich("meta: 3 atoms between", 22, ROSE), rich("parallel, triplet", 22, ROSE))
        pl = m.VGroup(rich("para: 4 atoms between", 22, BLUE), rich("antiparallel, singlet", 22, BLUE))
        base = min(meta.get_bottom()[1], para.get_bottom()[1]) - 0.25  # para's arm points down: label both below it
        for grp, mol in ((ml, meta), (pl, para)):
            grp.arrange(m.DOWN, buff=0.06)
            grp.move_to([mol.get_center()[0], base - grp.height / 2, 0])
        self.say("[How does a coupling on each bond become a rule about topology? First, at strong U each bond carries "
                 "the antiferromagnetic coupling J A F, four t squared over U: kinetic exchange, from Part nine.]",
                 m.FadeIn(lst[0]))
        self.say("[Second, an alternant molecule is a bipartite graph: every bond joins a starred atom to an unstarred "
                 "one.]", m.FadeIn(lst[1]))
        self.say("[Third, the lowest-energy arrangement of the spins puts all starred spins one way and all unstarred "
                 "spins the other, so every bond is antiparallel. This is the Néel arrangement.]", m.FadeIn(lst[2]))
        self.say("[Fourth, two atoms are in the same set exactly when an even number of bonds separates them, which "
                 "means an odd number of atoms in between.]", m.FadeIn(lst[3]))
        self.say("[So: same set, parallel; different sets, antiparallel.] [In meta xylylene the two C H two groups have "
                 "three ring atoms between them, so their spins are parallel and the ground state is a triplet.] [In para "
                 "xylylene there are four atoms between them: antiparallel, a singlet.]",
                 m.FadeIn(rule), m.AnimationGroup(m.FadeIn(meta), m.FadeIn(ml)),
                 m.AnimationGroup(m.FadeIn(para), m.FadeIn(pl)))
        self.wait(0.4)


class S79Ovchinnikov(Frame):
    """12-spinpol.tex, frame 4: 'Ovchinnikov's rule, and Lieb's theorem behind it'."""

    TITLE = "Ovchinnikov's rule, and Lieb's theorem behind it"
    SYMBOLS = (r"$n_A,n_B$: starred / unstarred atom counts — half filling: one $\pi$ electron per carbon — $S=0$ "
               r"singlet, $1$ triplet, $\tfrac32$ quartet — rule = Ovchinnikov count; exact = our diagonalisation")

    def construct(self) -> None:
        self.setup_frame()
        count = rich(r"count the Néel arrangement: $n_A$ up, $n_B$ down", 28).move_to([-3.3, 2.15, 0])
        S = M(r"S=\tfrac12\,|n_A-n_B|", size=44).next_to(count, m.DOWN, buff=0.25)
        ov = rich('Ovchinnikov\'s rule, as the review states it, p. 443: the most spin-alternant determinant "is '
                  'expected to have the lowest energy and the highest contribution"', 26, width=6.4)
        ov.next_to(S, m.DOWN, buff=0.3).align_to(count, m.LEFT)
        lieb = boxed(r"repulsive Hubbard model, bipartite graph, half filling, any $U>0$: unique ground state with "
                     r"$S=\tfrac12\bigl||\mathcal B|-|\mathcal A|\bigr|$", "result", width=6.4, size=26,
                     tag="Lieb, Phys. Rev. Lett. 62, 1201, 1989")
        lieb.next_to(ov, m.DOWN, buff=0.3).align_to(count, m.LEFT)
        tab = M(r"\begin{array}{lccc} \text{T9}\ (U=3t) & n_A/n_B & \text{rule} & \text{exact}\\ \hline "
                r"\text{CBD} & 2/2 & 0 & 0\\ \text{TMM} & 1/3 & 1 & 1\\ \text{TME} & 3/3 & 0 & 0\\ "
                r"\text{MX} & 3/5 & 1 & 1\\ \text{TriMB} & 3/6 & \tfrac32 & \tfrac32\\ \text{TetraMB} & 5/5 & 0 & 0\\ "
                r"p\text{-xylylene} & 4/4 & 0 & 0 \end{array}", size=32).move_to([3.6, 0.75, 0])
        note = rich('TriMB: the review, p. 444, groups it with MX as having "triplet ground states"; three unpaired '
                    'electrons give a *quartet*, $S=\\tfrac32$.', 24, ROSE, width=5.4).next_to(tab, m.DOWN, buff=0.3)
        self.say("[Count the Néel arrangement: n A spins up on the starred atoms and n B down on the unstarred ones. The "
                 "total spin is one half of the difference, n A minus n B.]",
                 m.AnimationGroup(m.FadeIn(count), m.Write(S)))
        self.say("[That is Ovchinnikov's rule. As the review states it, the most spin-alternant determinant is expected "
                 "to have the lowest energy and the highest contribution.]", m.FadeIn(ov))
        self.say("[Behind it stands a theorem, by Lieb, in Physical Review Letters, nineteen eighty nine: for the "
                 "repulsive Hubbard model on a bipartite graph at half filling, with any U greater than zero, the ground "
                 "state is unique and has spin one half of the difference between the sizes of the two sets.]",
                 m.FadeIn(lieb))
        self.say("[Test T nine checked the rule against exact diagonalisation at U equal to three t, for seven "
                 "molecules: cyclobutadiene, T M M, T M E, meta xylylene, trimethylenebenzene, tetramethylenebenzene "
                 "and para xylylene. In every case the exact spin equals the rule's count.]", m.FadeIn(tab))
        self.say("[One correction to the review. On page four hundred and forty four it groups trimethylenebenzene with "
                 "meta xylylene as having triplet ground states. Its three unpaired electrons give a quartet, with spin "
                 "three halves, as both the rule and our calculation say.]", m.FadeIn(note))
        self.wait(0.4)


class S80DisjointWho(Frame):
    """12-spinpol.tex, frame 5: 'Disjoint diradicals: who picks the singlet?'."""

    TITLE = "Disjoint diradicals: who picks the singlet?"
    SYMBOLS = (r"D$_{4h}$: square geometry — first order: energy from the exchange integral alone — second order: energy "
               r"from mixing in excited, spin-polarised configurations, scaling as $U^2$")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"In the singlet state of D$_{4h}$ CBD, the bonding $\\pi$-electrons can partially localize on the '
                      'same pair of atoms as the same-spin unpaired electrons; however, in the triplet state such '
                      'advantageous spin polarization is not possible." — p. 443', "claim", width=6.3, size=27)
        claim.move_to([-3.25, 0.7, 0])
        pts = bullets([r"first order: $2K_{ab}=0$, disjoint",
                       r"second order: spin polarisation of the paired electrons, $\propto U^2$",
                       r"our scaling test: gap $\propto U^{1.97}$ for CBD, $U^{1.95}$ for TME, singlet lower"],
                      width=5.7, size=28).move_to([3.4, 1.0, 0])
        ok = m.VGroup(pill("verified"), rich("consistent with the spin-polarisation mechanism of the review's ref. 9, "
                                             "Kollmar & Staemmler, “Violation of Hund's rule by spin polarization”; not "
                                             "accessed", 24, width=5.7)).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15)
        ok.next_to(pts, m.DOWN, buff=0.4).align_to(pts, m.LEFT)
        self.say("[Back to the question left open in Part ten: for disjoint diradicals, what picks the singlet? The "
                 "review's answer, for square cyclobutadiene: in the singlet state, the bonding pi electrons can partially "
                 "localise on the same pair of atoms as the same-spin unpaired electrons; in the triplet state such "
                 "advantageous spin polarisation is not possible.]", m.FadeIn(claim))
        self.say("[At first order the gap is two K a b, which is zero for disjoint orbitals.]", m.FadeIn(pts[0]))
        self.say("[At second order the paired electrons polarise, mixing in spin-polarised excited configurations, and "
                 "that energy scales as U squared.]", m.FadeIn(pts[1]))
        self.say("[Our scaling test found exactly that: the gap grows as U to the power one point nine seven for "
                 "cyclobutadiene and one point nine five for T M E, with the singlet lower.]", m.FadeIn(pts[2]))
        self.say("[That is consistent with the spin-polarisation mechanism of the review's reference nine, by Kollmar "
                 "and Staemmler, titled Violation of Hund's rule by spin polarization, which we could not access.]",
                 m.FadeIn(ok))
        self.wait(0.4)


class S81Figure4(Frame):
    """12-spinpol.tex, frame 6: 'Topology in the paper: Figure 4'."""

    TITLE = "Topology in the paper: Figure 4"
    SYMBOLS = (r"dots: rose spin up, blue spin down — $p$, $m$: para / meta attachment on each ring — Schlenk, "
               r"Chichibabin: classic hydrocarbon diradicals")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig04_topology_driven_multiplicity.png", height=4.9, max_width=6.9).move_to([-2.9, 0.1, 0])
        claim = boxed('simple polyradicals "can also be thought of as coupling units that sustain certain spin alignment '
                      'depending on topology, as seen in Schlenk\'s and Chichibabin\'s hydrocarbons, or in isomers of '
                      'dinitroxide IV" — p. 444', "claim", width=5.4, size=26).move_to([3.7, 1.0, 0])
        note = rich(r"in Fig. 4, IV with $p,p'$ links: parallel spins; $m,m'$ and $m,p'$: antiparallel. Same atoms, "
                    r"different topology.", 27, width=5.4).next_to(claim, m.DOWN, buff=0.35)
        self.say("[The review's Figure four shows topology at work in real molecules.]", m.FadeIn(fig))
        self.say("[It says that simple polyradicals can also be thought of as coupling units that sustain certain spin "
                 "alignment depending on topology, as seen in Schlenk's and Chichibabin's hydrocarbons, or in isomers of "
                 "dinitroxide four.]", m.FadeIn(claim))
        self.say("[In the figure, dinitroxide four with para, para prime links has parallel spins, while the meta, meta "
                 "prime and meta, para prime isomers have antiparallel spins. The atoms are the same; only the topology "
                 "differs.]", m.FadeIn(note))
        self.wait(0.4)


class S82Tropylidene(Frame):
    """12-spinpol.tex, frame 7: 'Tropylidene: a singlet from spin polarisation (Figure 5)'."""

    TITLE = "Tropylidene: a singlet from spin polarisation, Figure 5"
    SYMBOLS = (r"tropylidene: cycloheptatrienylidene, a carbene in a 7-ring — $2a_2$, $2b_1$, $a_1$: orbital symmetry "
               r"labels, $a_1$ in-plane, the others $\pi$ — $^1A_2$ / $^3A_2$: singlet / triplet states")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig05_tropylidene_orbitals.png", height=4.7, max_width=5.9).move_to([-3.4, 0.1, 0])
        items = [r"1. unpaired electron in the $2a_2$ $\pi$ orbital",
                 r"2. polarises the bonding $\pi$ electrons in $2b_1$",
                 r"3. opposite spin accumulates on the carbenic carbon",
                 r"4. it couples *ferromagnetically* with the electron in the orthogonal $a_1$ orbital on the same atom",
                 r"5. net result: the $^1A_2$ singlet is lower"]
        lst = m.VGroup(*[rich(t, 27, width=6.0) for t in items]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.22)
        lst.move_to([3.3, 0.55, 0])
        summary = rich("**our summary: Hund's rule obeyed locally, violated globally.**", 28, GOLD, width=6.0)
        summary.next_to(lst, m.DOWN, buff=0.35).align_to(lst, m.LEFT)
        self.say("[Spin polarisation can even produce a singlet ground state where Hund's rule would predict a triplet. "
                 "The review's Figure five shows tropylidene, a carbene in a seven-membered ring.] Follow the mechanism "
                 "in five steps.", m.FadeIn(fig))
        self.say("[One: an unpaired electron occupies the two a two pi orbital.]", m.FadeIn(lst[0]))
        self.say("[Two: it polarises the bonding pi electrons in two b one.]", m.FadeIn(lst[1]))
        self.say("[Three: as a result, opposite spin accumulates on the carbenic carbon.]", m.FadeIn(lst[2]))
        self.say("[Four: that opposite spin couples ferromagnetically, following Hund's rule, with the electron in the "
                 "orthogonal in-plane a one orbital on the same atom.]", m.FadeIn(lst[3]))
        self.say("[Five: the net result is that the singlet, one A two, lies lower than the triplet.]", m.FadeIn(lst[4]))
        self.say("[Our summary: Hund's rule is obeyed locally, on the carbenic carbon, and violated globally, for the "
                 "molecule as a whole.]", m.FadeIn(summary))
        self.wait(0.4)


class S83WhereRulesStop(Frame):
    """12-spinpol.tex, frame 8: 'Where the rules stop'."""

    TITLE = "Where the rules stop"
    SYMBOLS = (r"alternant: no odd-membered rings, so atoms split into two sets — $\sigma$–$\pi$ diradical: one unpaired "
               r"electron in an in-plane $\sigma$ orbital, one in a $\pi$ orbital — didehydrotoluene: toluene with two "
               r"H removed")

    def construct(self) -> None:
        self.setup_frame()
        pts = bullets([r"Ovchinnikov / Lieb: *alternant* $\pi$ systems, Hubbard/Heisenberg-type physics",
                       r"pyridinium V, Fig. 6: ionic resonance overturns the topology prediction",
                       r"$\sigma$–$\pi$ diradicals, didehydrotoluenes: ortho, para triplet; *meta* open-shell singlet"],
                      width=6.2, size=28).move_to([-3.1, 0.75, 0])
        claim = boxed('"Crucially, all of these rules are not the direct consequences of quantum mechanics and only '
                      'mimic the dynamic and static correlation effects with the help of simplifying assumptions, thus '
                      'inevitably having limited scope." — p. 443', "claim", width=5.6, size=26).move_to([3.55, 1.0, 0])
        ok = m.VGroup(pill("verified"), rich("fair: the topology rule is a theorem only of the Hubbard model, Lieb; the "
                                             "others are model heuristics", 26, width=5.6))
        ok.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15).next_to(claim, m.DOWN, buff=0.35).align_to(claim, m.LEFT)
        self.say("[Where do these rules stop working? Ovchinnikov's rule and Lieb's theorem cover alternant pi systems, "
                 "where Hubbard or Heisenberg type physics applies.]", m.FadeIn(pts[0]))
        self.say("[The pyridinium molecule five, from Figure six, is an exception: ionic resonance overturns the "
                 "topology prediction.]", m.FadeIn(pts[1]))
        self.say("[And sigma pi diradicals, such as the didehydrotoluenes, break the pattern too: the ortho and para "
                 "isomers are triplets, but the meta isomer is an open-shell singlet.]", m.FadeIn(pts[2]))
        self.say("[The review itself says: crucially, all of these rules are not the direct consequences of quantum "
                 "mechanics and only mimic the dynamic and static correlation effects with the help of simplifying "
                 "assumptions, thus inevitably having limited scope.]", m.FadeIn(claim))
        self.say("[That is fair. The topology rule is a theorem only of the Hubbard model, by Lieb; the others are model "
                 "heuristics.]", m.FadeIn(ok))
        self.wait(0.4)
