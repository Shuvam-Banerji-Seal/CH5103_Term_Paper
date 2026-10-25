"""Chapter 14: quasi-closed-shell (non-aufbau) radicals (presentation/sections/16-quasi.tex)."""
import csv

import numpy as np

import manimgx as m

from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ORANGE, ROSE, ROOT, Box, Derivation, Frame, M, Plot, boxed,
                  bullets, connect, curve, figure, node, pill, rich, table_rows)


class S102SomoBelow(Frame):
    """16-quasi.tex, frame 1: 'SOMO below HOMO (Figure 10)'."""

    TITLE = "SOMO below HOMO: Figure 10"
    SYMBOLS = (r"SOMO: singly occupied MO — HOMO: here the highest *doubly* occupied MO — LUMO: lowest unoccupied MO — "
               r"quasi-closed shell: SOMO below one or more doubly occupied MOs — redox: electron removal, oxidation, or "
               r"addition, reduction")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig10_aufbau_vs_non_aufbau.png", height=4.3, max_width=5.9).move_to([-3.45, 0.2, 0])
        claim = boxed('"upon ionization an electron is removed from the higher energy doubly occupied MO, leaving another '
                      'unpaired electron behind, while upon addition new electron enters the former LUMO; essentially, '
                      'SOMO does not participate in these processes." — p. 449', "claim", width=6.2, size=27)
        claim.move_to([3.45, 0.9, 0])
        fp = rich("the fingerprint is **redox**: products are **polyradicals**, diradicals in the simplest case, not "
                  "closed shells", 28, width=6.1).next_to(claim, m.DOWN, buff=0.35)
        self.say("[Part fifteen: quasi-closed shells, or non-aufbau radicals. In an ordinary radical the singly occupied "
                 "orbital, the SOMO, is the highest occupied orbital. The review's Figure ten shows the alternative: the "
                 "SOMO lies below one or more doubly occupied orbitals.]", m.FadeIn(fig))
        self.say("[The review says: upon ionisation an electron is removed from the higher energy doubly occupied orbital, "
                 "leaving another unpaired electron behind, while upon addition the new electron enters the former LUMO; "
                 "essentially, the SOMO does not participate in these processes.]", m.FadeIn(claim))
        self.say("[So the fingerprint is redox chemistry: oxidation and reduction give polyradicals, diradicals in the "
                 "simplest case, not closed shells.]", m.FadeIn(fp))
        self.wait(0.4)


class S103UHF1(Frame):
    """16-quasi.tex, frame 2: 'UHF orbital energies of s1h2 (1/2)'."""

    TITLE = r"UHF orbital energies of $s^1h^2$, part 1"
    SYMBOLS = (r"$s$: SOMO, $h$: HOMO — $h_s,h_h$: one-electron energies — $J_{hs}=\eri hhss$: Coulomb — "
               r"$K_{hs}=\eri hssh\ge0$: exchange — UHF: unrestricted HF, $\alpha$ and $\beta$ orbitals may differ; frozen and "
               r"equal here — $E(\cdot)$: energy of the $N-1$ electron ion")

    def construct(self) -> None:
        self.setup_frame()
        assume = boxed(r"frozen orbitals; SOMO $s$, $\alpha$ only, doubly occupied $h$; core absorbed into $h_s,h_h$; "
                       r"$\varepsilon_k=E_N-E_{N-1}^{(k)}$, Koopmans", "assume", width=12.6, size=27).move_to([0, 2.0, 0])
        conf = rich(r"configuration: $s\alpha,\ h\alpha,\ h\beta$ — pairs: $(s\alpha,h\alpha)$ same spin, $(s\alpha,h\beta)$, "
                    r"$(h\alpha,h\beta)$", 28).move_to([0, 1.05, 0])
        d = Derivation([
            (r"E_N", r"=h_s+2h_h+\underbrace{(J_{hs}-K_{hs})}_{s\alpha,h\alpha}+\underbrace{J_{hs}}_{s\alpha,h\beta}"
                     r"+\underbrace{J_{hh}}_{h\alpha,h\beta}", "each pair: $J$; same-spin pair: also $-K$"),
            (r"\varepsilon_h^\alpha=E_N-E(s\alpha,h\beta)", r"=h_h+J_{hh}+J_{hs}-K_{hs}", r"$h\alpha$ leaves with its two pairs"),
            (r"\varepsilon_h^\beta=E_N-E(s\alpha,h\alpha)", r"=h_h+J_{hh}+J_{hs}", r"$h\beta$ has no same-spin partner: no $K$"),
        ], size=32, why_size=24).move_to([0, -0.85, 0])
        self.say("[Why should a SOMO ever drop below a HOMO? Derive the orbital energies. Assume frozen orbitals: a SOMO s "
                 "with one alpha electron, a doubly occupied orbital h, the core absorbed into the one-electron energies, "
                 "and each orbital energy defined, as in Koopmans' theorem, as the cost of removing that electron.]",
                 m.FadeIn(assume))
        self.say("[The configuration is s alpha, h alpha, h beta. There are three pairs: s alpha with h alpha, which have "
                 "the same spin; s alpha with h beta; and h alpha with h beta.]", m.FadeIn(conf))
        self.say("[The energy: h s plus two h h, plus, for each pair, a Coulomb integral, and for the same-spin pair also "
                 "minus the exchange integral K h s.]", m.FadeIn(d.rows[0]))
        self.say("[Remove h alpha: it takes its one-electron energy and its two pairs with it. So epsilon h alpha is h h "
                 "plus J h h plus J h s minus K h s.]", m.FadeIn(d.rows[1]))
        self.say("[Remove h beta instead: it has no same-spin partner, so there is no K. Epsilon h beta is h h plus J h h "
                 "plus J h s.]", m.FadeIn(d.rows[2]))
        self.wait(0.4)


