"""Chapter 5: Fermi holes, K ≥ 0 and J ≥ K (presentation/sections/07-holes.tex)."""
import numpy as np

import manimgx as m

from ch01_foundations import explain
from noir import (BLUE, CYAN, FG, GOLD, GREEN, MUTED, ROSE, Box, Derivation, Frame, M, T, boxed, rich)

# the slides' pgfplots colour map "noirmap": black, deep blue, cyan, gold, white
_MAP = np.array([[0, 0, 0], [30, 60, 110], [95, 212, 208], [233, 185, 91], [255, 255, 255]], dtype=float)


def heatmap(values: np.ndarray) -> np.ndarray:
    """values in [0, max] -> RGBA image with the noirmap colour map (row 0 = top)."""
    v = values / values.max()
    x = np.clip(v, 0, 1) * (len(_MAP) - 1)
    i = np.minimum(x.astype(int), len(_MAP) - 2)
    f = (x - i)[..., None]
    rgb = _MAP[i] * (1 - f) + _MAP[i + 1] * f
    return np.dstack([rgb, np.full(v.shape, 255.0)]).astype(np.uint8)


def pair_density(sign: int, n: int = 360) -> np.ndarray:
    """P(x1, x2) = 4 [sin πx1 sin 2πx2 ± sin 2πx1 sin πx2]² on the unit square: orbitals √2 sin πx, √2 sin 2πx."""
    x = (np.arange(n) + 0.5) / n
    x1, x2 = np.meshgrid(x, x[::-1])  # rows: x2 from 1 (top) to 0 (bottom)
    return 4 * (np.sin(np.pi * x1) * np.sin(2 * np.pi * x2) + sign * np.sin(2 * np.pi * x1) * np.sin(np.pi * x2)) ** 2


class S39PairDensity(Frame):
    """07-holes.tex, frame 1: 'Where can the two electrons be?'."""

    TITLE = "Where can the two electrons be?"
    SUBTITLE = "the pair density"
    SYMBOLS = (r"$x_k=(\mathbf r_k,\sigma_k)$ — $\int\dd x$: integrate over position, sum over spin — $P_T$: pair density of "
               r"the triplet, $P_{\OSS}$: of the open-shell singlet — $[A-B]^2$ vanishes when $\mathbf r_1=\mathbf r_2$, "
               r"because then $A=B$")

    def construct(self) -> None:
        self.setup_frame()
        P = M(r"P(\mathbf r_1,\mathbf r_2)=N(N-1)\sum_{\sigma_1\sigma_2}\int|\Psi|^2\,\dd x_3\cdots\dd x_N", size=34)
        e1 = explain("probability density for “one electron at r1 and another at r2”", width=6.8)
        two = rich("two electrons, spin summed:", 30)
        d = Derivation([(r"P_T", r"=\bigl[\pa(1)\pb(2)-\pb(1)\pa(2)\bigr]^2", ""),
                        (r"P_{\OSS}", r"=\bigl[\pa(1)\pb(2)+\pb(1)\pa(2)\bigr]^2", "")], size=34)
        e2 = explain(r"$N(N-1)=2$ cancels the $(\tfrac1{\sqrt2})^2$; the spin sum gives $\sum|\Theta|^2=1$", width=6.8)
        same = rich(r"set $\mathbf r_1=\mathbf r_2=\mathbf r$: $\quad P_T(\mathbf r,\mathbf r)=0,\quad P_{\OSS}(\mathbf r,"
                    r"\mathbf r)=4\pa^2\pb^2$", 30, width=7.0)
        left = m.VGroup(P, e1, two, d, e2, same).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.24).move_to([-3.0, 0.1, 0])
        res = boxed("in the triplet the two electrons are never at the same point, for every $M_S$; exact, no "
                    "approximation beyond the form of Ψ", "result", width=5.6, size=28, tag="Fermi hole")
        coul = rich("The Coulomb hole, caused by $1/r_{12}$ itself, is absent here: it needs correlation beyond one "
                    "configuration — dynamic correlation, review p. 442.", 26, MUTED, width=5.5)
        right = m.VGroup(res, coul).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.4).move_to([3.85, 0.3, 0])
        self.say("[Where can the two electrons be? The pair density, P of r one and r two, is the probability density "
                 "of finding one electron at r one and another at r two. It is N times N minus one, times the "
                 "wavefunction squared, summed over the spins and integrated over all the other electrons.]",
                 m.AnimationGroup(m.FadeIn(P), m.FadeIn(e1)))
        self.say("[For our two electrons, after summing over spin, the triplet's pair density is the square of the "
                 "antisymmetric spatial function, A minus B.] [The open-shell singlet's is the square of A plus B.]",
                 m.AnimationGroup(m.FadeIn(two), m.FadeIn(d.rows[0])), m.FadeIn(d.rows[1]))
        self.say("[The prefactors cancel: N times N minus one is two, which cancels the one half from normalisation, and "
                 "the spin functions are normalised, so their sum over spins gives one.]", m.FadeIn(e2))
        self.say("[Now put both electrons at the same point. A and B become equal, so the triplet's pair density is "
                 "exactly zero, while the singlet's is four phi a squared phi b squared.]", m.FadeIn(same))
        self.say("[This is the Fermi hole: in the triplet, the two electrons are never found at the same point, for "
                 "every M S. It is exact, with no approximation beyond the form of the wavefunction.]", m.FadeIn(res))
        self.say("[The Coulomb hole, caused by the repulsion itself, is absent at this level. It needs correlation "
                 "beyond a single configuration, which the review calls dynamic correlation.]", m.FadeIn(coul))
        self.wait(0.4)


