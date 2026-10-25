"""Chapter 15: broken symmetry and spin projection (presentation/sections/17-bs.tex)."""
import csv

import manimgx as m

from ch01_foundations import explain
from noir import (CYAN, FG, GOLD, GREEN, MUTED, ROSE, ROOT, Box, Derivation, Frame, M, Plot, boxed, bullets, curve,
                  pill, rich)


class S120Cheap(Frame):
    """17-bs.tex, frame 1: 'Cheap methods for diradicals'."""

    TITLE = "Cheap methods for diradicals"
    SYMBOLS = (r"BS: broken symmetry, $\alpha$ and $\beta$ electrons in different spatial orbitals — $\bar b'$: $b'$ with "
               r"$\beta$ spin — $S_z$: total $M_S$ — $N_\beta$: number of $\beta$ electrons")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"relatively \'cheap\' methods such as unrestricted or broken symmetry formalisms suffer from a number '
                      'of serious drawbacks" — p. 443; rigorous methods are too costly for large systems', "claim",
                      width=12.6, size=28).move_to([0, 1.95, 0])
        bs = rich(r"BS determinant $\ket{a'\bar b'}$: $a'$ on $l$, $b'$ on $r$, $s=\braket{a'}{b'}$", 29).move_to([-2.9, 0.85, 0])
        d = Derivation([
            (r"\ev{\hat S^2}_{\text{UHF}}", r"=S_z(S_z+1)+N_\beta-\textstyle\sum_{i\alpha,j\beta}|\braket ij|^2", ""),
            (r"\ev{\hat S^2}_{\text{BS}}", r"=0+1-s^2", ""),
        ], size=34).next_to(bs, m.DOWN, buff=0.35).align_to(bs, m.LEFT)
        e = explain(r"exact for a determinant; BS: $S_z=0$, $N_\beta=1$, one overlap $s$", width=6.6)
        e.next_to(d, m.DOWN, buff=0.25).align_to(bs, m.LEFT)
        lim = m.VGroup(rich(r"$s=1$: closed shell, $\ev{\hat S^2}=0$", 28),
                       rich(r"$s=0$: half singlet, half triplet, $\ev{\hat S^2}=1$", 28)).arrange(m.DOWN, aligned_edge=m.LEFT,
                                                                                               buff=0.2)
        lim.move_to([3.95, 0.3, 0])
        part = rich("**a single determinant cannot be the open-shell singlet**, Part III", 28, GOLD, width=5.4)
        part.next_to(lim, m.DOWN, buff=0.45).align_to(lim, m.LEFT)
        self.say("[Part sixteen: broken symmetry. The review says that relatively cheap methods, such as unrestricted or "
                 "broken-symmetry formalisms, suffer from a number of serious drawbacks, while rigorous methods are too "
                 "costly for large systems.]", m.FadeIn(claim))
        self.say("[A broken-symmetry determinant puts the alpha electron in an orbital a prime on the left centre and the "
                 "beta electron in b prime on the right, with overlap s.]", m.FadeIn(bs))
        self.say("[For any unrestricted determinant, the expectation value of S squared is S z times S z plus one, plus the "
                 "number of beta electrons, minus the sum of squared overlaps between alpha and beta orbitals.]",
                 m.FadeIn(d.rows[0]))
        self.say("[For the broken-symmetry determinant, S z is zero, there is one beta electron, and one overlap s: the "
                 "result is one minus s squared.] This formula is exact for a determinant.",
                 m.AnimationGroup(m.FadeIn(d.rows[1]), m.FadeIn(e)))
        self.say("[If s is one, the two orbitals coincide: a closed shell, with S squared zero. If s is zero, the "
                 "determinant is half singlet and half triplet, with S squared one.]", m.FadeIn(lim))
        self.say("[As Part three showed, a single determinant cannot be the open-shell singlet.]", m.FadeIn(part))
        self.wait(0.4)


