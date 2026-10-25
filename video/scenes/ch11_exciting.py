"""Chapter 11: switching spin states, Figures 7-9 (presentation/sections/13-exciting.tex)."""
import numpy as np

import manimgx as m

from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ORANGE, ROSE, Box, Derivation, Frame, Plot, M, axes, boxed, bullets,
                  curve, figure, pill, rich)


class S84Crossover(Frame):
    """13-exciting.tex, frame 1: 'Spin-state crossover by external stimuli (Figure 7)'."""

    TITLE = "Spin-state crossover by external stimuli: Figure 7"
    SYMBOLS = (r"dots in the figure: rose ↑, blue ↓ — $h\nu$: light — TEMPO: a stable nitroxide radical — superexchange: "
               r"coupling of two spins through an intervening atom — $T$: temperature, $B$: magnetic field")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig07_spin_crossover_external_stimuli.png", height=5.0, max_width=4.8).move_to([-4.1, 0.0, 0])
        items = [r"**(a) oxidation**: quinone coupler switches two nitroxides between ferro- and antiferromagnetic coupling",
                 r"**(b) light**: *trans*-azobenzene, antiparallel, singlet → *cis*, which loses planarity: triplet, "
                 r"predicted computationally",
                 r"**(c) light**: *trans*→*cis* alkene brings two TEMPO units close, H-bonded, antiferromagnetic",
                 r"**(d) light**: photo-induced bond formation changes the orbital topology",
                 r"**(e) Zn²⁺**: O–Zn–O superexchange and O⋯O through-space exchange favour antiferromagnetic coupling",
                 r"**(f) $T$ or $B$**: 1,4-phenylenedinitrene, open-shell singlet → triplet"]
        lst = m.VGroup(*[rich(t, 25, width=7.6) for t in items]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.2)
        lst.move_to([2.35, 0.1, 0])
        self.say("[Part twelve: switching spin states. The review's Figure seven collects molecules whose spin state "
                 "can be switched by an external stimulus.]", m.FadeIn(fig))
        self.say("[In panel a, oxidation: a quinone coupler switches two nitroxide radicals between ferromagnetic and "
                 "antiferromagnetic coupling.]", m.FadeIn(lst[0]))
        self.say("[In panel b, light: trans azobenzene couples its spins antiparallel, a singlet; light turns it into the "
                 "cis isomer, which loses planarity and is predicted, computationally, to be a triplet.]",
                 m.FadeIn(lst[1]))
        self.say("[In panel c, light again: a trans to cis switch of an alkene brings two TEMPO units close together, "
                 "hydrogen bonded, and they couple antiferromagnetically.] TEMPO is a stable nitroxide radical.",
                 m.FadeIn(lst[2]))
        self.say("[In panel d, light forms a new bond, and that changes the orbital topology.]", m.FadeIn(lst[3]))
        self.say("[In panel e, zinc ions: coordination creates oxygen zinc oxygen superexchange and through-space "
                 "exchange between the oxygens, which favour antiferromagnetic coupling.] Superexchange is coupling of "
                 "two spins through an atom in between.", m.FadeIn(lst[4]))
        self.say("[And in panel f, temperature or a magnetic field turns one four phenylenedinitrene from an open-shell "
                 "singlet into a triplet.]", m.FadeIn(lst[5]))
        self.wait(0.4)