class S40SeeFermiHole(Frame):
    """07-holes.tex, frame 2: 'Seeing the Fermi hole'."""

    TITLE = "Seeing the Fermi hole"
    SUBTITLE = r"two electrons in a one-dimensional box, orbitals $\sin\pi x$ and $\sin2\pi x$"
    SYMBOLS = (r"box orbitals $\pa=\sqrt2\sin\pi x$, $\pb=\sqrt2\sin2\pi x$ on $0\le x\le1$, normalised; prefactor "
               r"$(\sqrt2)^4=4$ — colour: the probability density of electron 1 at $x_1$ and electron 2 at $x_2$, black "
               r"zero, white high")

    def construct(self) -> None:
        self.setup_frame()
        size = 3.9
        panels = []
        for k, (sign, name, col, x) in enumerate([(-1, "triplet", ROSE, -3.0), (+1, "singlet", BLUE, 3.0)]):
            img = m.ImageMobject(heatmap(pair_density(sign)))
            img.height = size
            img.move_to([x, 0.1, 0])
            frame = m.Square(side_length=size, stroke_color=MUTED, stroke_width=1.5).move_to(img)
            diag = m.DashedLine(img.get_corner(m.DL), img.get_corner(m.UR), color=ROSE if sign < 0 else MUTED,
                                stroke_width=3)
            title = rich(f"{name} " + (r"$P_T(x_1,x_2)$" if sign < 0 else r"$P_{\OSS}(x_1,x_2)$"), 30, col)
            title.next_to(frame, m.UP, buff=0.15)
            xl = M("x_1", size=30, color=MUTED).next_to(frame, m.DOWN, buff=0.12)
            yl = M("x_2", size=30, color=MUTED).next_to(frame, m.LEFT, buff=0.12)
            ticks = m.VGroup(M("0", size=24, color=MUTED).next_to(frame.get_corner(m.DL), m.DL, buff=0.05),
                             M("1", size=24, color=MUTED).next_to(frame.get_corner(m.DR), m.DOWN, buff=0.08),
                             M("1", size=24, color=MUTED).next_to(frame.get_corner(m.UL), m.LEFT, buff=0.08))
            panels.append(m.Group(img, frame, diag, title, xl, yl, ticks))
        note = rich("dashed line $x_1=x_2$: dark all along for the triplet, bright for the singlet", 30, width=12)
        note.move_to([0, -2.45, 0])
        self.say("[To see the Fermi hole, put two electrons in a one-dimensional box, in the two lowest orbitals, root "
                 "two sine pi x and root two sine two pi x. Here is the triplet's pair density: the brightness at each "
                 "point is the probability of finding electron one at x one and electron two at x two.]",
                 m.FadeIn(panels[0]))
        self.say("[Along the dashed diagonal, where x one equals x two, it is dark all the way: the two electrons are "
                 "never at the same place.]", m.Indicate(panels[0][2], color=ROSE))
        self.say("[The open-shell singlet is different. Its pair density is bright along the diagonal: the two "
                 "electrons are often found together.]", m.FadeIn(panels[1]))
        self.say("[So for the same two orbitals, the triplet keeps its electrons apart and the singlet does not. That is "
                 "why the triplet's electron repulsion carries a minus K.]", m.FadeIn(note))
        self.wait(0.4)