class S104UHF2(Frame):
    """16-quasi.tex, frame 3: 'UHF orbital energies of s1h2 (2/2)'."""

    TITLE = r"UHF orbital energies of $s^1h^2$, part 2"
    SYMBOLS = (r"$\varepsilon_k^\sigma$: Koopmans energy of orbital $k$ with spin $\sigma$ — occupied: $E_N-E_{N-1}$; empty: "
               r"$E_{N+1}-E_N$ — $J_{ss}$: repulsion of two electrons in $s$, large, on-site — Scheme 3: donor HOMO split "
               r"by the radical's spin")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\varepsilon_s^\alpha=E_N-E(h\alpha,h\beta)", r"=h_s+2J_{hs}-K_{hs}",
             r"$s\alpha$ leaves: pairs with $h\alpha$, $J-K$, and $h\beta$, $J$"),
            (r"\varepsilon_s^\beta\ (\text{empty; add }s\beta)", r"=h_s+J_{ss}+2J_{hs}-K_{hs}",
             r"$E_{N+1}-E_N$: new pairs with $s\alpha$, $h\alpha$, $h\beta$, same spin"),
        ], size=32, why_size=24).move_to([0, 1.55, 0])
        res = boxed(r"$\varepsilon_h^\beta-\varepsilon_h^\alpha=K_{hs}\ge0$: the donor's $\alpha$ HOMO is pulled down by "
                    r"exchange with the unpaired electron; its $\beta$ HOMO is not", "result", width=6.4, size=28,
                    tag="Scheme 3, derived").move_to([-3.1, -0.65, 0])
        t2 = m.VGroup(pill("verified"), rich("T2: all four checked against determinant energies", 24, MUTED))
        t2.arrange(m.RIGHT, buff=0.2).next_to(res, m.DOWN, buff=0.3).align_to(res, m.LEFT)
        fig = figure("scheme03_donor_HOMO_spin_polarization.png", height=3.0, max_width=4.6).move_to([3.9, -0.75, 0])
        self.say("[Now the SOMO itself. Removing s alpha breaks its pair with h alpha, worth J minus K, and its pair with h "
                 "beta, worth J. So epsilon s alpha is h s plus two J h s minus K h s.]", m.FadeIn(d.rows[0]))
        self.say("[The beta SOMO is empty, so its energy is the cost of adding an electron there. The new electron pairs "
                 "with s alpha, paying the large on-site repulsion J s s, with h alpha, paying J h s, and with h beta, "
                 "which has the same spin, paying J h s minus K h s. So epsilon s beta is h s plus J s s plus two J h s "
                 "minus K h s.]", m.FadeIn(d.rows[1]))
        self.say("[Compare the two HOMO energies: epsilon h beta minus epsilon h alpha is K h s, which is never negative. "
                 "The donor's alpha HOMO is pulled down by exchange with the unpaired electron; its beta HOMO is not. "
                 "This is the review's Scheme three, derived.]", m.AnimationGroup(m.FadeIn(res), m.FadeIn(fig)))
        self.say("[Test T two checked all four energies against energies of explicit determinants.]", m.FadeIn(t2))
        self.wait(0.4)


class S105WhenBelow(Frame):
    """16-quasi.tex, frame 4: 'When does the SOMO drop below the HOMO?'."""

    TITLE = "When does the SOMO drop below the HOMO?"
    SYMBOLS = (r"conversion: SOMO–HOMO conversion, i.e. $\varepsilon_s^\alpha<\varepsilon_h^\alpha$ — $J_{hh}$: "
               r"self-repulsion of the HOMO pair — stable radical: low-lying, well-protected SOMO, e.g. a nitroxide")

    def construct(self) -> None:
        self.setup_frame()
        top = rich(r"compare within the $\alpha$ manifold:", 30).move_to([-4.3, 2.1, 0])
        d = Derivation([
            (r"\varepsilon_s^\alpha<\varepsilon_h^\alpha", r"\iff h_s+2J_{hs}-K_{hs}<h_h+J_{hh}+J_{hs}-K_{hs}",
             r"insert the two $\alpha$ energies"),
            ("", r"\iff h_s+J_{hs}<h_h+J_{hh}", r"cancel $-K_{hs}$ and one $J_{hs}$"),
        ], size=36, why_size=24).move_to([0, 1.15, 0])
        cancelled = M(r"\iff h_s+2J_{hs}\cancel{-K_{hs}}<h_h+J_{hh}+J_{hs}\cancel{-K_{hs}}", size=36)
        cancelled.move_to(d.rows[0][1], aligned_edge=m.LEFT)
        read = rich("radical orbital: its energy plus repulsion with *one* $h$ electron, vs. $h$'s energy plus its "
                    "*self*-repulsion", 28, width=12.4).move_to([0, -0.05, 0])
        fav = boxed("**favours conversion**: a stable radical, low $h_s$, beside an electron-rich, e.g. anionic, "
                    "fragment, high $h_h$", "plain", width=5.9, size=27).move_to([-3.2, -1.55, 0])
        claim = boxed('"spatially separated stable radical center and molecular fragment serving as a source of '
                      'high-energy doubly occupied orbitals" — p. 454', "claim", width=5.9, size=27).move_to([3.2, -1.55, 0])
        self.say("[When does the SOMO drop below the HOMO? Compare the two alpha energies. Epsilon s alpha is below epsilon "
                 "h alpha exactly when h s plus two J h s minus K h s is less than h h plus J h h plus J h s minus K h s.]",
                 m.AnimationGroup(m.FadeIn(top), m.FadeIn(d.rows[0])))
        self.say("[The exchange terms cancel,] [and so does one J h s: the condition is h s plus J h s less than h h plus J "
                 "h h.]", m.Transform(d.rows[0][1], cancelled), m.FadeIn(d.rows[1]))
        self.say("[Read it: on the left, the radical orbital's energy plus its repulsion with one h electron; on the "
                 "right, h's own energy plus its self-repulsion.]", m.FadeIn(read))
        self.say("[So conversion is favoured by a stable radical with a low h s, next to an electron-rich fragment, for "
                 "example an anionic one, with a high h h.]", m.FadeIn(fav))
        self.say("[Exactly the review's recipe: a spatially separated stable radical centre and a molecular fragment "
                 "serving as a source of high-energy doubly occupied orbitals.]", m.FadeIn(claim))
        self.wait(0.4)