class S85WordingSlip(Frame):
    """13-exciting.tex, frame 2: 'A wording slip in (e)?'."""

    TITLE = "A wording slip in (e)?"
    SYMBOLS = (r"disjoint / nondisjoint NBMOs: Part X — no shared atoms ⇒ $K\approx0$; shared atoms ⇒ $K>0$, triplet "
               r"favoured")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"Coordination to Zn²⁺ brings about O–Zn–O superexchange and O⋯O through-space exchange, which '
                      'favor antiferromagnetic coupling and override the preference for the triplet ground state, '
                      'predicted on the basis of *disjoint* NBMOs in parent dinitroxide ligand" — p. 445', "claim",
                      width=12.6, size=28).move_to([0, 1.55, 0])
        left = boxed("review, p. 443: **disjoint** NBMOs make the singlet *competitive*; its triplet examples, MX and "
                     "TriMB, are **nondisjoint**", "plain", width=5.9, size=28).move_to([-3.2, -0.45, 0])
        right = boxed('so "disjoint" here probably means "nondisjoint", or the triplet preference has another origin',
                      "plain", width=5.9, size=28).move_to([3.2, -0.45, 0])
        verdict = m.VGroup(pill("inconsistent"), rich("wording vs p. 443; original, ref. 52, not checked", 26, MUTED))
        verdict.arrange(m.RIGHT, buff=0.25).move_to([0, -2.0, 0])
        self.say("[Panel e comes with a sentence worth reading closely. The review says: coordination to zinc brings "
                 "about oxygen zinc oxygen superexchange and through-space exchange between the oxygens, which favour "
                 "antiferromagnetic coupling and override the preference for the triplet ground state, predicted on the "
                 "basis of disjoint N B M Os in the parent dinitroxide ligand.]", m.FadeIn(claim))
        self.say("[But on page four hundred and forty three, the review itself says that disjoint N B M Os make the "
                 "singlet competitive, and its triplet examples, meta xylylene and trimethylenebenzene, are "
                 "nondisjoint.]", m.FadeIn(left))
        self.say("[So disjoint here probably means nondisjoint, or else the triplet preference has some other origin.]",
                 m.FadeIn(right))
        self.say("[We mark it inconsistent with page four hundred and forty three. We did not check the original, "
                 "reference fifty two.]", m.FadeIn(verdict))
        self.wait(0.4)


class S86Temperature(Frame):
    """13-exciting.tex, frame 3: 'Panel (f), quantitatively: temperature'."""

    TITLE = "Panel (f), quantitatively: temperature"
    SUBTITLE = "assume a singlet ground state, triplet $\\Delta$ above; Boltzmann statistics; degeneracies 1 and 3"
    SYMBOLS = (r"$Z$: partition function — $k_B$: Boltzmann constant — $\Delta=E_T-E_S>0$ — degeneracy 3: the triplet's "
               r"$M_S=-1,0,+1$ — $p_T$: fraction of molecules in the triplet")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            ("Z", r"=1+3e^{-\Delta/k_BT}", "Boltzmann weights"),
            ("p_T", r"=\frac{3e^{-\Delta/k_BT}}{1+3e^{-\Delta/k_BT}}", "triplet weight $/Z$"),
            (r"p_T(T\to\infty)", r"\to\tfrac34", r"$e^{0}=1$: $3/(1+3)$"),
        ], size=34, why_size=24).move_to([-3.1, 0.75, 0])
        quote = m.VGroup(rich('"increased temperature … promotes electrons to populate the triplet state" — p. 445', 26,
                              width=5.6), pill("verified")).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15)
        quote.next_to(d, m.DOWN, buff=0.5).align_to(d, m.LEFT)
        ax = Plot([0, 4], [0, 0.8], 4.9, 3.4, xticks=range(0, 5), yticks=[0, 0.2, 0.4, 0.6, 0.8]).move_to([3.7, 0.55, 0])
        xs = np.linspace(0.02, 4, 160)
        pt = curve(ax, xs, 3 * np.exp(-1 / xs) / (1 + 3 * np.exp(-1 / xs)), ROSE)
        lim = m.DashedLine(ax.c2p(0, 0.75), ax.c2p(4, 0.75), color=MUTED, stroke_width=2)
        ll = M(r"\tfrac34", size=26, color=MUTED).next_to(ax.c2p(4, 0.75), m.RIGHT, buff=0.1)
        xl = rich(r"$k_BT/\Delta$", 24, MUTED).next_to(ax.x_axis, m.DOWN, buff=0.42)
        yl = rich(r"$p_T$", 24, MUTED).next_to(ax.y_axis, m.UP, buff=0.12)
        self.say("[Panel f can be made quantitative. Assume a singlet ground state with the triplet an energy delta "
                 "above it, and Boltzmann statistics. The singlet has degeneracy one and the triplet three, one for each "
                 "M S. So the partition function is one plus three e to the minus delta over k B T.]",
                 m.FadeIn(d.rows[0]))
        self.say("[The fraction of molecules in the triplet is its weight over the partition function: three e to the "
                 "minus delta over k B T, divided by one plus three e to the minus delta over k B T.]",
                 m.AnimationGroup(m.FadeIn(d.rows[1]), m.Create(ax), m.FadeIn(xl), m.FadeIn(yl),
                                  m.Create(pt)))
        self.say("[At high temperature the exponential tends to one, so the fraction tends to three over one plus three: "
                 "three quarters.]", m.AnimationGroup(m.FadeIn(d.rows[2]), m.Create(lim), m.FadeIn(ll)))
        self.say("[That agrees with the review: increased temperature promotes electrons to populate the triplet state.]",
                 m.FadeIn(quote))
        self.wait(0.4)


