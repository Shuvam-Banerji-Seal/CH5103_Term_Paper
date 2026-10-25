"""Chapter 9: NBMOs and disjointness (presentation/sections/11-nbmo.tex)."""
import csv

import numpy as np

import manimgx as m

from ch01_foundations import explain
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ORANGE, ROSE, ROOT, Box, Derivation, Frame, Plot, M, axes, boxed,
                  bullets, diagram, figure, rich)


def molecule(coords: dict, bonds, scale: float = 1.0, labels: dict | None = None, size: float = 24) -> m.VGroup:
    """Carbon skeleton: muted bonds, light atom dots, optional atom labels. Returns VGroup(bonds, atoms, labels)
    with .at[name] = the atom's screen position."""
    pos = {k: np.array([x * scale, y * scale, 0.0]) for k, (x, y) in coords.items()}
    lines = m.VGroup(*[m.Line(pos[a], pos[b], color=MUTED, stroke_width=4) for a, b in bonds])
    dots = m.VGroup(*[m.Dot(p, radius=0.06, color=FG) for p in pos.values()])
    labs = m.VGroup()
    for k, (direction, text) in (labels or {}).items():
        labs.add(rich(text, size, MUTED).next_to(m.Dot(pos[k]), direction, buff=0.12))
    g = m.VGroup(lines, dots, labs)
    g.at = pos
    return g


def lobes(mol: m.VGroup, coeffs: dict, radius: float = 0.75) -> m.VGroup:
    """Lobes with area proportional to c_i^2: rose for +, blue for -, as in the slides' NBMO pictures."""
    out = m.VGroup()
    for k, c in coeffs.items():
        if abs(c) < 1e-9:
            continue
        col = ROSE if c > 0 else BLUE
        out.add(m.Circle(radius=radius * abs(c), stroke_color=col, stroke_width=3, fill_color=col,
                         fill_opacity=0.45).move_to(mol.at[k]))
    return out


def sync_shift(mol: m.VGroup, v) -> m.VGroup:
    mol.shift(v)
    mol.at = {k: p + np.array(v) for k, p in mol.at.items()}
    return mol


class S67Classification(Frame):
    """11-nbmo.tex, frame 1: 'Borden & Davidson's classification'."""

    TITLE = "Borden & Davidson's classification"
    SYMBOLS = (r"NBMO: non-bonding MO, orbital energy equal to that of an isolated $p$ orbital — disjoint: the two NBMOs "
               r"share no atom — CBD cyclobutadiene, TME tetramethyleneethane, TMM trimethylenemethane, MX "
               r"$m$-xylylene, TriMB 1,3,5-trimethylenebenzene")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"If the two orbitals do not have common atoms and the probability of two electrons occupying the '
                      'same space is nil independent of their spins, they are termed disjoint. Under such circumstances, '
                      'the energy of an open-shell singlet can become comparable to or even lower than that of a '
                      'triplet." — p. 443', "claim", width=6.4, size=27).move_to([-3.2, 0.9, 0])
        todo = rich(r"three things to derive: **(1)** how to find NBMOs, **(2)** when they can be disjoint, **(3)** why "
                    r"disjoint means $K\approx0$", 28, width=6.4).next_to(claim, m.DOWN, buff=0.35)
        fig = figure("fig03_high_low_spin_polyradicals.png", height=4.3, max_width=5.9).move_to([3.55, 0.45, 0])
        cap = rich("Fig. 3: high- and low-spin polyradicals", 22, MUTED).next_to(fig, m.DOWN, buff=0.12)
        self.say("[Part ten turns to the molecules themselves. The review's Figure three collects high-spin and low-spin "
                 "polyradicals: cyclobutadiene, tetramethyleneethane, trimethylenemethane, meta xylylene and "
                 "trimethylenebenzene.]", m.AnimationGroup(m.FadeIn(fig), m.FadeIn(cap)))
        self.say("[Their spin follows Borden and Davidson's classification. The review says: if the two orbitals do not "
                 "have common atoms and the probability of two electrons occupying the same space is nil independent of "
                 "their spins, they are termed disjoint. Under such circumstances, the energy of an open-shell singlet "
                 "can become comparable to or even lower than that of a triplet.]", m.FadeIn(claim))
        self.say("[The two orbitals are the non-bonding molecular orbitals, or N B M Os, whose energy equals that of an "
                 "isolated p orbital. Three things need deriving: first, how to find them; second, when they can be "
                 "disjoint; and third, why disjoint means the exchange integral K is close to zero.]", m.FadeIn(todo))
        self.wait(0.4)