class S106Redox(Frame):
    """16-quasi.tex, frame 5: 'The redox fingerprint, derived'."""

    TITLE = "The redox fingerprint, derived"
    SYMBOLS = (r"Koopmans: the electron leaves from, or enters, the orbital with the cheapest $\pm\varepsilon$ — $l$: former "
               r"LUMO — $2K_{sh}$: the singlet–triplet gap of Part V — nondegenerate SOMOs: the two singly occupied "
               r"orbitals differ in energy")

    def construct(self) -> None:
        self.setup_frame()
        oh = rich("**oxidation**", 32, GOLD)
        ox = bullets([r"Koopmans: $\mathrm{IP}(h)=-\varepsilon_h<\mathrm{IP}(s)$", r"product $s^1h^1$: a diradical",
                      r"its states: $E_{\OSS}-E_T=2K_{sh}>0$",
                      r"**triplet** cation diradicals with nondegenerate SOMOs, as observed"], width=6.0, size=28)
        left = m.VGroup(oh, ox).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.25).move_to([-3.3, 0.45, 0])
        rh = rich("**reduction**", 32, GOLD)
        red = bullets([r"into $s\beta$ at $\varepsilon_s^\beta$, or into $l$ at $\varepsilon_l$",
                       r"at frozen orbitals: diradical $s^1h^2l^1$ iff $\varepsilon_l<h_s+J_{ss}+2J_{hs}-K_{hs}$",
                       r"**a separate condition**: SOMO–HOMO conversion alone does not imply it"], width=6.0, size=28)
        right = m.VGroup(rh, red).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.25).move_to([3.3, 0.55, 0])
        note = rich("the large on-site $J_{ss}$ is what pushes $\\varepsilon_s^\\beta$ up", 26, MUTED).move_to([3.3, -2.2, 0])
        self.say("[Now derive the redox fingerprint. Oxidation first: by Koopmans' theorem the electron leaves from the "
                 "orbital with the smallest ionisation potential, which is h, since minus epsilon h is less than the "
                 "SOMO's.]", m.AnimationGroup(m.FadeIn(oh), m.FadeIn(ox[0])))
        self.say("[The product, s one h one, is a diradical.]", m.FadeIn(ox[1]))
        self.say("[Its states are those of Part five: the open-shell singlet lies two K s h above the triplet.]",
                 m.FadeIn(ox[2]))
        self.say("[So oxidation gives triplet cation diradicals with nondegenerate SOMOs, as observed.]", m.FadeIn(ox[3]))
        self.say("[Reduction: the new electron goes either into s beta, at epsilon s beta, or into the former LUMO l, at "
                 "epsilon l.]", m.AnimationGroup(m.FadeIn(rh), m.FadeIn(red[0])))
        self.say("[At frozen orbitals, the product is the diradical s one h two l one if and only if epsilon l is below h s "
                 "plus J s s plus two J h s minus K h s.]", m.FadeIn(red[1]))
        self.say("[That is a separate condition: SOMO HOMO conversion on its own does not imply it.]", m.FadeIn(red[2]))
        self.say("[What makes it possible is the large on-site repulsion J s s, which pushes epsilon s beta up.]",
                 m.FadeIn(note))
        self.wait(0.4)


class S107ROHF(Frame):
    """16-quasi.tex, frame 6: 'ROHF: are these orbital energies even real?'."""

    TITLE = "ROHF: are these orbital energies even real?"
    SYMBOLS = (r"ROHF: restricted open-shell HF, one set of spatial orbitals — $\mathbf D^\sigma$: spin-$\sigma$ density "
               r"matrix — $\mathbf F^\sigma=\partial E/\partial\mathbf D^\sigma$: Fock matrix — $\kappa$: small rotation angle "
               r"— canonicalisation: the choice of matrix whose eigenvectors define the orbitals")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"erroneous non-aufbau occupations can be observed with restricted open-shell methods depending on '
                      'the canonicalization parameters of the $\\alpha$ and $\\beta$ electrons in Fock matrix" — p. 449',
                      "claim", width=12.6, size=28).move_to([0, 1.85, 0])
        spaces = rich(r"spaces: core $c$, doubly; open $o$, $\alpha$; virtual $v$ — $\mathbf D^\alpha=\mathbf D_c+\mathbf D_o$, "
                      r"$\mathbf D^\beta=\mathbf D_c$", 29).move_to([0, 0.7, 0])
        dE = M(r"\delta E=\operatorname{tr}(\mathbf F^\alpha\delta\mathbf D^\alpha)+\operatorname{tr}(\mathbf F^\beta\delta"
               r"\mathbf D^\beta),\qquad \text{rotation }p\leftrightarrow q:\ \delta\mathbf D^\sigma=\kappa(\ket p\bra q+\ket q"
               r"\bra p)", size=36).move_to([0, -0.45, 0])
        note = rich("a rotation changes $\\mathbf D^\\sigma$ only if exactly one of $p,q$ is occupied in spin $\\sigma$", 28,
                    MUTED).move_to([0, -1.5, 0])
        self.say("[Before trusting these orbital energies, a warning from the review: erroneous non-aufbau occupations "
                 "can be observed with restricted open-shell methods, depending on the canonicalisation parameters of the "
                 "alpha and beta electrons in the Fock matrix.] Let us see why.", m.FadeIn(claim))
        self.say("[In restricted open-shell Hartree Fock there are three spaces: the doubly occupied core c, the open "
                 "shell o, occupied by alpha electrons only, and the virtuals v. The alpha density covers core and open "
                 "shell; the beta density covers the core.]", m.FadeIn(spaces))
        self.say("[A small change of the densities changes the energy by the trace of each Fock matrix times the change "
                 "of its density. Rotating orbitals p and q into each other by a small angle kappa changes a density by "
                 "kappa times the symmetric combination of p and q.]", m.Write(dE))
        self.say("[But a rotation changes a spin density only if exactly one of p and q is occupied in that spin. Two "
                 "occupied orbitals, or two empty ones, can be mixed without changing anything.]", m.FadeIn(note))
        self.wait(0.4)