class S87Field(Frame):
    """13-exciting.tex, frame 4: 'Panel (f), quantitatively: magnetic field'."""

    TITLE = "Panel (f), quantitatively: magnetic field"
    SUBTITLE = r"assume a Zeeman term $g\mu_BBM_S$; the singlet is unaffected; $g\approx2$"
    SYMBOLS = (r"$g$: electron $g$-factor, ≈ 2 — $\mu_B$: Bohr magneton — $B$: magnetic field — $M_S$: spin projection "
               r"along $B$ — the singlet has $M_S=0$ only, so it does not shift")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"E_T(M_S)", r"=\Delta+g\mu_BB\,M_S", r"$M_S=0,\pm1$ split apart"),
            (r"E_T(-1)=E_S", r"\ \Leftrightarrow\ B^*=\frac{\Delta}{g\mu_B}", r"$\Delta-g\mu_BB=0$"),
        ], size=34, why_size=24).move_to([-3.1, 1.0, 0])
        quote = m.VGroup(rich('"external magnetic field that splits the triplet into microstates, one of which '
                              'approaches the energy of the ground-state singlet" — p. 445', 26, width=5.8),
                         pill("verified")).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15)
        quote.next_to(d, m.DOWN, buff=0.5).align_to(d, m.LEFT)
        ax = Plot([0, 1.5], [-0.6, 2.6], 4.8, 3.8, xticks=[0, 0.5, 1, 1.5], yticks=[0, 1, 2]).move_to([3.75, 0.35, 0])
        xs = np.linspace(0, 1.5, 2)
        s_line = curve(ax, xs, 0 * xs, BLUE)
        t_lines = m.VGroup(*[curve(ax, xs, 1 + k * xs, ROSE) for k in (1, 0, -1)])
        sl = rich("$S$", 26, BLUE).next_to(ax.c2p(1.5, 0), m.RIGHT, buff=0.1)
        tl = rich("$T$", 26, ROSE).next_to(ax.c2p(1.5, 1), m.RIGHT, buff=0.1)
        cross = m.DashedLine(ax.c2p(1, -0.6), ax.c2p(1, 2.6), color=GOLD, stroke_width=2)
        bl = rich("$B^*$", 24, GOLD).next_to(ax.c2p(1, 2.6), m.UP, buff=0.05)
        xl = rich(r"$g\mu_BB/\Delta$", 24, MUTED).next_to(ax.x_axis, m.DOWN, buff=0.42)
        yl = rich(r"$E/\Delta$", 24, MUTED).next_to(ax.y_axis, m.UP, buff=0.12)
        self.say("[Now a magnetic field. Assume a Zeeman term, g mu B times B times M S, with g about two. The singlet "
                 "has only M S equal to zero, so it does not move. The three triplet components split apart: delta plus "
                 "g mu B B times M S.]",
                 m.AnimationGroup(m.FadeIn(d.rows[0]), m.Create(ax), m.FadeIn(xl), m.FadeIn(yl), m.Create(s_line),
                                  m.Create(t_lines), m.FadeIn(sl), m.FadeIn(tl)))
        self.say("[The M S equal to minus one component reaches the singlet when delta minus g mu B B is zero, at the "
                 "field B star equal to delta over g mu B.]",
                 m.AnimationGroup(m.FadeIn(d.rows[1]), m.Create(cross), m.FadeIn(bl)))
        self.say("[That matches the review: an external magnetic field splits the triplet into microstates, one of which "
                 "approaches the energy of the ground-state singlet.]", m.FadeIn(quote))
        self.wait(0.4)