class S41KPositive(Frame):
    """07-holes.tex, frame 3: 'K_ab ≥ 0: a three-line proof'."""

    TITLE = r"$K_{ab}\ge0$: a three-line proof"
    SYMBOLS = (r"$\rho=\pa\pb$: overlap density, which integrates to 0 but is not zero point by point — $\mathbf k$: wave "
               r"vector, $k=|\mathbf k|$ — $\tilde\rho(\mathbf k)=\int\rho(\mathbf r)e^{-i\mathbf k\cdot\mathbf r}\dd\mathbf r$: "
               r"Fourier transform — $|z|^2=z^*z$")

    def construct(self) -> None:
        self.setup_frame()
        top = rich(r"overlap density $\rho(\mathbf r)=\pa(\mathbf r)\pb(\mathbf r)$, real $\Rightarrow$ "
                   r"$K_{ab}=\iint\frac{\rho(1)\rho(2)}{r_{12}}$", 32).move_to([0, 2.15, 0])
        d = Derivation([
            (r"\text{(1)}\ \frac1{|\mathbf r|}", r"=\int\frac{\dd^3k}{(2\pi)^3}\,\frac{4\pi}{k^2}\,e^{i\mathbf k\cdot\mathbf r}",
             r"$1/r$ as a sum of plane waves, all with positive weight $4\pi/k^2$"),
            (r"\text{(2)}\ K_{ab}", r"=\int\frac{\dd^3k}{(2\pi)^3}\frac{4\pi}{k^2}\underbrace{\Bigl(\int\rho\,e^{i\mathbf k\cdot\mathbf r_1}"
             r"\Bigr)}_{\tilde\rho(\mathbf k)^*}\underbrace{\Bigl(\int\rho\,e^{-i\mathbf k\cdot\mathbf r_2}\Bigr)}_{\tilde\rho(\mathbf k)}",
             r"insert with $\mathbf r=\mathbf r_1-\mathbf r_2$; the integrals separate"),
            (r"\text{(3)}", r"=\int\frac{\dd^3k}{(2\pi)^3}\,\frac{4\pi}{k^2}\,|\tilde\rho(\mathbf k)|^2\ \ge0",
             r"$\rho$ real, so the factors are complex conjugates"),
        ], size=32, why_size=24, why_gap=0.35).move_to([0, 0.05, 0])
        e = explain("a positive weight times a square, integrated: it can never be negative", width=11).move_to([0, -1.95, 0])
        eq = rich(r"equality iff $\pa\pb\equiv0$, no common region of space: this returns as disjointness", 30, GOLD,
                  width=12).move_to([0, -2.55, 0])
        self.say("[Now prove that K is never negative. Define the overlap density rho as phi a times phi b, which is real. "
                 "Then K is the self repulsion of rho: the double integral of rho at one point times rho at another, "
                 "over their distance.]", m.FadeIn(top))
        self.say("[Step one. Write one over r as a sum of plane waves: an integral over all wave vectors k of four pi "
                 "over k squared times e to the i k dot r.] Every plane wave enters with a positive weight.",
                 m.FadeIn(d.rows[0]))
        self.say("[Step two. Insert this with r equal to r one minus r two. The exponential splits into a factor for "
                 "electron one and a factor for electron two, so the two spatial integrals separate. They are the "
                 "Fourier transform of rho and its complex conjugate.]", m.FadeIn(d.rows[1]))
        self.say("[Step three. Because rho is real, the two factors are complex conjugates, and their product is the "
                 "squared modulus of the Fourier transform.]", m.FadeIn(d.rows[2]))
        self.say("[So K is a positive weight times a square, integrated: it can never be negative.]", m.FadeIn(e))
        self.say("[It is zero only if phi a times phi b vanishes everywhere, meaning the two orbitals share no region of "
                 "space.] That idea returns later as disjointness.", m.FadeIn(eq))
        self.wait(0.4)