class S108Stationarity(Frame):
    """16-quasi.tex, frame 7: 'ROHF stationarity, rotation by rotation'."""

    TITLE = "ROHF stationarity, rotation by rotation"
    SYMBOLS = (r"$F^\sigma_{pq}$: Fock element between spaces $p,q$ — $\delta E\equiv0$: the energy is blind to that rotation "
               r"— $A$: any real weight")

    def construct(self) -> None:
        self.setup_frame()
        rows = [r"c\leftrightarrow o & \text{no, both }\alpha\text{-occ.} & \text{yes} & F^\beta_{co}=0",
                r"o\leftrightarrow v & \text{yes} & \text{no, both }\beta\text{-empty} & F^\alpha_{ov}=0",
                r"c\leftrightarrow v & \text{yes} & \text{yes} & F^\alpha_{cv}+F^\beta_{cv}=0",
                r"\text{within }c,\ o\text{ or }v & \text{no} & \text{no} & \text{none: }\delta E\equiv0"]
        full = M(r"\begin{array}{llll}\text{rotation} & \text{changes }\mathbf D^\alpha? & \text{changes }\mathbf D^\beta? & "
                 r"\text{condition}\\ \hline " + r"\\ ".join(rows) + r"\end{array}", size=32).move_to([0, 1.05, 0])
        bands = table_rows(full, 5)  # header (with its rule) and four rotation rows
        res = boxed(r"diagonal blocks are *arbitrary*: any $A\mathbf F^\alpha+(1-A)\mathbf F^\beta$ gives the same energy "
                    r"and density, but different orbital energies", "result", width=12.0, size=28).move_to([0, -1.35, 0])
        t11a = m.VGroup(pill("verified"), rich("T11a: required blocks $<10^{-7}$, others ~0.1, for H₂NO, NO₂, CH₃, allyl; "
                                               "PySCF's Roothaan Fock uses exactly these off-diagonal blocks", 24, MUTED,
                                               width=10.4)).arrange(m.RIGHT, buff=0.2).move_to([0, -2.45, 0])
        self.say("[Go through the rotations one by one, asking for each whether it changes the alpha density, the beta "
                 "density, and so what stationarity requires.]", m.FadeIn(bands[0]))
        self.say("[Core with open shell: both are alpha-occupied, so the alpha density does not change, but the beta "
                 "density does. Stationarity requires the beta Fock element between core and open shell to vanish.]",
                 m.FadeIn(bands[1]))
        self.say("[Open shell with virtual: the alpha density changes, the beta density does not, since both are "
                 "beta-empty. So the alpha Fock element between open and virtual must vanish.]", m.FadeIn(bands[2]))
        self.say("[Core with virtual: both densities change, so the sum of the alpha and beta elements must vanish.]",
                 m.FadeIn(bands[3]))
        self.say("[And rotations within the core, within the open shell, or within the virtuals change nothing at all: "
                 "the energy is blind to them, and there is no condition.]", m.FadeIn(bands[4]))
        self.say("[So the diagonal blocks of the Fock matrix are arbitrary. Any weighted combination, A times the alpha "
                 "Fock matrix plus one minus A times the beta one, gives the same energy and the same density, but "
                 "different orbital energies.]", m.FadeIn(res))
        self.say("[Test T eleven a confirmed it for H two N O, N O two, methyl and allyl: the required blocks are below "
                 "ten to the minus seven, while the others are about zero point one. PySCF's Roothaan Fock matrix uses "
                 "exactly these off-diagonal blocks.]", m.FadeIn(t11a))
        self.wait(0.4)


class S109HowArbitrary(Frame):
    """16-quasi.tex, frame 8: 'How arbitrary? H2NO, ROHF/6-31G*'."""

    TITLE = "How arbitrary? H₂NO, ROHF/6-31G∗"
    SYMBOLS = (r"H₂NO: aminoxyl, the smallest nitroxide — $\mathbf R_{oo}$: open–open block of the ROHF effective Fock "
               r"matrix — $A^*$: weight where SOMO and HOMO cross — $E_{\mathrm h}$: hartree")

    def construct(self) -> None:
        self.setup_frame()
        ax = Plot([-0.2, 1.4], [-0.62, 0.32], 6.0, 4.0, xticks=[-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4],
                  yticks=[-0.6, -0.4, -0.2, 0, 0.2], yfmt="{:.1f}").move_to([-2.75, 0.3, 0])
        xl = rich(r"weight $A$ in $\mathbf R_{oo}=A\mathbf F^\alpha+(1-A)\mathbf F^\beta$", 24, MUTED)
        xl.next_to(ax.x_axis, m.DOWN, buff=0.45)
        yl = rich(r"$\varepsilon$, $E_{\mathrm h}$", 24, MUTED).next_to(ax.y_axis, m.UP, buff=0.12)
        xs = np.array([-0.2, 1.4])
        homo = curve(ax, xs, [-0.4666, -0.4666], GOLD)
        slope = -0.4397 - 0.2028
        xs_s = np.array([(0.32 - 0.2028) / slope, (-0.62 - 0.2028) / slope])  # clipped to the plot's y range
        somo = curve(ax, xs_s, 0.2028 + slope * xs_s, CYAN)
        hl = rich("HOMO, closed", 24, GOLD).next_to(ax.c2p(-0.18, -0.4666), m.DOWN + m.RIGHT, buff=0.06)
        sl = rich("SOMO", 24, CYAN).move_to(ax.c2p(0.42, 0.10))
        A = (0.2028 + 0.4666) / (0.2028 + 0.4397)
        cross = m.VGroup(m.Dot(ax.c2p(A, -0.4666), radius=0.07, color=ROSE),
                         m.DashedLine(ax.c2p(A, -0.62), ax.c2p(A, 0.32), color=ROSE, stroke_width=2),
                         rich(r"$A^*\approx1.04$", 24, ROSE).next_to(ax.c2p(A, -0.3), m.RIGHT, buff=0.08))
        shade = m.Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 0.32)[1] - ax.c2p(0, -0.62)[1],
                            stroke_width=0, fill_color=MUTED, fill_opacity=0.15)
        shade.move_to((ax.c2p(0, -0.62) + ax.c2p(1, 0.32)) / 2)
        pts = bullets([r"energy identical for every $A$: $-130.369709\,E_{\mathrm h}$",
                       r"SOMO crosses the HOMO at $A^*\approx1.04$",
                       r"shaded: the “natural” range $0\le A\le1$, no crossing here"], width=5.3, size=27)
        pts.move_to([3.85, 0.85, 0])
        verdict = m.VGroup(pill("partial"), rich("the review is right in principle; for ordinary radicals the standard "
                                                 "choices do not flip", 25, width=4.6))
        verdict.arrange(m.RIGHT, buff=0.2, aligned_edge=m.UP).next_to(pts, m.DOWN, buff=0.4).align_to(pts, m.LEFT)
        self.say("[How arbitrary is it in practice? We took H two N O, the smallest nitroxide, with restricted open-shell "
                 "Hartree Fock in the six thirty one G star basis, and varied the weight A in the open-open block of the "
                 "effective Fock matrix. The energy is identical for every A: minus one hundred and thirty point three "
                 "six nine seven zero nine hartree.]",
                 m.AnimationGroup(m.Create(ax), m.FadeIn(xl), m.FadeIn(yl), m.FadeIn(pts[0])))
        self.say("[The HOMO, a closed-shell orbital, stays put at minus zero point four six six seven. But the SOMO energy "
                 "moves linearly with A, from plus zero point two at A equal to zero to minus zero point four four at A "
                 "equal to one.]", m.AnimationGroup(m.Create(homo), m.Create(somo), m.FadeIn(hl), m.FadeIn(sl)))
        self.say("[The SOMO crosses the HOMO at A star, about one point zero four.]",
                 m.AnimationGroup(m.FadeIn(cross), m.FadeIn(pts[1])))
        self.say("[The natural range of weights, from zero to one, is shaded: there is no crossing inside it.]",
                 m.AnimationGroup(m.FadeIn(shade), m.FadeIn(pts[2])))
        self.say("[So the review is right in principle, but for ordinary radicals the standard choices do not flip the "
                 "order. We mark it partial.]", m.FadeIn(verdict))
        self.wait(0.4)