class S88ClosedOrDiradical(Frame):
    """13-exciting.tex, frame 5: 'Closed shell or diradical? (Figures 8 and 9)'."""

    TITLE = "Closed shell or diradical? Figures 8 and 9"
    SYMBOLS = (r"closed shell: all electrons paired — diradical: two unpaired electrons — biradicaloid: partial diradical "
               r"character — polaron: a charge carrier with its own spin in a polymer")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig08_borderline_triplet_closed_shell.png", height=4.6, max_width=4.4).move_to([-4.3, 0.05, 0])
        pts = bullets([r"**Fig. 8**: 1,3-dinitrophenyls with anionic substituents transfer an electron intramolecularly "
                       r"to give anionic diradicals; triplet is the ground state or only negligibly above the closed "
                       r"shell; cation binding to the nitro group stabilises the diradical",
                       r"**Fig. 9**: protonation, and oxidation, create diradicals: donor–acceptor electron transfer "
                       r"after double protonation, a sapphyrin-derived singlet biradicaloid, a dipyrylium diradical salt, "
                       r"high-spin building blocks for polaronic ferromagnets",
                       r"**singlet fission**: one excited singlet shares its excitation with a neighbour; both end in a "
                       r"low triplet"], width=7.6, size=26).move_to([2.35, 0.1, 0])
        self.say("[Some molecules sit on the border between a closed shell and a diradical.] In Figure eight, one three "
                 "dinitrophenyls with anionic substituents transfer an electron within the molecule to give anionic "
                 "diradicals.", m.FadeIn(fig))
        self.say("[Their triplet is the ground state, or lies only negligibly above the closed shell; and binding a cation "
                 "to the nitro group stabilises the diradical.]", m.FadeIn(pts[0]))
        self.say("[In Figure nine, protonation and oxidation create diradicals: by donor acceptor electron transfer after "
                 "double protonation, in a sapphyrin-derived singlet biradicaloid, in a dipyrylium diradical salt, and in "
                 "high-spin building blocks for polaronic ferromagnets.]", m.FadeIn(pts[1]))
        self.say("[The review also mentions singlet fission: one excited singlet shares its excitation with a neighbour, "
                 "and both end in a low-lying triplet.]", m.FadeIn(pts[2]))
        self.wait(0.4)


class S89Protonation(Frame):
    """13-exciting.tex, frame 6: 'Protonation-induced magnetisation (Figure 9)'."""

    TITLE = "Protonation-induced magnetisation: Figure 9"
    SYMBOLS = (r"arrows: reactions, H⁺ added or removed, electrons transferred — dots: unpaired electrons, coloured by "
               r"spin")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig09_protonation_induced_magnetization.png", height=4.6, max_width=11.5).move_to([0, 0.35, 0])
        note = rich("descriptive part of the review: no mathematics to derive, only claims about specific molecules, not "
                    "re-checked", 26, MUTED, width=12).next_to(fig, m.DOWN, buff=0.25)
        self.say("[Here is Figure nine in full: protonation-induced magnetisation. The arrows are reactions, adding or "
                 "removing protons and transferring electrons, and the dots are unpaired electrons, coloured by spin.]",
                 m.FadeIn(fig))
        self.say("[This part of the review is descriptive. There is no mathematics to derive, only claims about specific "
                 "molecules, which we did not re-check.]", m.FadeIn(note))
        self.wait(0.4)