class S68Huckel(Frame):
    """11-nbmo.tex, frame 2: 'Hückel theory and the zero-sum rule'."""

    TITLE = "Hückel theory and the zero-sum rule"
    SUBTITLE = (r"assume (Hückel) one $p_\pi$ per carbon; $H_{ii}=\alpha$, $H_{ij}=\beta$ if bonded, else 0; zero "
                r"overlap")
    SYMBOLS = (r"**here $\alpha,\beta$ are Hückel energies, not spin**: $\alpha$ = energy of a $p_\pi$ electron on one "
               r"carbon, $\beta<0$ = coupling of bonded neighbours — $\mathbf A$: adjacency matrix, $A_{ij}=1$ if $i,j$ "
               r"bonded — $\mathbf c$: MO coefficients — $\mathcal N(i)$: neighbours of atom $i$")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\mathbf H\mathbf c=E\mathbf c,\quad \mathbf H", r"=\alpha\mathbf 1+\beta\mathbf A", "Hückel's assumptions"),
            (r"(\alpha\mathbf 1+\beta\mathbf A)\mathbf c", r"=(\alpha+x\beta)\mathbf c", r"write $E=\alpha+x\beta$"),
            (r"\mathbf A\mathbf c", r"=x\,\mathbf c", r"subtract $\alpha\mathbf c$, divide by $\beta$"),
            (r"\text{NBMO: }E=\alpha", r"\Leftrightarrow\ \mathbf A\mathbf c=\mathbf 0", r"$x=0$"),
            (r"\text{row }i:", r"\textstyle\sum_{j\in\mathcal N(i)}c_j=0", r"row $i$ of $\mathbf A$ marks $i$'s neighbours"),
        ], size=32, why_size=24).move_to([-2.35, 0.75, 0])
        rule = rich("**for every atom, the NBMO coefficients of its neighbours sum to zero**", 28, GOLD, width=7.4)
        rule.next_to(d, m.DOWN, buff=0.35).align_to(d, m.LEFT)
        allyl = molecule({1: (0, 0), 2: (1, 0.6), 3: (2, 0)}, [(1, 2), (2, 3)], scale=1.45)
        sync_shift(allyl, [3.35, -0.1, 0])
        lob = lobes(allyl, {1: 1 / np.sqrt(2), 2: 0.0, 3: -1 / np.sqrt(2)}, radius=0.85)
        cl = m.VGroup(M(r"+\tfrac1{\sqrt2}", size=28).next_to(m.Dot(allyl.at[1]), m.DOWN, buff=0.75),
                      M("0", size=28).next_to(m.Dot(allyl.at[2]), m.UP, buff=0.25),
                      M(r"-\tfrac1{\sqrt2}", size=28).next_to(m.Dot(allyl.at[3]), m.DOWN, buff=0.75))
        cap = rich("allyl NBMO: centre sees $c_1+c_3=0$", 24, MUTED).move_to([4.8, -2.05, 0])
        self.say("[To find N B M Os we use Hückel theory. Its assumptions: one p pi orbital per carbon, a diagonal energy "
                 "alpha, a coupling beta between bonded neighbours and zero otherwise, and zero overlap. So the "
                 "Hamiltonian matrix is alpha times the identity plus beta times the adjacency matrix A.] Careful: alpha "
                 "and beta here are Hückel energies, not spin functions.", m.FadeIn(d.rows[0]))
        self.say("[Write each orbital energy as alpha plus x beta.]", m.FadeIn(d.rows[1]))
        self.say("[Subtract alpha times c from both sides and divide by beta: the coefficient vector is an eigenvector "
                 "of the adjacency matrix, with eigenvalue x.]", m.FadeIn(d.rows[2]))
        self.say("[A non-bonding orbital has energy exactly alpha, so x is zero: A times c is the zero vector.]",
                 m.FadeIn(d.rows[3]))
        self.say("[Row i of the adjacency matrix has a one for each neighbour of atom i, so row i of this equation says "
                 "the coefficients on the neighbours of atom i add up to zero.]", m.FadeIn(d.rows[4]))
        self.say("[That is the zero-sum rule: for every atom, the N B M O coefficients of its neighbours sum to zero.]",
                 m.FadeIn(rule))
        self.say("[The allyl radical shows it. The end atoms carry plus and minus one over root two, and the centre "
                 "carries zero.] The centre's neighbours are the two ends, and their coefficients cancel; each end's only "
                 "neighbour is the centre, whose coefficient is zero. Every atom is satisfied.",
                 m.AnimationGroup(m.FadeIn(allyl), m.FadeIn(lob), m.FadeIn(cl), m.FadeIn(cap)))
        self.wait(0.4)