class S110TrustObservables(Frame):
    """16-quasi.tex, frame 9: 'Hence: trust observables'."""

    TITLE = "Hence: trust observables"
    SYMBOLS = (r"a posteriori: after the fact, from measured or computed total energies — invariant: the same for every "
               r"canonicalisation — electron affinity: energy released on adding an electron")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"a rigorous support for the non-aufbau occupation can be obtained a posteriori from the ionization '
                      'potentials and electron affinities (or redox potentials in solution) … as well as from the '
                      'determination of the spin state and magnetic properties of the corresponding open-shell '
                      'oxidation/reduction products." — p. 449', "claim", width=12.6, size=28).move_to([0, 1.5, 0])
        orb = node("orbital ordering\nconvention-dependent", ROSE, width=3.6, height=1.1, size=26).move_to([-3.0, -0.75, 0])
        obs = node("$E$(diradical) vs\n$E$(closed shell)\ninvariant", GREEN, width=3.6, height=1.4, size=26)
        obs.move_to([3.0, -0.75, 0])
        arr = connect(orb, obs)
        al = rich("replace by", 24, MUTED).next_to(arr, m.UP, buff=0.08)
        ahead = rich("this is exactly the test we ran on a distonic radical anion, a few slides ahead", 27)
        ahead.move_to([0, -2.3, 0])
        self.say("[Hence the review's advice, which we endorse: a rigorous support for the non-aufbau occupation can be "
                 "obtained after the fact from the ionisation potentials and electron affinities, or redox potentials in "
                 "solution, as well as from the spin state and magnetic properties of the open-shell oxidation and "
                 "reduction products.]", m.FadeIn(claim))
        self.say("[In other words, stop arguing about orbital ordering, which depends on a convention,] [and compare the "
                 "total energies of the diradical and the closed shell, which do not.]", m.FadeIn(orb),
                 m.AnimationGroup(m.GrowArrow(arr), m.FadeIn(al), m.FadeIn(obs)))
        self.say("[That is exactly the test we ran on a distonic radical anion, a few slides ahead.]", m.FadeIn(ahead))
        self.wait(0.4)


class S111Inorganic(Frame):
    """16-quasi.tex, frame 10: 'Inorganic precedents (Scheme 2)'."""

    TITLE = "Inorganic precedents: Scheme 2"
    SYMBOLS = (r"VO(oep): vanadyl octaethylporphyrin — the unpaired electron sits in a vanadium d orbital, below the "
               r"porphyrin's highest filled $\pi$ orbital — oep: octaethylporphyrin")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("scheme02_VO_oep.png", height=3.8, max_width=4.2).move_to([-4.1, 0.4, 0])
        cap = rich("VO(oep)", 24, MUTED).next_to(fig, m.DOWN, buff=0.12)
        pts = bullets(["unpaired electron localised on **vanadium**",
                       "one-electron *oxidation* uses an occupied **porphyrin** orbital",
                       "one-electron *reduction* uses an unoccupied **porphyrin** orbital"], width=7.4, size=30)
        pts.move_to([2.4, 0.75, 0])
        also = rich("also reported: quantum dots, the LiF dissociation curve", 28, MUTED).move_to([2.4, -1.2, 0])
        self.say("[Non-aufbau radicals were known first in inorganic chemistry. The review's Scheme two shows the vanadyl "
                 "porphyrin V O o e p. Its unpaired electron is localised on vanadium.]",
                 m.AnimationGroup(m.FadeIn(fig), m.FadeIn(cap), m.FadeIn(pts[0])))
        self.say("[Yet one-electron oxidation removes an electron from an occupied porphyrin orbital,]", m.FadeIn(pts[1]))
        self.say("[and one-electron reduction puts it into an unoccupied porphyrin orbital. The vanadium electron takes "
                 "part in neither.]", m.FadeIn(pts[2]))
        self.say("[The same behaviour has been reported in quantum dots and along the dissociation curve of lithium "
                 "fluoride.]", m.FadeIn(also))
        self.wait(0.4)