class S121Yamaguchi(Frame):
    """17-bs.tex, frame 2: 'Yamaguchi's projection, derived'."""

    TITLE = "Yamaguchi's projection, derived"
    SYMBOLS = (r"Heisenberg model: spins only, coupling $J$ — $\hat{\mathbf S}_1,\hat{\mathbf S}_2$: spin-½ operators of the "
               r"two centres — $c_S,c_T$: amplitudes, $|c_S|^2+|c_T|^2=1$ — HS: high-spin determinant, an exact triplet")

    def construct(self) -> None:
        self.setup_frame()
        assume = boxed(r"two-centre Heisenberg model $\hat H=-2J\,\hat{\mathbf S}_1\cdot\hat{\mathbf S}_2$; BS state "
                       r"$=c_S\Psi_S+c_T\Psi_T$, $M_S=0$", "assume", width=12.6, size=28).move_to([0, 2.05, 0])
        d = Derivation([
            (r"\stepno{1}\ \hat{\mathbf S}_1\cdot\hat{\mathbf S}_2", r"=\tfrac12\bigl[S(S+1)-\tfrac32\bigr]\ \Rightarrow\ "
             r"E_T=-\tfrac J2,\ E_S=\tfrac{3J}2", r"$\hat S^2=\hat S_1^2+\hat S_2^2+2\hat{\mathbf S}_1\cdot\hat{\mathbf S}_2$, "
             r"$\hat S_i^2=\tfrac34$"),
            (r"\stepno{2}\ \ev{\hat S^2}_{\text{BS}}", r"=2|c_T|^2,\qquad E_{\text{BS}}=|c_S|^2E_S+|c_T|^2E_T",
             r"$S^2$: 0 and 2; no cross terms"),
            (r"\stepno{3}\ E_{\text{BS}}-E_T", r"=|c_S|^2(E_S-E_T)=\bigl(1-\tfrac12\ev{\hat S^2}_{\text{BS}}\bigr)2J",
             r"$|c_T|^2=1-|c_S|^2$; $E_S-E_T=2J$"),
            (r"\stepno{4}\ J", r"=\dfrac{E_{\text{BS}}-E_{\text{HS}}}{\ev{\hat S^2}_{\text{HS}}-\ev{\hat S^2}_{\text{BS}}}",
             r"solve for $J$; HS = triplet, $\ev{\hat S^2}_{\text{HS}}=2$"),
        ], size=30, why_size=22).move_to([0, -0.1, 0])
        note = rich("Lean: `yamaguchi`; sign conventions differ between sources, here $J<0$ is antiferromagnetic", 25,
                    MUTED).move_to([0, -2.4, 0])
        self.say("[How do broken-symmetry calculations still give couplings? Through Yamaguchi's projection, which we "
                 "derive. Assume the two-centre Heisenberg model, minus two J times S one dot S two, and write the "
                 "broken-symmetry state as a mixture of the singlet and the M S zero triplet.]", m.FadeIn(assume))
        self.say("[Step one. Since S squared is S one squared plus S two squared plus twice S one dot S two, and each S i "
                 "squared is three quarters, S one dot S two is one half of S times S plus one, minus three halves. So "
                 "the triplet energy is minus J over two and the singlet energy three J over two.]", m.FadeIn(d.rows[0]))
        self.say("[Step two. S squared is zero in the singlet and two in the triplet, and the two states do not mix under "
                 "either operator, so the broken-symmetry state has S squared equal to two c T squared, and energy c S "
                 "squared E S plus c T squared E T.]", m.FadeIn(d.rows[1]))
        self.say("[Step three. Subtract the triplet energy: c S squared times E S minus E T. With c T squared equal to one "
                 "minus c S squared, and E S minus E T equal to two J, this is one minus half the broken-symmetry S "
                 "squared, times two J.]", m.FadeIn(d.rows[2]))
        self.say("[Step four. Solve for J: the energy difference between the broken-symmetry and high-spin "
                 "determinants, divided by the difference of their S squared values, two for the high-spin triplet.]",
                 m.FadeIn(d.rows[3]))
        self.say("[Our Lean file proves this as the theorem yamaguchi. Sign conventions differ between sources; here a "
                 "negative J means antiferromagnetic coupling.]", m.FadeIn(note))
        self.wait(0.4)