class S69Pairing(Frame):
    """11-nbmo.tex, frame 3: 'Alternant hydrocarbons: the pairing theorem'."""

    TITLE = "Alternant hydrocarbons: the pairing theorem"
    SYMBOLS = (r"alternant: atoms can be split into two sets with bonds only between the sets, no odd rings — "
               r"$\mathbf u,\mathbf v$: coefficients on the starred and unstarred atoms — $\mathbf B$: bonds from starred "
               r"to unstarred — $\mathsf T$: transpose")

    def construct(self) -> None:
        self.setup_frame()
        top = rich(r"star every other atom; bonds only join starred ($\mathcal A$) to unstarred ($\mathcal B$):", 30)
        top.move_to([0, 2.2, 0])
        A = M(r"\mathbf A=\begin{pmatrix}\mathbf 0&\mathbf B\\\mathbf B^{\mathsf T}&\mathbf 0\end{pmatrix}", size=40)
        A.move_to([0, 1.25, 0])
        e = explain("zero diagonal blocks: no bond joins two starred atoms or two unstarred atoms", width=9)
        e.next_to(A, m.DOWN, buff=0.15)
        d = Derivation([
            (r"\mathbf A\binom{\mathbf u}{\mathbf v}=x\binom{\mathbf u}{\mathbf v}",
             r"\ \Leftrightarrow\ \mathbf B\mathbf v=x\mathbf u,\quad\mathbf B^{\mathsf T}\mathbf u=x\mathbf v",
             "multiply the blocks"),
            (r"\mathbf A\binom{\mathbf u}{-\mathbf v}",
             r"=\binom{-\mathbf B\mathbf v}{\mathbf B^{\mathsf T}\mathbf u}=\binom{-x\mathbf u}{x\mathbf v}"
             r"=-x\binom{\mathbf u}{-\mathbf v}", "flip the sign on one set"),
        ], size=34).move_to([0, -0.95, 0])
        res = rich(r"levels come in $\pm x$ pairs, mirrored about $\alpha$ — Lean: `pairing`", 30, GOLD)
        res.move_to([0, -2.4, 0])
        self.say("[Most of these molecules are alternant hydrocarbons: you can star every other atom so that bonds only "
                 "join starred atoms to unstarred ones.] That is possible exactly when there are no odd rings.",
                 m.FadeIn(top))
        self.say("[Order the starred atoms first. Then the adjacency matrix has zero diagonal blocks and an off-diagonal "
                 "block B with its transpose.]", m.Write(A))
        self.say("[The zero blocks say that no bond joins two starred atoms or two unstarred atoms.]", m.FadeIn(e))
        self.say("[Split an eigenvector into u on the starred atoms and v on the unstarred ones. Multiplying the blocks, "
                 "the eigenvalue equation becomes two equations: B v equals x u, and B transpose u equals x v.]",
                 m.FadeIn(d.rows[0]))
        self.say("[Now flip the sign of v. A times u, minus v, is minus B v on top and B transpose u below, which is "
                 "minus x u and x v, which is minus x times the flipped vector.]", m.FadeIn(d.rows[1]))
        self.say("[So every level x has a partner at minus x: the levels come in pairs mirrored about alpha. This is the "
                 "pairing theorem, and our Lean file proves it as the theorem named pairing.]", m.FadeIn(res))
        self.wait(0.4)


