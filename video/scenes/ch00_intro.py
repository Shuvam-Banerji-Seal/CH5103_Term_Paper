"""Chapter 0: title, roadmap, how to read the video, and the paper (presentation/sections/00-02)."""
import numpy as np

import manimgx as m

from noir import (BLUE, CALLI, CYAN, FG, GARAMOND, GOLD, GREEN, MUTED, ORANGE, PANEL, ROSE, VIOLET, Box, Frame,
                  M, SC, T, boxed, bullets, connect, figure, level, node, pill, rich, spin, why)


class S00Title(Frame):
    """00-title.tex, frame 1: the title page."""

    def construct(self) -> None:
        ornament = m.VGroup(*[m.Ellipse(width=6.0, height=1.8, stroke_color=CYAN, stroke_width=1.2, stroke_opacity=0.35)
                              .rotate(a * m.DEGREES) for a in range(0, 180, 30)],
                            m.Dot(radius=0.12, color=GOLD, fill_opacity=0.6)).scale(0.85).move_to([4.35, 0.4, 0])
        title = rich("Uncommon Molecular Electronic Configurations", size=60, color=GOLD, font=CALLI, width=7.4)
        sub = rich("Theory, derivations and verification of Gryn'ova, Coote & Corminboeuf, 2015", size=30,
                   color=FG, font=GARAMOND, italic=True, width=7.4)
        who = m.VGroup(T("Shuvam Banerji Seal", size=30), T("CH5103 term paper", size=26, color=MUTED))
        who.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.15)
        block = m.VGroup(title, sub, who).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.4).to_edge(m.LEFT, buff=0.9)
        self.add(ornament)
        self.say("[This is a complete, step by step explainer of a review article: Theory and practice of uncommon "
                 "molecular electronic configurations,] by Ganna Gryn'ova, Michelle Coote and Clémence "
                 "Corminboeuf, published in WIREs Computational Molecular Science in twenty fifteen.",
                 m.AnimationGroup(m.Write(title), m.FadeIn(sub, shift=m.UP * 0.1), lag_ratio=0.5),
                 )
        self.say("[We will derive every equation the review relies on, check each one with symbolic algebra, "
                 "quantum chemistry and a proof assistant,] and finish with a claim by claim verdict, which "
                 "includes a sign error in the published paper.",
                 m.AnimationGroup(m.Rotate(ornament, angle=m.PI / 3), m.FadeIn(who, shift=m.UP * 0.1)))
        self.wait(0.5)


ROAD = [("Foundations", GOLD), ("Spin &\nantisymmetry", GOLD), ("Two electrons,\ntwo orbitals", GOLD),
        ("Energies, $J$ & $K$", GOLD), ("Hund's rule", GOLD), ("Static\ncorrelation", GOLD),
        ("Kinetic\nexchange", GOLD), ("NBMOs &\ndisjointness", GOLD), ("Spin\npolarisation", GOLD),
        ("Exciting\ncases", GOLD), ("Koopmans\n& Janak", GOLD), ("Aufbau\non trial", GOLD),
        ("Quasi-closed\nshells", GOLD), ("Our\nverification", CYAN), ("Verdict", GREEN)]