class S122HowGood(Frame):
    """17-bs.tex, frame 3: 'How good is it? The Hubbard dimer'."""

    TITLE = "How good is it? The Hubbard dimer"
    SUBTITLE = "T14: self-consistent BS-UHF vs the exact singlet–triplet gap"
    SYMBOLS = (r"$U$: on-site repulsion — $t$: hopping — exact $J=\tfrac12(E_S-E_T)$ from the Hubbard dimer, Part VI — "
               r"weakly coupled: large $U/t$, electrons localised on their centres — covalent: small $U/t$, a real bond")

    def construct(self) -> None:
        self.setup_frame()
        with open(ROOT / "presentation" / "data" / "yamaguchi.csv") as fh:
            rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(fh)]
        U = [r["U"] for r in rows]
        ax = Plot([2, 16], [-0.62, 0], 6.2, 4.0, xticks=[2, 4, 6, 8, 10, 12, 14, 16],
                  yticks=[-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0], yfmt="{:.1f}", grid=False).move_to([-2.7, 0.25, 0])
        xl = rich("$U/t$", 24, MUTED).next_to(ax.x_axis, m.DOWN, buff=0.45)
        yl = rich("$J/t$", 24, MUTED).next_to(ax.y_axis, m.UP, buff=0.12)
        exact = curve(ax, U, [r["Jexact"] for r in rows], CYAN)
        yam = curve(ax, U, [r["Jyam"] for r in rows], GOLD, dashed=True)
        leg = m.VGroup(m.VGroup(m.Line([0, 0, 0], [0.4, 0, 0], color=CYAN, stroke_width=4),
                                rich(r"exact $\tfrac14(U-\sqrt{U^2+16t^2})$", 23)).arrange(m.RIGHT, buff=0.1),
                       m.VGroup(m.DashedLine([0, 0, 0], [0.4, 0, 0], color=GOLD, stroke_width=4),
                                rich("Yamaguchi from BS-UHF", 23)).arrange(m.RIGHT, buff=0.1))
        leg.arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.1).move_to(ax.c2p(11.2, -0.47))
        pts = bullets([r"$U=3t$: error $-7.7\%$", r"$U=12t$: $-0.1\%$",
                       r"good when the centres are weakly coupled, $\ev{\hat S^2}_{\text{BS}}\to1$; poor when covalent"],
                      width=5.0, size=28).move_to([4.15, 0.8, 0])
        ok = m.VGroup(pill("verified"), rich("“serious drawbacks” is fair", 27)).arrange(m.RIGHT, buff=0.2)
        ok.next_to(pts, m.DOWN, buff=0.4).align_to(pts, m.LEFT)
        self.say("[How good is the projection? Test T fourteen compares it with the exact answer for the Hubbard dimer. "
                 "The exact coupling, one half of E S minus E T, is one quarter of U minus the square root of U squared "
                 "plus sixteen t squared.]",
                 m.AnimationGroup(m.Create(ax), m.FadeIn(xl), m.FadeIn(yl), m.Create(exact), m.FadeIn(leg[0])))
        self.say("[The dashed curve is Yamaguchi's formula applied to self-consistent broken-symmetry unrestricted Hartree "
                 "Fock. At U equal to three t, it underestimates the coupling by seven point seven percent.]",
                 m.AnimationGroup(m.Create(yam), m.FadeIn(leg[1]), m.FadeIn(pts[0])))
        self.say("[At U equal to twelve t, the error is only a tenth of a percent.]", m.FadeIn(pts[1]))
        self.say("[So the projection is good when the centres are weakly coupled, with the broken-symmetry S squared near "
                 "one, and poor when the bond is covalent.]", m.FadeIn(pts[2]))
        self.say("[The review's serious drawbacks is a fair description.]", m.FadeIn(ok))
        self.wait(0.4)