class S70HowMany(Frame):
    """11-nbmo.tex, frame 4: 'How many NBMOs?'."""

    TITLE = "How many NBMOs?"
    SYMBOLS = (r"rank: number of nonzero eigenvalues — #NBMO: number of zero eigenvalues, $x=0$ — $n_A,n_B$: sizes of "
               r"the starred and unstarred sets — $N$: number of $\pi$ atoms")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\operatorname{rank}\mathbf A", r"=2\operatorname{rank}\mathbf B", r"$\pm x$ pairs"),
            ("", r"\le2\min(n_A,n_B)", "rank ≤ smaller side"),
            (r"\#\text{NBMO}=N-\operatorname{rank}\mathbf A", r"\ge|n_A-n_B|", r"$N=n_A+n_B$"),
        ], size=32, why_size=24)
        d.move_to([-6.6 + d.width / 2, 1.15, 0])
        lh = rich(r"sharper (Longuet-Higgins): $\operatorname{rank}\mathbf B\le T$, the size of a maximum matching — the "
                  r"largest set of bonds sharing no atom ⇒ $\#\text{NBMO}\ge N-2T$", 28, width=7.0)
        lh.next_to(d, m.DOWN, buff=0.4).align_to(d, m.LEFT)
        err = boxed("square cyclobutadiene: $N=4$, $T=2$, so $N-2T=0$, yet it has *two* NBMOs", "erratum",
                    width=4.1, size=26, tag="Careful: only a bound").move_to([4.65, 1.0, 0])
        sq = m.Square(side_length=1.3, color=MUTED, stroke_width=3).move_to([4.65, -1.0, 0])
        c = [sq.get_corner(v) for v in (m.DL, m.DR, m.UR, m.UL)]
        match = m.VGroup(m.Line(c[0], c[1], color=GOLD, stroke_width=7), m.Line(c[3], c[2], color=GOLD, stroke_width=7))
        dots = m.VGroup(*[m.Dot(p, radius=0.06, color=FG) for p in c])
        ml = rich("perfect matching", 22, GOLD).next_to(sq, m.DOWN, buff=0.15)
        t8 = rich("T8 caught our own wrong assumption here.", 24, MUTED).move_to([4.65, -2.35, 0])
        self.say("[How many N B M Os does an alternant hydrocarbon have? Each nonzero level of B gives a plus and minus x "
                 "pair of levels of A, so the rank of A is twice the rank of B.] The rank counts the nonzero eigenvalues.",
                 m.FadeIn(d.rows[0]))
        self.say("[A rank can never exceed the smaller side of the matrix, so it is at most twice the smaller of n A and "
                 "n B.]", m.FadeIn(d.rows[1]))
        self.say("[The number of N B M Os is the number of zero eigenvalues, N minus the rank. With N equal to n A plus n "
                 "B, that is at least the difference between the two set sizes.]", m.FadeIn(d.rows[2]))
        self.say("[A sharper bound, due to Longuet-Higgins: the rank of B is at most T, the size of a maximum matching, "
                 "meaning the largest set of bonds that share no atom. So the number of N B M Os is at least N minus two "
                 "T.]", m.FadeIn(lh))
        self.say("[Careful: these are only lower bounds. Square cyclobutadiene has four atoms and a perfect matching of two "
                 "bonds, so N minus two T is zero, yet it has two N B M Os.]",
                 m.AnimationGroup(m.FadeIn(err), m.Create(sq), m.FadeIn(dots), m.Create(match), m.FadeIn(ml)))
        self.say("[We had first assumed the bound was an equality; test T eight caught that wrong assumption.]",
                 m.FadeIn(t8))
        self.wait(0.4)