class S01Journey(Frame):
    """01-roadmap.tex, frame 1: 'The journey'."""

    TITLE = "The journey"
    SUBTITLE = "from the Schrödinger equation to a sign error in print"

    def construct(self) -> None:
        self.setup_frame()
        xs = [-5.8, -2.9, 0.0, 2.9, 5.8]
        ys = [1.55, 0.05, -1.45]
        pos = []
        for r, y in enumerate(ys):  # a snake: left→right, right→left, left→right
            row = xs if r % 2 == 0 else xs[::-1]
            pos += [(x, y) for x in row]
        nodes = [node(t, c, width=2.3, height=1.15, size=35).move_to([x, y, 0]) for (t, c), (x, y) in zip(ROAD, pos)]
        arrows = [connect(a, b) for a, b in zip(nodes, nodes[1:])]
        note = rich("Every equation is derived step by step; every identity used was checked by SymPy, PySCF or "
                    "Lean.", size=26, color=MUTED).next_to(m.VGroup(*nodes), m.DOWN, buff=0.5)
        first = m.Succession(*[m.AnimationGroup(m.FadeIn(n, scale=0.9), *( [m.GrowArrow(arrows[i - 1])] if i else []))
                               for i, n in enumerate(nodes[:5])], run_time=4)
        mid = m.Succession(*[m.AnimationGroup(m.FadeIn(n, scale=0.9), m.GrowArrow(arrows[i + 4]))
                             for i, n in enumerate(nodes[5:10])], run_time=4)
        last = m.Succession(*[m.AnimationGroup(m.FadeIn(n, scale=0.9), m.GrowArrow(arrows[i + 9]))
                              for i, n in enumerate(nodes[10:])], run_time=4)
        self.say("Here is the route. [We start from the foundations: the molecular Hamiltonian, spin, and why "
                 "electrons must be antisymmetric. Then two electrons in two orbitals, their energies, and the "
                 "exchange integral K, which leads to Hund's rule.]", first)
        self.say("[Next come the mechanisms that compete with Hund's rule: static correlation, kinetic exchange, "
                 "non-bonding orbitals and their disjointness, and dynamic spin polarisation, followed by the "
                 "review's exciting cases of molecules whose spin state can be switched.]", mid)
        self.say("[The second half turns to orbital energies: Koopmans and Janak, the aufbau principle put on "
                 "trial, and quasi-closed-shell radicals. It ends with our own verification and the verdict.]", last)
        self.say("[Every equation is derived step by step, and every identity we use was checked by computer: "
                 "with the symbolic algebra package SymPy, the quantum chemistry package PySCF, or the Lean "
                 "proof assistant.] At the end we also walk through those Python checks and Lean proofs themselves.",
                 m.FadeIn(note, shift=m.UP * 0.1))
        self.wait(0.4)


class S02HowToRead(Frame):
    """01-roadmap.tex, frame 2: 'How to read these slides'."""

    TITLE = "How to read this video"

    def construct(self) -> None:
        self.setup_frame()
        w = 6.1
        claim = boxed("a statement quoted from the review", "claim", width=w)
        assume = boxed("what a derivation takes for granted", "assume", width=w)
        result = boxed("what the derivation proves", "result", width=w)
        checked = boxed("how we tested it: a script or a proof", "checked", width=w)
        erratum = boxed("where the paper got it wrong", "erratum", width=w)
        left = m.VGroup(claim, assume, result).arrange(m.DOWN, buff=0.42, aligned_edge=m.LEFT)
        right = m.VGroup(checked, erratum).arrange(m.DOWN, buff=0.42, aligned_edge=m.LEFT)
        cols = m.VGroup(left, right).arrange(m.RIGHT, buff=0.6, aligned_edge=m.UP).next_to(self.title_group, m.DOWN, buff=0.5)
        cols.set_x(0)
        pills = m.VGroup(*[pill(p, size=30) for p in ("verified", "error", "overstated", "partial")]).arrange(m.RIGHT, buff=0.2)
        pills.next_to(right, m.DOWN, buff=0.45).align_to(right, m.LEFT)
        demo = m.VGroup(M(r"E=h+J", size=34), why("blue italic: why this step follows", size=26)).arrange(m.RIGHT, buff=0.4)
        demo.next_to(pills, m.DOWN, buff=0.35).align_to(right, m.LEFT)
        strip_note = m.VGroup(SC("symbols", 34, GOLD), rich("strip at the foot of a frame defines its notation", 26))
        strip_note.arrange(m.RIGHT, buff=0.2).next_to(demo, m.DOWN, buff=0.3).align_to(right, m.LEFT)
        units = rich(r"Atomic units throughout: $\hbar=m_e=e=4\pi\varepsilon_0=1$, energies in hartree, $\Eh$.",
                     size=26, color=FG).to_edge(m.DOWN, buff=0.75)
        self.say("Each frame uses the same visual language. [A gold box quotes the review itself.]", m.FadeIn(claim))
        self.say("[A violet box lists what a derivation takes for granted,] [and a green box states what the "
                 "derivation proves.]", m.FadeIn(assume), m.FadeIn(result))
        self.say("[A cyan box says how we tested a result, by a script or a proof,] [and a rose box marks a place "
                 "where the paper got something wrong.]", m.FadeIn(checked), m.FadeIn(erratum))
        self.say("[Verdicts appear as small pills: verified, error, overstated, or partial.]",
                 m.LaggedStart(*[m.FadeIn(p, scale=0.8) for p in pills], lag_ratio=0.25))
        self.say("[Beside each step of a derivation, a short note in blue italics says why the step follows,] "
                 "[and a symbols strip at the foot of the frame defines the notation on it.]",
                 m.FadeIn(demo), m.FadeIn(strip_note))
        self.say("[We use atomic units throughout: h bar, the electron mass, the elementary charge and four pi "
                 "epsilon nought are all one, and energies are in hartree.] One hartree is about twenty seven "
                 "point two electron volts.", m.Write(units))
        self.wait(0.4)