class S42JgeK(Frame):
    """07-holes.tex, frame 4: 'J_ab ≥ K_ab'."""

    TITLE = r"$J_{ab}\ge K_{ab}$"
    SYMBOLS = (r"$\iint A^2/r_{12}=\iint B^2/r_{12}=J_{ab}$ and $\iint AB/r_{12}=K_{ab}$, the same integrals as in Part V — "
               r"RHF/6-31G: Hartree–Fock orbitals in a standard Gaussian basis")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\text{(1)}\ f", r"=\pa(1)\pb(2)-\pb(1)\pa(2)", r"$=A-B$"),
            (r"\text{(2)}\ 0", r"\le\iint\frac{f^2}{r_{12}}", r"$f^2\ge0$ and $1/r_{12}>0$"),
            ("", r"=J_{ab}+J_{ab}-K_{ab}-K_{ab}", r"$f^2=A^2+B^2-2AB$"),
            ("", r"=2(J_{ab}-K_{ab})", ""),
        ], size=38).move_to([-2.4, 0.9, 0])
        box = M(r"\boxed{\,J_{ab}\ge K_{ab}\ge0\,}", size=46, color=GREEN).move_to([-2.4, -1.15, 0])
        e = explain(r"so the triplet's repulsion $J-K$ is never negative, and lies below the singlet's $J+K$", width=7.4)
        e.next_to(box, m.DOWN, buff=0.3)
        chk = boxed(r"all canonical RHF/6-31G orbitals of H$_2$O: $\min K_{pq}=1.1\times10^{-3}\,\Eh>0$ and $J_{pq}\ge K_{pq}$ "
                    r"for every pair", "checked", width=4.6, size=28, tag="T3").move_to([4.35, 0.75, 0])
        so = rich(r"so $E_T=h_a+h_b+J-K$ really is the lower of the two.", 30, width=4.4).next_to(chk, m.DOWN, buff=0.4)
        self.say("[One more inequality. Take f to be the antisymmetric function A minus B.]", m.FadeIn(d.rows[0]))
        self.say("[Its square is never negative and one over r one two is positive, so the integral of f squared over r "
                 "one two is at least zero.]", m.FadeIn(d.rows[1]))
        self.say("[Expand f squared as A squared plus B squared minus two A B. The A squared and B squared integrals are "
                 "each J, and the A B integral is K, so the result is J plus J minus K minus K,] [which is two times J "
                 "minus K.]", m.FadeIn(d.rows[2]), m.FadeIn(d.rows[3]))
        self.say("[So J a b is at least K a b, which is at least zero.]", m.Write(box))
        self.say("[The triplet's repulsion, J minus K, is never negative, and it lies below the singlet's J plus K.]",
                 m.FadeIn(e))
        self.say("[Test T three checked this on real molecular orbitals: for every pair of canonical Hartree Fock "
                 "orbitals of water in the six thirty one G basis, the smallest K is one point one times ten to the "
                 "minus three hartree, positive, and J is at least K for every pair.]", m.FadeIn(chk))
        self.say("[So with frozen orbitals, the triplet energy really is the lower of the two.]", m.FadeIn(so))
        self.wait(0.4)