class S71TME(Frame):
    """11-nbmo.tex, frame 5: 'Tetramethyleneethane: solving the zero-sum equations'."""

    TITLE = "Tetramethyleneethane: solving the zero-sum equations"
    SYMBOLS = (r"$c_i$: NBMO coefficient on atom $i$ — $\chi_i$: the $p_\pi$ atomic orbital on carbon $i$ — two free "
               r"parameters, $c_3$ and $c_5$ ⇒ two NBMOs — $\tfrac1{\sqrt2}$: normalisation")

    def construct(self) -> None:
        self.setup_frame()
        coords = {1: (-0.6, 0), 2: (0.6, 0), 3: (-1.3, 1), 4: (-1.3, -1), 5: (1.3, 1), 6: (1.3, -1)}
        labels = {1: (m.DOWN, "1"), 2: (m.DOWN, "2"), 3: (m.LEFT, "3"), 4: (m.LEFT, "4"), 5: (m.RIGHT, "5"),
                  6: (m.RIGHT, "6")}
        tme = molecule(coords, [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6)], scale=1.35, labels=labels, size=26)
        sync_shift(tme, [-4.4, 0.3, 0])
        d = Derivation([
            (r"\text{atom 3:}\ c_1", r"=0", "its only neighbour is atom 1"),
            (r"\text{atom 5:}\ c_2", r"=0", "its only neighbour is atom 2"),
            (r"\text{atom 1:}\ c_2+c_3+c_4", r"=0\ \Rightarrow\ c_4=-c_3", r"use $c_2=0$"),
            (r"\text{atom 2:}\ c_1+c_5+c_6", r"=0\ \Rightarrow\ c_6=-c_5", r"use $c_1=0$"),
        ], size=32, why_size=24).move_to([2.0, 1.3, 0])
        phis = M(r"\varphi_a=\tfrac1{\sqrt2}(\chi_3-\chi_4),\qquad\varphi_b=\tfrac1{\sqrt2}(\chi_5-\chi_6)", size=36)
        phis.move_to([2.0, -0.85, 0])
        la = lobes(tme, {3: 1 / np.sqrt(2), 4: -1 / np.sqrt(2)}, radius=0.7)
        lb = lobes(tme, {5: 1 / np.sqrt(2), 6: -1 / np.sqrt(2)}, radius=0.7)
        ok = rich("no common atom: disjoint", 30, GREEN).move_to([2.0, -1.9, 0])
        self.say("[Tetramethyleneethane, T M E, has six pi atoms: a central bond from atom one to atom two, with atoms "
                 "three and four on atom one, and five and six on atom two. Apply the zero-sum rule atom by atom.]",
                 m.FadeIn(tme))
        self.say("[Atom three has a single neighbour, atom one, so its rule forces c one to be zero.]", m.FadeIn(d.rows[0]))
        self.say("[Likewise atom five's only neighbour is atom two, so c two is zero.] Atoms four and six give the same "
                 "two conditions again.", m.FadeIn(d.rows[1]))
        self.say("[Atom one's neighbours are two, three and four. With c two zero, c four equals minus c three.]",
                 m.FadeIn(d.rows[2]))
        self.say("[Atom two's neighbours are one, five and six. With c one zero, c six equals minus c five.]",
                 m.FadeIn(d.rows[3]))
        self.say("[Two coefficients remain free, c three and c five, so there are two N B M Os. Choosing one free "
                 "parameter at a time and normalising gives phi a, chi three minus chi four over root two,] [and phi b, "
                 "chi five minus chi six over root two.]",
                 m.AnimationGroup(m.FadeIn(phis), m.FadeIn(la)), m.FadeIn(lb))
        self.say("[They share no atom: the N B M Os of T M E are disjoint.]", m.FadeIn(ok))
        self.wait(0.4)