class S03Review(Frame):
    """02-paper.tex, frame 1: 'The review'."""

    TITLE = "The review"

    def construct(self) -> None:
        self.setup_frame()
        page = figure("paper_page1.png", height=5.6).to_edge(m.LEFT, buff=0.7).shift(m.DOWN * 0.3)
        title = rich("Theory and practice of uncommon\nmolecular electronic configurations".replace("\n", " "),
                     size=40, color=GOLD, font=CALLI, width=7.4)
        authors = rich("Ganna Gryn'ova, Michelle L. Coote, Clémence Corminboeuf", size=28, font=GARAMOND)
        venue = rich("WIREs Computational Molecular Science 5, 440–459, 2015 — doi:10.1002/wcms.1233 — "
                     "Advanced Review, open access", size=24, color=MUTED, width=7.4)
        info = m.VGroup(title, authors, venue).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.25)
        info.next_to(page, m.RIGHT, buff=0.6).align_to(page, m.UP)
        pts = bullets(["20 pages, 17 figures, 5 schemes, 118 references",
                       "part theory: what decides a spin state?",
                       "part catalogue: molecules that break the textbook rules"], width=7.4, size=28)
        pts.next_to(info, m.DOWN, buff=0.45).align_to(info, m.LEFT)
        self.say("[The review appeared in WIREs Computational Molecular Science, volume five, pages four hundred "
                 "forty to four hundred fifty nine, in twenty fifteen.] It is an advanced review, and it is open "
                 "access.", m.AnimationGroup(m.FadeIn(page, shift=m.RIGHT * 0.2), m.Write(title),
                                             m.FadeIn(authors), m.FadeIn(venue), lag_ratio=0.2))
        self.say("[It runs to twenty pages, with seventeen figures, five schemes and one hundred eighteen "
                 "references.]", m.FadeIn(pts[0], shift=m.RIGHT * 0.1))
        self.say("[Part of it is theory: what decides whether a molecule's ground state is high spin or low "
                 "spin?]", m.FadeIn(pts[1], shift=m.RIGHT * 0.1))
        self.say("[And part of it is a catalogue of real molecules that break the textbook rules.]",
                 m.FadeIn(pts[2], shift=m.RIGHT * 0.1))
        self.wait(0.4)


def two_level(x: float, y: float, gap: float, top_up: bool, bottom_up: bool = True) -> m.VGroup:
    a = level(x, y, w=1.0)
    b = level(x, y + gap, w=1.0)
    return m.VGroup(a, b, spin(x, y, bottom_up), spin(x, y + gap, top_up))


