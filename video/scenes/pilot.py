"""Pilot: slide 'The sum D_iii + D_iv, every term tracked' (presentation/sections/05-two-electrons.tex).

End-to-end test of the pipeline: theme, derivation rows revealed on the narration's words, coloured parts,
underbraces, a result box and the symbols strip.
"""
import manimgx as m

from noir import (CYAN, ROSE, Box, Derivation, Frame, M, X, paint_parts)


class SumTracked(Frame):
    TITLE = r"The sum $D_{\text{iii}}+D_{\text{iv}}$, every term tracked"
    SYMBOLS = (r"$A=\pa(1)\pb(2)$, $B=\pb(1)\pa(2)$ — $A-B$ changes sign under $1\leftrightarrow2$ (antisymmetric) — "
               r"$\Theta_{1,0}=\tfrac1{\sqrt2}(\alpha_1\beta_2+\beta_1\alpha_2)$: triplet, $M_S=0$")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"D_{\text{iii}}+D_{\text{iv}}",
             ["=", "A", r"\,\alpha_1\beta_2-", "B", r"\,\beta_1\alpha_2+", "A", r"\,\beta_1\alpha_2-", "B",
              r"\,\alpha_1\beta_2"], "rows iii, iv"),
            ("", ["=", "A", r"\,(\alpha_1\beta_2+\beta_1\alpha_2)-", "B", r"\,(\beta_1\alpha_2+\alpha_1\beta_2)"],
             "collect A, B"),
            ("", ["=(", "A", "-", "B", r")\,(\alpha_1\beta_2+\beta_1\alpha_2)"], "same bracket"),
            ("", [r"=\underbrace{\bigl[\pa(1)\pb(2)-\pb(1)\pa(2)\bigr]}_{\text{antisymmetric space}}"
                  r"\underbrace{(\alpha_1\beta_2+\beta_1\alpha_2)}_{\sqrt2\,\Theta_{1,0}}"], "put A, B back"),
        ], size=36)
        for row in d.rows:
            paint_parts(row[1], {"A": CYAN, "B": ROSE})
        d.next_to(self.title_group, m.DOWN, buff=0.45).set_x(0)
        result = Box(X(r"antisymmetric space $\times$ symmetric spin: the \emph{sum} is the $M_S=0$ triplet.", size=28),
                     kind="result")
        result.next_to(d, m.DOWN, buff=0.45)

        self.say("Now add the two determinants, keeping track of every term. Write A for phi a of electron one "
                 "times phi b of electron two, and B for the same product with the two electrons swapped.",
                 m.Indicate(self.strip, color=CYAN, scale_factor=1.02))
        self.say("Expanding determinants three and four gives four products: [A alpha one beta two, minus B beta "
                 "one alpha two, plus A beta one alpha two, minus B alpha one beta two.]",
                 m.Write(m.VGroup(d.rows[0][0], d.rows[0][1])))
        self.add(d.rows[0][2])
        self.say("[Collect the terms that multiply A, and the terms that multiply B.]",
                 m.AnimationGroup(m.FadeIn(d.rows[1][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[1][2])))
        self.say("Both brackets hold the same spin function, [so it factors out: A minus B, times alpha one beta "
                 "two plus beta one alpha two.]",
                 m.AnimationGroup(m.FadeIn(d.rows[2][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[2][2])))
        self.say("[Now put A and B back.] The spatial factor changes sign when the two electrons swap places, [so it "
                 "is antisymmetric.] The spin factor is root two times theta one zero, [the symmetric triplet "
                 "function with M S equal to zero.]",
                 m.AnimationGroup(m.FadeIn(d.rows[3][1], shift=m.RIGHT * 0.2), m.FadeIn(d.rows[3][2])),
                 m.Indicate(d.rows[3][1], color=ROSE, scale_factor=1.03),
                 m.Indicate(d.rows[3][1], color=CYAN, scale_factor=1.03))
        self.say("[An antisymmetric space times a symmetric spin is a triplet.] So the sum of determinants three "
                 "and four is the M S equals zero component of the triplet, not the open-shell singlet.",
                 m.FadeIn(result, shift=m.UP * 0.15))
        self.wait(0.5)