class S72JsDiagrams(Frame):
    """11-nbmo.tex, frame 6: 'Disjoint pairs, drawn by our JavaScript'."""

    TITLE = "Disjoint pairs, drawn by our JavaScript"
    SUBTITLE = "lobe area ∝ $|c_i|^2$; rose $+$, blue $-$"
    SYMBOLS = (r"$a_i,b_i$: coefficients of $\pa,\pb$ on atom $i$ — degenerate NBMOs can be mixed freely; we pick the "
               r"mixture that overlaps least — $\sum_ia_i^2b_i^2=0$: no atom carries both orbitals")

    def construct(self) -> None:
        self.setup_frame()
        tme = diagram("nbmo_tme.svg", height=3.6, max_width=6.6).move_to([-3.4, 0.55, 0])
        cbd = diagram("nbmo_cbd.svg", height=3.6, max_width=5.6).move_to([3.6, 0.55, 0])
        pipe = rich(r"JS code: Hückel matrix → Jacobi diagonalisation → rotate the degenerate pair to minimise "
                    r"$\sum_ia_i^2b_i^2$ → SVG → PDF", 28, width=12.4).move_to([0, -1.95, 0])
        self.say("[Our JavaScript draws these orbitals. Lobe area is proportional to the squared coefficient, rose for "
                 "plus and blue for minus. On the left, T M E: phi a lives on atoms three and four, phi b on five and six."
                 "]", m.FadeIn(tme))
        self.say("[On the right, square cyclobutadiene: its two N B M Os can also be chosen to share no atom, each living "
                 "on one diagonal pair.]", m.FadeIn(cbd))
        self.say("[The pipeline: build the Hückel matrix, diagonalise it by Jacobi rotations, then rotate the degenerate "
                 "pair to minimise the sum over atoms of a i squared times b i squared, and write S V G, then P D F.] A "
                 "degenerate pair can be mixed freely, so we pick the mixture that overlaps least; when that sum is zero, "
                 "no atom carries both orbitals.", m.FadeIn(pipe))
        self.wait(0.4)


class S73TMM(Frame):
    """11-nbmo.tex, frame 7: 'Trimethylenemethane cannot be made disjoint'."""

    TITLE = "Trimethylenemethane cannot be made disjoint"
    SYMBOLS = (r"atoms: centre 0, terminals 1–3 — support of a vector: the atoms where it is nonzero — “for every basis”: "
               r"no rotation of the two NBMOs can separate them")

    def construct(self) -> None:
        self.setup_frame()
        items = [r"1. zero-sum at a terminal ⇒ $c_0=0$",
                 r"2. zero-sum at the centre ⇒ $c_1+c_2+c_3=0$",
                 r"3. a vector in this plane with one nonzero entry cannot sum to zero: **at least 2 nonzero**",
                 r"4. two such vectors with disjoint supports need $\ge4$ terminal atoms; there are 3"]
        lst = m.VGroup(*[rich(t, 29, width=6.2) for t in items]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.3)
        lst.move_to([-3.3, 0.6, 0])
        verdict = rich("nondisjoint, for every choice of basis", 30, ROSE).next_to(lst, m.DOWN, buff=0.4)
        verdict.align_to(lst, m.LEFT)
        tmm = diagram("nbmo_tmm.svg", height=3.9, max_width=6.0).move_to([3.5, 0.4, 0])
        mx = diagram("nbmo_mx.svg", height=3.9, max_width=5.6).move_to([3.5, 0.55, 0])
        mxl = rich("$m$-xylylene: also nondisjoint", 24, MUTED).next_to(mx, m.DOWN, buff=0.1)
        self.say("[Trimethylenemethane, T M M, is different. Number the centre zero and the terminals one to three. Each "
                 "terminal's only neighbour is the centre, so the zero-sum rule there forces c zero to be zero.]",
                 m.FadeIn(lst[0]))
        self.say("[At the centre, the rule says c one plus c two plus c three is zero.] So both N B M Os live in this "
                 "two-dimensional plane of terminal coefficients.", m.FadeIn(lst[1]))
        self.say("[A vector in this plane with only one nonzero entry cannot sum to zero, so every N B M O has at least "
                 "two nonzero coefficients.]", m.FadeIn(lst[2]))
        self.say("[Two such vectors with no atom in common would need at least four terminal atoms, and there are only "
                 "three.]", m.FadeIn(lst[3]))
        self.say("[So T M M is nondisjoint, for every choice of basis: no rotation of its two N B M Os can separate them, "
                 "as the drawing shows.]", m.AnimationGroup(m.FadeIn(verdict), m.FadeIn(tmm)))
        self.say("[Meta xylylene is also nondisjoint.]",
                 m.AnimationGroup(m.FadeOut(tmm), m.FadeIn(mx), m.FadeIn(mxl)))
        self.wait(0.4)