class S04TwoConfigs(Frame):
    """02-paper.tex, frame 2: 'Two uncommon configurations'."""

    TITLE = "Two uncommon configurations"
    SUBTITLE = "the two halves of the paper"

    def construct(self) -> None:
        self.setup_frame()
        h1 = SC("1. fluctuating multiplicity", 34, GOLD).move_to([-3.6, 2.2, 0])
        h2 = SC("2. non-aufbau ordering", 34, GOLD).move_to([3.6, 2.2, 0])
        g = 0.8  # level spacing
        trip = m.VGroup(level(-5.2, 0.5, 1.1), level(-5.2, 0.5 + g, 1.1), spin(-5.2, 0.5, True), spin(-5.2, 0.5 + g, True))
        oss = m.VGroup(level(-2.0, 0.5, 1.1), level(-2.0, 0.5 + g, 1.1), spin(-2.0, 0.5, True), spin(-2.0, 0.5 + g, False))
        lt = T("triplet", 30, ROSE).next_to(trip, m.DOWN, buff=0.3)
        lo = T("open-shell singlet", 30, BLUE).next_to(oss, m.DOWN, buff=0.3)
        vs = T("vs", 40, GOLD, font=CALLI).move_to([-3.6, 0.9, 0])
        t1 = rich("two nearly degenerate orbitals, two electrons: parallel or antiparallel?", 28, width=6.3)
        t1.move_to([-3.6, -1.6, 0])
        q1 = rich("Who wins: Hund's rule, or correlation?", 30, GOLD).next_to(t1, m.DOWN, buff=0.35)
        au = m.VGroup(level(1.9, -0.1, 1.1), level(1.9, -0.1 + g, 1.1, "SOMO"), level(1.9, -0.1 + 2 * g, 1.1),
                      spin(1.9, -0.1, True), spin(1.9, -0.1, False), spin(1.9, -0.1 + g, True))
        qc = m.VGroup(level(4.8, -0.1, 1.1, "SOMO"), level(4.8, -0.1 + g, 1.1, "HOMO"), level(4.8, -0.1 + 2 * g, 1.1),
                      spin(4.8, -0.1, True), spin(4.8, -0.1 + g, True), spin(4.8, -0.1 + g, False))
        la = T("aufbau", 30, MUTED).next_to(au, m.DOWN, buff=0.3)
        lq = T("quasi-closed shell", 30, ROSE).next_to(qc, m.DOWN, buff=0.3)
        t2 = rich("the singly occupied orbital lies below a doubly occupied one", 28, width=6.3).move_to([3.6, -1.6, 0])
        q2 = rich("Redox then gives a polyradical, a diradical in the simplest case.", 30, GOLD, width=6.3)
        q2.next_to(t2, m.DOWN, buff=0.35)
        self.say("The paper has two halves, one for each kind of uncommon configuration.")
        self.say("[The first is fluctuating multiplicity.] [Take two nearly degenerate orbitals and two electrons.] "
                 "[The electrons can sit with parallel spins, a triplet,] [or with antiparallel spins in different "
                 "orbitals, an open-shell singlet.]",
                 m.FadeIn(h1), m.FadeIn(m.VGroup(trip[0], trip[1], oss[0], oss[1])),
                 m.AnimationGroup(m.FadeIn(m.VGroup(trip[2], trip[3])), m.FadeIn(lt)),
                 m.AnimationGroup(m.FadeIn(vs), m.FadeIn(m.VGroup(oss[2], oss[3])), m.FadeIn(lo), m.FadeIn(t1)))
        self.say("[Which one is the ground state? Does Hund's rule win, or does electron correlation?]",
                 m.Write(q1))
        self.say("[The second half is about non-aufbau ordering.] [In the usual, aufbau, picture of a radical, the "
                 "singly occupied molecular orbital, the SOMO, is the highest occupied orbital.] [In a quasi-closed "
                 "shell the SOMO lies below a doubly occupied orbital, the HOMO.]",
                 m.FadeIn(h2), m.AnimationGroup(m.FadeIn(au), m.FadeIn(la)),
                 m.AnimationGroup(m.FadeIn(qc), m.FadeIn(lq), m.FadeIn(t2)))
        self.say("[So when such a molecule is oxidised or reduced, the electron leaves or arrives elsewhere, and the "
                 "unpaired SOMO electron stays: redox gives a polyradical, which is a diradical in the simplest "
                 "case.]", m.Write(q2))
        self.wait(0.4)