class S112TempoPt(Frame):
    """16-quasi.tex, frame 11: 'A TEMPO-dithiolate on platinum (Figure 11)'."""

    TITLE = "A TEMPO-dithiolate on platinum: Figure 11"
    SYMBOLS = (r"tempodt: TEMPO-substituted dithiolate ligand — tBubpy: di-*tert*-butyl-bipyridine — NHOMO: next-highest "
               r"occupied MO — CV: cyclic voltammetry — ESR: electron spin resonance")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig11_tempo_dithiolate_non_aufbau.png", height=4.6, max_width=6.6).move_to([-3.1, 0.15, 0])
        pts = bullets(["oxidation of (tempodt)Pt(tBubpy) removes an electron from the **dithiolate HOMO**",
                       "evidence: UV–Vis, ESR, CV, DFT and the dimerisation product",
                       "free tempodt is a normal radical; the conversion comes from an antibonding interaction of its "
                       "NHOMO with the HOMO of Pt(tBubpy)²⁺",
                       "(b) a ditempo metalladithiolene: oxidation-generated biradicals couple to a bicyclic product"],
                      width=5.6, size=26).move_to([3.65, 0.2, 0])
        self.say("[An organometallic example, the review's Figure eleven: a TEMPO dithiolate ligand on platinum. Oxidising "
                 "the complex removes an electron from the dithiolate HOMO, not from the TEMPO SOMO.]",
                 m.AnimationGroup(m.FadeIn(fig), m.FadeIn(pts[0])))
        self.say("[The evidence: U V visible spectra, electron spin resonance, cyclic voltammetry, density functional "
                 "calculations, and the product of dimerisation.]", m.FadeIn(pts[1]))
        self.say("[The free ligand is a normal radical. The conversion comes from an antibonding interaction of its next-"
                 "highest occupied orbital with the HOMO of the platinum bipyridine fragment, which pushes it above the "
                 "SOMO.]", m.FadeIn(pts[2]))
        self.say("[In panel b, a ditempo metalladithiolene: oxidation generates biradicals that couple to give a bicyclic "
                 "product.]", m.FadeIn(pts[3]))
        self.wait(0.4)


class S113Donors(Frame):
    """16-quasi.tex, frame 12: 'Spin-polarised donors (Figures 12, 13)'."""

    TITLE = "Spin-polarised donors: Figures 12 and 13"
    SYMBOLS = (r"NN: nitronyl nitroxide radical — TTF: tetrathiafulvalene — BQ: benzoquinone — donor: electron-rich group "
               r"that is oxidised first — disjoint: no shared atoms, Part X")

    def construct(self) -> None:
        self.setup_frame()
        f12 = figure("fig12_nitronyl_nitroxide_donors.png", height=3.3, max_width=5.2).move_to([-3.75, 0.85, 0])
        t12 = rich("nitronyl nitroxide, NN, radicals on TTF, BQ, amine donors: one-electron oxidation gives **triplet "
                   "cation diradicals**", 26, width=5.4).next_to(f12, m.DOWN, buff=0.2)
        f13 = figure("fig13_disjoint_nondisjoint_orbital_conversion.png", height=3.1, max_width=6.4).move_to([3.3, 0.95, 0])
        t13 = rich("**NNN**, 1-pyrrolyl: donor HOMO disjoint from SOMO/NHOMO. **βNN**, 3-pyrrolyl: donor HOMO and NHOMO "
                   "nondisjoint; their combination rises above the SOMO.", 26, width=6.4).next_to(f13, m.DOWN, buff=0.2)
        self.say("[Figure twelve: nitronyl nitroxide radicals attached to donors such as tetrathiafulvalene, benzoquinone "
                 "and amines. One-electron oxidation gives triplet cation diradicals, the fingerprint we derived.]",
                 m.AnimationGroup(m.FadeIn(f12), m.FadeIn(t12)))
        self.say("[Figure thirteen links the effect to disjointness, from Part ten.]", m.FadeIn(f13))
        self.say("[With a one-pyrrolyl link, the donor HOMO is disjoint from the SOMO and the next orbital. With a three-"
                 "pyrrolyl link, the donor HOMO and the next-highest orbital are nondisjoint, and their combination rises "
                 "above the SOMO.]", m.FadeIn(t13))
        self.wait(0.4)


class S114ConductingMagnets(Frame):
    """16-quasi.tex, frame 13: 'Conducting magnets (Scheme 4, Figure 14, Scheme 5)'."""

    TITLE = "Conducting magnets: Scheme 4, Figure 14, Scheme 5"
    SYMBOLS = (r"itinerant: free to move through the crystal, carries current — localised spin: stays on the radical, "
               r"carries magnetism — magnetoresistance: resistance that changes with magnetic field — ETBN, ESBN: "
               r"radical-substituted TTF-type donors")

    def construct(self) -> None:
        self.setup_frame()
        s4 = figure("scheme04_conductivity_magnetism.png", height=2.3, max_width=5.4).move_to([-3.6, 1.15, 0])
        s5 = figure("scheme05_conducting_magnets_ETBN_ESBN.png", height=2.2, max_width=5.0).move_to([-3.6, -1.35, 0])
        f14 = figure("fig14_oxidation_induced_ferromagnetic_coupling.png", height=2.2, max_width=5.0).move_to([-3.6, -1.35, 0])
        pts = bullets(["two nondegenerate SOMOs: the donor's, higher, carries an itinerant electron, the radical's, lower, "
                       "a localised spin",
                       "ETBN, ESBN perchlorate salts: “first genuine paramagnetic conductors”",
                       "neutral crystals: negative magnetoresistance; field-effect transistors",
                       "Fig. 14: several radicals on one donor; oxidation gives a strongly ferromagnetic high-spin system"],
                      width=6.2, size=26).move_to([3.25, 0.2, 0])
        self.say("[The same orbital pattern gives conducting magnets, Scheme four. After oxidation there are two "
                 "nondegenerate SOMOs: the donor's, higher, carries an itinerant electron that can conduct, and the "
                 "radical's, lower, carries a localised spin that gives magnetism.]",
                 m.AnimationGroup(m.FadeIn(s4), m.FadeIn(pts[0])))
        self.say("[Scheme five: the perchlorate salts of E T B N and E S B N, described as the first genuine paramagnetic "
                 "conductors.]", m.AnimationGroup(m.FadeIn(s5), m.FadeIn(pts[1])))
        self.say("[Their neutral crystals show negative magnetoresistance and have been used in field-effect "
                 "transistors.]", m.FadeIn(pts[2]))
        self.say("[And Figure fourteen: several radicals on one donor; oxidation gives a strongly ferromagnetic, high-spin "
                 "system.]", m.AnimationGroup(m.FadeOut(s5), m.FadeIn(f14), m.FadeIn(pts[3])))
        self.wait(0.4)