class S74WhyKZero(Frame):
    """11-nbmo.tex, frame 8: 'Why disjoint means K_ab = 0'."""

    TITLE = r"Why disjoint means $K_{ab}=0$"
    SUBTITLE = (r"assume zero differential overlap (ZDO): $\eri\mu\nu\lambda\sigma=\delta_{\mu\nu}\delta_{\lambda\sigma}"
                r"\,\gamma_{\mu\lambda}$")
    SYMBOLS = (r"ZDO: products of two different atomic orbitals are treated as zero — $\gamma_{\mu\lambda}$: repulsion "
               r"between an electron on atom $\mu$ and one on atom $\lambda$ — $\gamma$ is positive definite, so nondisjoint "
               r"⇒ $K_{ab}>0$")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"K_{ab}=\eri abab", r"=\textstyle\sum_{\mu\nu\lambda\sigma}a_\mu b_\nu a_\lambda b_\sigma\,\eri\mu\nu\lambda\sigma",
             r"insert $\pa=\sum a_\mu\chi_\mu$, $\pb=\sum b_\nu\chi_\nu$"),
            ("", r"=\textstyle\sum_{\mu\lambda}(a_\mu b_\mu)(a_\lambda b_\lambda)\,\gamma_{\mu\lambda}",
             r"ZDO keeps only $\nu=\mu$, $\sigma=\lambda$"),
            (r"\text{disjoint }(a_\mu b_\mu=0\ \forall\mu):\ K_{ab}", r"=0", "every product vanishes"),
            (r"\text{Hubbard }(\gamma_{\mu\lambda}=U\delta_{\mu\lambda}):\ K_{ab}", r"=U\textstyle\sum_\mu a_\mu^2b_\mu^2",
             "on-site repulsion only"),
        ], size=32, why_size=24).move_to([0, 0.55, 0])
        nums = rich(r"TMM: $\min\sum a^2b^2=\tfrac16$ — MX: $\tfrac1{16}$ — Python *and* JavaScript agree", 28)
        nums.move_to([0, -2.0, 0])
        self.say("[Why does disjointness kill the exchange integral? Assume zero differential overlap: any product of two "
                 "different atomic orbitals is treated as zero, so the two-electron integral over atomic orbitals mu nu "
                 "lambda sigma survives only when mu equals nu and lambda equals sigma, and then it is gamma mu lambda, "
                 "the repulsion between an electron on atom mu and one on atom lambda.] Expand both orbitals in atomic "
                 "orbitals and insert them into K a b: a quadruple sum.", m.FadeIn(d.rows[0]))
        self.say("[Zero differential overlap keeps only the terms with nu equal to mu and sigma equal to lambda: K becomes "
                 "a double sum of a mu b mu, times a lambda b lambda, times gamma.]", m.FadeIn(d.rows[1]))
        self.say("[If the orbitals are disjoint, the product a mu b mu vanishes on every atom, so every term vanishes and K "
                 "is zero.] Conversely, gamma is positive definite, so for nondisjoint orbitals K is strictly positive.",
                 m.FadeIn(d.rows[2]))
        self.say("[In the Hubbard model, where only on-site repulsion U survives, K is U times the sum over atoms of a "
                 "squared b squared.]", m.FadeIn(d.rows[3]))
        self.say("[Minimised over the choice of basis, that sum is one sixth for T M M and one sixteenth for meta xylylene; "
                 "our Python and JavaScript agree on both.]", m.FadeIn(nums))
        self.wait(0.4)