class S05WhyCare(Frame):
    """02-paper.tex, frame 3: 'Why anyone cares'."""

    TITLE = "Why anyone cares"

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"species with unpaired electrons display unique chemical reactivity and are capable of carrying '
                      'magnetism and conductivity functionalities" — p. 440', "claim", width=6.6, size=26)
        pts = bullets(["spin valves, switches, field-effect transistors, logic",
                       "wanted: a set spin state that a stimulus can flip",
                       "but few radicals are persistent, crystallisable and not Mott insulators"], width=6.6, size=26)
        left = m.VGroup(claim, pts).arrange(m.DOWN, buff=0.45, aligned_edge=m.LEFT).to_edge(m.LEFT, buff=0.6)
        left.shift(m.DOWN * 0.2)
        mol = node("molecule", CYAN, width=2.4, height=0.9, size=28).move_to([3.9, 0.1, 0])
        stim = [("light", GOLD, 90), ("pH", GREEN, 30), ("redox", ROSE, -30), ("heat", ORANGE, -90),
                ("field", BLUE, 210), ("metal ion", VIOLET, 150)]
        labels, arrows = [], []
        for name, col, ang in stim:
            p = mol.get_center() + 2.1 * np.array([np.cos(ang * m.DEGREES), np.sin(ang * m.DEGREES), 0])
            lab = T(name, 26, col).move_to(p)
            labels.append(lab)
            arrows.append(connect(lab, mol, MUTED, buff=0.1))
        cap = rich("stimuli that switch spin states — Figures 7 to 9 of the review", 22, MUTED, width=4.6)
        cap.next_to(mol, m.DOWN, buff=2.3)
        self.say("[Why care about any of this? In the review's words, species with unpaired electrons display unique "
                 "chemical reactivity and are capable of carrying magnetism and conductivity functionalities.]",
                 m.FadeIn(claim))
        self.say("[That makes them candidates for spin valves, switches, field-effect transistors and logic.]",
                 m.FadeIn(pts[0], shift=m.RIGHT * 0.1))
        self.say("[What such devices want is a molecule with a well defined spin state that an outside stimulus can "
                 "flip: light, pH, redox chemistry, heat, a magnetic field, or a metal ion.]",
                 m.AnimationGroup(m.FadeIn(pts[1], shift=m.RIGHT * 0.1), m.FadeIn(mol),
                                  m.LaggedStart(*[m.AnimationGroup(m.FadeIn(l), m.GrowArrow(a))
                                                  for l, a in zip(labels, arrows)], lag_ratio=0.2),
                                  m.FadeIn(cap)))
        self.say("[The catch is that few radicals are persistent, which means they survive long enough to be used, "
                 "can be crystallised, and are not Mott insulators.] A Mott insulator is a material whose "
                 "electrons are held in place by their mutual repulsion, so it does not conduct even where simple "
                 "band theory says it should.", m.FadeIn(pts[2], shift=m.RIGHT * 0.1))
        self.wait(0.4)


class S06WhatWeDid(Frame):
    """02-paper.tex, frame 4: 'What we did with it'."""

    TITLE = "What we did with it"

    def construct(self) -> None:
        self.setup_frame()
        read = node("read\n20 pp., 118 refs", GOLD, 2.6, 1.3, size=32).move_to([-5.0, 0.4, 0])
        der = node("derive\n18 sections", VIOLET, 2.6, 1.3, size=32).move_to([-1.8, 0.4, 0])
        num = node("compute\nPySCF, SymPy, ED", CYAN, 2.9, 1.3, size=32).move_to([1.6, 1.4, 0])
        lean = node("prove\nLean 4 + Mathlib", CYAN, 2.9, 1.3, size=32).move_to([1.6, -0.6, 0])
        ver = node("verdict\nclaim by claim", GREEN, 2.6, 1.3, size=32).move_to([5.0, 0.4, 0])
        arrows = [connect(read, der), connect(der, num), connect(der, lean), connect(num, ver), connect(lean, ver)]
        counts = rich("21 checks: T1 to T17, with T1b, T9b and T11a to c — 17 machine-checked theorems", 24, MUTED,
                      width=6.0).move_to([1.6, -2.1, 0])
        err = rich("… and one published sign error", 28, ROSE).move_to([5.0, -1.5, 0])
        self.say("[Here is what we did with the review. We read all twenty pages and the cited work we could "
                 "access.]", m.FadeIn(read))
        self.say("[We derived the mathematics behind it, step by step, in eighteen sections.]",
                 m.AnimationGroup(m.GrowArrow(arrows[0]), m.FadeIn(der)))
        self.say("[We computed: with PySCF for quantum chemistry, SymPy for exact symbolic algebra, and exact "
                 "diagonalisation of model Hamiltonians.] [And we proved the algebraic identities in the Lean four "
                 "proof assistant, with its Mathlib library.]",
                 m.AnimationGroup(m.GrowArrow(arrows[1]), m.FadeIn(num)),
                 m.AnimationGroup(m.GrowArrow(arrows[2]), m.FadeIn(lean)))
        self.say("[Everything feeds a verdict, claim by claim.]",
                 m.AnimationGroup(m.GrowArrow(arrows[3]), m.GrowArrow(arrows[4]), m.FadeIn(ver)))
        self.say("[In total there are twenty one numbered checks, T one to T seventeen with T one b, T nine b and T "
                 "eleven a to c, and seventeen machine-checked theorems.]", m.FadeIn(counts))
        self.say("[And along the way we found one published sign error.]", m.Write(err))
        self.wait(0.4)