class S115PhSensor(Frame):
    """16-quasi.tex, frame 14: 'Other radicals, and a pH sensor (Figure 15)'."""

    TITLE = "Other radicals, and a pH sensor: Figure 15"
    SYMBOLS = (r"phenol: Ar–OH; deprotonated, the phenolate is a strong donor — oxoverdazyl: a stable nitrogen-rich radical "
               r"— high spin: parallel unpaired electrons")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig15_donors_other_radicals.png", height=4.9, max_width=4.6).move_to([-4.0, 0.05, 0])
        pts = bullets([r"**(a)** NN with a phenol-based donor: deprotonation and protonation switch between *triplet* and "
                       r"*closed-shell singlet*: a pH sensor",
                       r"**(b)** anthracene–$p$-phenylene–oxoverdazyl, AnOV: high-spin oxidation products"],
                      width=7.2, size=29).move_to([2.45, 0.4, 0])
        self.say("[Figure fifteen extends the idea to other radicals. In panel a, a nitronyl nitroxide carries a phenol-"
                 "based donor. Removing or adding a proton switches the oxidised molecule between a triplet and a closed-"
                 "shell singlet: a pH sensor.]", m.AnimationGroup(m.FadeIn(fig), m.FadeIn(pts[0])))
        self.say("[In panel b, an anthracene, para phenylene, oxoverdazyl molecule gives high-spin oxidation products.]",
                 m.FadeIn(pts[1]))
        self.wait(0.4)


class S116Distonic(Frame):
    """16-quasi.tex, frame 15: 'Distonic radical anions (Figure 16)'."""

    TITLE = "Distonic radical anions: Figure 16"
    SYMBOLS = (r"distonic: charge and radical on different atoms — not $\pi$-conjugated: no shared $\pi$ system between them "
               r"— zwitterion: closed shell carrying + and − charges")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig16_distonic_radical_anions.png", height=5.0, max_width=4.4).move_to([-4.15, 0.0, 0])
        claim = boxed('a stabilised radical plus an anionic group not $\\pi$-conjugated to it: the anion\'s HOMO lies above '
                      'the SOMO; "if the anion is protonated, the aufbau orbital occupation is restored", switchable "via '
                      'changing pH"; on oxidation it "has been shown computationally to yield diradical species '
                      'preferentially over the closed-shell zwitterion" — p. 452–453', "claim", width=7.6, size=27)
        claim.move_to([2.35, 0.75, 0])
        test = rich("**testable**, and so far computational: compute both oxidised states, with and without the proton", 28,
                    width=7.5).next_to(claim, m.DOWN, buff=0.35)
        self.say("[Figure sixteen shows distonic radical anions: the charge and the radical sit on different atoms.]",
                 m.FadeIn(fig))
        self.say("[The review's claim: a stabilised radical plus an anionic group not conjugated to it; the anion's HOMO "
                 "lies above the SOMO; if the anion is protonated, the aufbau occupation is restored, so it can be "
                 "switched by changing the pH; and on oxidation it has been shown computationally to give diradicals in "
                 "preference to the closed-shell zwitterion.]", m.FadeIn(claim))
        self.say("[That is testable, and so far only computational. So we computed both oxidised states, with and "
                 "without the proton.]", m.FadeIn(test))
        self.wait(0.4)


class S117OurTest(Frame):
    """16-quasi.tex, frame 16: 'Our test: two radicals, two protonation states, two functionals'."""

    TITLE = "Our test: two radicals, two protonation states, two functionals"
    SUBTITLE = "T11/T11c: UB3LYP/6-31G∗ geometries, vertical oxidation at 6-31+G∗"
    SYMBOLS = (r"$E_T$: oxidised diradical, triplet — $E_{\text{CS}}$: oxidised closed shell — vertical: same geometry as the "
               r"radical — + in 6-31+G∗: diffuse functions for anions — CAM-B3LYP: range-separated, more HF exchange at "
               r"long range")

    def construct(self) -> None:
        self.setup_frame()
        with open(ROOT / "presentation" / "data" / "distonic.csv") as fh:
            rows = list(csv.DictReader(fh))
        ax = Plot([0.4, 4.6], [-0.6, 1.6], 6.6, 4.0, yticks=[-0.5, 0, 0.5, 1, 1.5], grid=False).move_to([-2.6, 0.2, 0])
        zero = m.Line(ax.c2p(0.4, 0), ax.c2p(4.6, 0), color=FG, stroke_width=2)
        yl = rich(r"$E_T-E_{\text{CS}}$, eV", 24, MUTED).rotate(m.PI / 2).next_to(ax.y_axis, m.LEFT, buff=0.75)
        names = ["short acid", "short anion", "TEMPO acid", "TEMPO anion"]
        cats = m.VGroup(*[rich(n, 22, MUTED).next_to(ax.c2p(k + 1, -0.6), m.DOWN, buff=0.15) for k, n in enumerate(names)])
        bars = {"b3lyp": m.VGroup(), "camb3lyp": m.VGroup()}
        vals = {"b3lyp": m.VGroup(), "camb3lyp": m.VGroup()}
        for k, r in enumerate(rows):
            for key, dx, col in (("b3lyp", -0.17, GOLD), ("camb3lyp", 0.17, CYAN)):
                v = float(r[key])
                p0, p1 = ax.c2p(k + 1 + dx, 0), ax.c2p(k + 1 + dx, v)
                bar = m.Rectangle(width=0.3, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0, fill_color=col,
                                  fill_opacity=1).move_to((p0 + p1) / 2)
                bars[key].add(bar)
                vals[key].add(M(f"{v:+.2f}", size=25, color=col).next_to(bar, m.UP if v >= 0 else m.DOWN, buff=0.05))
        leg = m.VGroup(*[m.VGroup(m.Square(0.22, stroke_width=0, fill_color=c, fill_opacity=1), rich(t, 24))
                         .arrange(m.RIGHT, buff=0.12) for c, t in ((GOLD, "B3LYP"), (CYAN, "CAM-B3LYP"))])
        leg.arrange(m.RIGHT, buff=0.5).next_to(ax, m.UP, buff=0.12)
        key = rich(r"$<0$: oxidation gives the **diradical**; $>0$: the closed shell", 27, width=5.0).move_to([4.15, 1.75, 0])
        pts = bullets([r"acids: closed shell by $1.2$–$1.4$ eV, SOMO = HOMO",
                       r"anions, CAM-B3LYP: **diradical** by $0.36$ and $0.30$ eV",
                       r"anions, B3LYP: misses by $0.06$–$0.07$ eV"], width=5.0, size=27).move_to([4.2, -0.2, 0])
        self.say("[Our test, T eleven and T eleven c. Two radicals, a short one and a TEMPO-based one, each as the acid and "
                 "as the anion; geometries from unrestricted B three L Y P; and vertical oxidation computed with two functionals. "
                 "The bars show the energy of the oxidised triplet diradical minus that of the oxidised closed shell. "
                 "Negative means oxidation gives the diradical; positive, the closed shell.]",
                 m.AnimationGroup(m.Create(ax), m.Create(zero), m.FadeIn(yl), m.FadeIn(cats), m.FadeIn(key)))
        self.say("[With B three L Y P, the acids oxidise to closed shells, by one point four and one point three electron volts, "
                 "and in them the SOMO is the HOMO.]",
                 m.AnimationGroup(m.FadeIn(bars["b3lyp"]), m.FadeIn(vals["b3lyp"]), m.FadeIn(leg[0]), m.FadeIn(pts[0])))
        self.say("[With the range-separated functional CAM B three L Y P, the anions oxidise to diradicals, by zero point three six "
                 "and zero point three zero electron volts: the pH switch, reproduced.]",
                 m.AnimationGroup(m.FadeIn(bars["camb3lyp"]), m.FadeIn(vals["camb3lyp"]), m.FadeIn(leg[1]),
                                  m.FadeIn(pts[1])))
        self.say("[But with B three L Y P the anions miss, by six to seven hundredths of an electron volt on the closed-shell "
                 "side.]", m.FadeIn(pts[2]))
        self.wait(0.4)