class S75GapTest(Frame):
    """11-nbmo.tex, frame 9: 'The test: how the gap grows with U'."""

    TITLE = "The test: how the gap grows with $U$"
    SUBTITLE = "T9b: exact Hubbard diagonalisation, $t=1$"
    SYMBOLS = (r"log–log axes: slope 1 means gap ∝ $U$, first order, $2K$; slope 2 means gap ∝ $U^2$, second order — "
               r"exact diagonalisation: all determinants of the Hubbard model, no approximation")

    def construct(self) -> None:
        self.setup_frame()
        with open(ROOT / "presentation" / "data" / "hubbard_gap.csv") as fh:
            rows = list(csv.DictReader(fh))
        U = np.array([float(r["U"]) for r in rows])
        col = {k: np.abs(np.array([float(r[k]) for r in rows])) for k in ("TMM", "MX", "CBD", "TME")}
        ax = Plot([0.04, 4.5], [10 ** -4.5, 1], 6.2, 4.2, xticks=[0.1, 1], yticks=[1e-4, 1e-3, 1e-2, 1e-1, 1],
                  log_x=True, log_y=True).move_to([-2.45, 0.35, 0])
        P = ax.c2p
        xl = rich("$U/t$", 24, MUTED).next_to(ax.x_axis, m.DOWN, buff=0.45)
        yl = rich("$|E_T-E_S|$", 24, MUTED).rotate(m.PI / 2).next_to(ax.y_axis, m.LEFT, buff=0.7)
        series, dots = {}, {}
        for k, c in (("TMM", ROSE), ("MX", ORANGE), ("CBD", CYAN), ("TME", GREEN)):
            pts_k = [P(u, g) for u, g in zip(U, col[k])]
            line = m.VMobject(stroke_color=c, stroke_width=4)
            line.set_points_as_corners(pts_k)
            series[k] = line
            dots[k] = m.VGroup(*[m.Dot(q, radius=0.045, color=c) for q in pts_k])
        names = {"TMM": "TMM (triplet)", "MX": "MX (triplet)", "CBD": "CBD (singlet)", "TME": "TME (singlet)"}
        legend = {k: m.VGroup(m.Line([0, 0, 0], [0.35, 0, 0], color=series[k].get_stroke_color(), stroke_width=4),
                              rich(names[k], 22)).arrange(m.RIGHT, buff=0.1) for k in series}
        leg = m.VGroup(*legend.values()).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.1)
        leg.arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.1), cell_alignment=m.LEFT, flow_order="dr")
        leg.move_to([3.75, -2.05, 0])
        pts = bullets([r"nondisjoint: slope ≈ 1; at $U=0.05$: TMM $0.0164$ vs $2U\cdot\tfrac16=0.0167$",
                       r"disjoint: slope ≈ 2 (fit $1.97$, $1.95$), singlet below triplet",
                       r"first-order $K$ vanishes; something second-order picks the singlet…"], width=5.4, size=27)
        pts.move_to([3.75, 0.3, 0])
        self.say("[Test T nine b checks all of this with exact diagonalisation of the Hubbard model, every determinant "
                 "and no approximation, at t equal to one. Both axes are logarithmic: the singlet-triplet gap against U "
                 "over t.] On log-log axes a slope of one means the gap grows like U, which is first order, two K; a "
                 "slope of two means it grows like U squared, which is second order.",
                 m.AnimationGroup(m.Create(ax), m.FadeIn(xl), m.FadeIn(yl)))
        self.say("[The nondisjoint molecules, T M M and meta xylylene, have triplet ground states, and their gaps rise with "
                 "slope about one.] [At U equal to zero point zero five, T M M's gap is zero point zero one six four, "
                 "against the first-order prediction two U times one sixth, zero point zero one six seven.]",
                 m.AnimationGroup(*[m.Create(series[k]) for k in ("TMM", "MX")],
                                  *[m.FadeIn(dots[k]) for k in ("TMM", "MX")],
                                  *[m.FadeIn(legend[k]) for k in ("TMM", "MX")]), m.FadeIn(pts[0]))
        self.say("[The disjoint molecules, cyclobutadiene and T M E, behave differently: their gaps rise with slope about "
                 "two, fitted at one point nine seven and one point nine five, and the singlet lies below the triplet.]",
                 m.AnimationGroup(*[m.Create(series[k]) for k in ("CBD", "TME")],
                                  *[m.FadeIn(dots[k]) for k in ("CBD", "TME")],
                                  *[m.FadeIn(legend[k]) for k in ("CBD", "TME")], m.FadeIn(pts[1])))
        self.say("[So the first-order exchange integral really does vanish for disjoint orbitals, and something at second "
                 "order picks the singlet. The next part finds out what.]", m.FadeIn(pts[2]))
        self.wait(0.4)