class S118WhatTestSays(Frame):
    """16-quasi.tex, frame 17: 'What the test says'."""

    TITLE = "What the test says"
    SYMBOLS = (r"delocalisation error: approximate functionals over-stabilise charge spread over many atoms; range "
               r"separation reduces it — functional-sensitive: the sign depends on the method")

    def construct(self) -> None:
        self.setup_frame()
        rh = rich("**reproduced**", 32, GREEN)
        rep = bullets(["SOMO 2–3 levels below the HOMO in the anions; equal to the HOMO in the acids",
                       "protonation moves $E_T-E_{\\text{CS}}$ by ~1.2–1.8 eV",
                       "with CAM-B3LYP, the anions oxidise to diradicals"], width=6.0, size=28, colour=GREEN)
        ok = pill("verified")
        left = m.VGroup(rh, rep, ok).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.28).move_to([-3.3, 0.35, 0])
        ch = rich("**caveat**", 32, GOLD)
        cav = bullets(["B3LYP lowers the closed shell by 0.61 eV vs. CAM-B3LYP, the triplet by only 0.17, for the short "
                       "anion",
                       "verdict flips at ~0.07 eV: a functional-sensitive claim",
                       "delocalisation error is a plausible cause, not tested"], width=6.0, size=28)
        right = m.VGroup(ch, cav).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.28).move_to([3.3, 0.45, 0])
        self.say("[What did the test show? Reproduced: in the anions the SOMO lies two to three levels below the HOMO, and "
                 "in the acids it is the HOMO.]", m.AnimationGroup(m.FadeIn(rh), m.FadeIn(rep[0])))
        self.say("[Protonation moves the triplet minus closed-shell energy by about one point two to one point eight "
                 "electron volts.]", m.FadeIn(rep[1]))
        self.say("[And with CAM B three L Y P the anions oxidise to diradicals, as the review says.]",
                 m.AnimationGroup(m.FadeIn(rep[2]), m.FadeIn(ok)))
        self.say("[The caveat: for the short anion, B three L Y P lowers the closed shell by zero point six one electron volts "
                 "relative to CAM B three L Y P, but the triplet by only zero point one seven.]",
                 m.AnimationGroup(m.FadeIn(ch), m.FadeIn(cav[0])))
        self.say("[The verdict flips at about seven hundredths of an electron volt: the claim is sensitive to the "
                 "functional.]", m.FadeIn(cav[1]))
        self.say("[Delocalisation error, the tendency of approximate functionals to over-stabilise charge spread over many "
                 "atoms, is a plausible cause; we did not test it.]", m.FadeIn(cav[2]))
        self.wait(0.4)


class S119ElectronAddition(Frame):
    """16-quasi.tex, frame 18: 'Non-aufbau by electron addition (Figure 17)'."""

    TITLE = "Non-aufbau by electron addition: Figure 17"
    SYMBOLS = (r"P3HT/PCBM: polymer/fullerene solar-cell blend — polaron pair: an electron and a hole on neighbouring "
               r"chains — self-doping: radicals formed inside the crystal without an external dopant")

    def construct(self) -> None:
        self.setup_frame()
        fig = figure("fig17_non_aufbau_by_electron_addition.png", height=4.7, max_width=6.4).move_to([-3.25, 0.1, 0])
        pts = bullets(["**(a)** spirobiphenalenyl VI is reduced to an open-shell singlet; it crystallises without "
                       "dimerising: an intrinsic molecular metal",
                       "**(b)** galvinoxyl in P3HT/PCBM: its LUMO mediates singlet→triplet crossing of polaron pairs via "
                       "exchange, preventing recombination and raising photovoltaic efficiency",
                       "self-doping: in TTFCOO⁻NH₄⁺ the SOMO of the TTF⁺• unit is not the highest occupied orbital, "
                       "according to calculations on a model tetramer"], width=5.8, size=26).move_to([3.55, 0.15, 0])
        self.say("[Finally, non-aufbau behaviour on electron addition, Figure seventeen. In panel a, the spirobiphenalenyl "
                 "radical six is reduced to an open-shell singlet, and it crystallises without dimerising: an intrinsic "
                 "molecular metal.]", m.AnimationGroup(m.FadeIn(fig), m.FadeIn(pts[0])))
        self.say("[In panel b, galvinoxyl added to a P three H T and P C B M solar cell: its LUMO mediates the crossing of "
                 "polaron pairs from singlet to triplet through exchange, which prevents recombination and raises the "
                 "photovoltaic efficiency.]", m.FadeIn(pts[1]))
        self.say("[And self-doping: in a tetrathiafulvalene carboxylate ammonium salt, the SOMO of the oxidised "
                 "tetrathiafulvalene unit is not the highest occupied orbital, according to calculations on a model "
                 "tetramer.]", m.FadeIn(pts[2]))
        self.wait(0.4)
