"""Chapter 17: verdict, take-home, references (presentation/sections/19-verdict.tex)."""
import manimgx as m

from noir import (CYAN, FG, GOLD, GREEN, MUTED, ORANGE, ROSE, Box, Frame, M, boxed, pill, rich)


def scorecard(rows: list[tuple[str, list[str]]], size: float = 27) -> m.VGroup:
    """Claim | verdict pills, with a header rule; returns the rows, header first."""
    head = m.VGroup(rich("**claim**", size, GOLD), rich("**verdict**", size, GOLD))
    body = [m.VGroup(rich(c, size, width=8.8), m.VGroup(*[pill(p, size=26) for p in ps]).arrange(m.RIGHT, buff=0.12))
            for c, ps in rows]
    y = 2.0
    out = []
    for row in [head, *body]:
        h = max(row[0].height, row[1].height)
        row[0].move_to([-5.9 + row[0].width / 2, y - h / 2, 0])
        row[1].move_to([3.6 + row[1].width / 2, y - h / 2, 0])
        out.append(row)
        y -= h + 0.22
    rule = m.Line([-5.9, out[0].get_bottom()[1] - 0.1, 0], [6.2, out[0].get_bottom()[1] - 0.1, 0], color=MUTED,
                  stroke_width=1.5)
    out[0].add(rule)
    return m.VGroup(*out)


class S130Confirmed(Frame):
    """19-verdict.tex, frame 1: 'Scorecard (1/2): confirmed'."""

    TITLE = "Scorecard, part 1: confirmed"

    def construct(self) -> None:
        self.setup_frame()
        g = scorecard([("triplet single-, open-shell singlet multi-reference", ["verified"]),
                       ("less screening, not lower $V_{ee}$, explains Hund's rule", ["verified"]),
                       ("static correlation grows as orbital interaction weakens", ["verified"]),
                       ("kinetic exchange; disjoint NBMOs; topology / Ovchinnikov rules", ["verified"]),
                       ("3d/4s; one-electron quantum numbers not conserved", ["verified"]),
                       ("ROHF orbital energies are convention-dependent", ["verified", "overstated"])])
        self.say("[Part eighteen: the verdict. First, what we confirmed. The triplet is single-reference and the open-"
                 "shell singlet multi-reference.]", m.AnimationGroup(m.FadeIn(g[0]), m.FadeIn(g[1])))
        self.say("[Less screening, not a lower electron repulsion, explains Hund's rule.]", m.FadeIn(g[2]))
        self.say("[Static correlation grows as the interaction between the orbitals weakens.]", m.FadeIn(g[3]))
        self.say("[Kinetic exchange, the disjoint non-bonding orbitals, and the topology rules of Ovchinnikov.]",
                 m.FadeIn(g[4]))
        self.say("[The three d four s argument, and the non-conservation of one-electron quantum numbers.]",
                 m.FadeIn(g[5]))
        self.say("[And restricted open-shell orbital energies do depend on a convention, although the practical danger is "
                 "overstated.]", m.FadeIn(g[6]))
        self.wait(0.4)


class S131Qualified(Frame):
    """19-verdict.tex, frame 2: 'Scorecard (2/2): qualified or wrong'."""

    TITLE = "Scorecard, part 2: qualified or wrong"

    def construct(self) -> None:
        self.setup_frame()
        g = scorecard([("distonic anions oxidise to diradicals, switchable by pH", ["partial"]),
                       ("same-spin correlation “an order of magnitude” smaller", ["overstated"]),
                       ("aufbau “violates” Pauli; “the obsolescence of” aufbau and Hund's rule", ["overstated"]),
                       (r"$^1\Psi_{\OSS}=\tfrac12(D_{\text{iii}}+D_{\text{iv}})$, p. 441", ["error"]),
                       ("Katriel & Pauncz cited as 1975, it is 1977", ["error"]),
                       ("TriMB called a “triplet” ground state, three unpaired electrons: a quartet", ["imprecise"])])
        self.say("[Now what we qualified or found wrong. The distonic anions oxidise to diradicals, switchable by pH: "
                 "partially confirmed, because it depends on the functional.]",
                 m.AnimationGroup(m.FadeIn(g[0]), m.FadeIn(g[1])))
        self.say("[Same-spin correlation an order of magnitude smaller: overstated, true only for compact two-electron "
                 "systems.]", m.FadeIn(g[2]))
        self.say("[Aufbau violates Pauli, and the obsolescence of aufbau and Hund's rule: overstated.]", m.FadeIn(g[3]))
        self.say("[The open-shell singlet written as one half of D three plus D four, on page four hundred and forty one: "
                 "an error. That is the triplet.]", m.FadeIn(g[4]))
        self.say("[Katriel and Pauncz cited as nineteen seventy five, when it is nineteen seventy seven: an error.]",
                 m.FadeIn(g[5]))
        self.say("[And trimethylenebenzene called a triplet ground state, when three unpaired electrons give a quartet: "
                 "imprecise.]", m.FadeIn(g[6]))
        self.wait(0.4)


class S132Errors(Frame):
    """19-verdict.tex, frame 3: 'The errors, once more'."""

    TITLE = "The errors, once more"

    def construct(self) -> None:
        self.setup_frame()
        e1 = boxed(r"$\tfrac12(D_{\text{iii}}\ +\ D_{\text{iv}})$ is the $M_S=0$ triplet; the open-shell singlet is "
                   r"$\tfrac12(D_{\text{iv}}\ -\ D_{\text{iii}})$", "erratum", width=5.9, size=28,
                   tag="Sign error, p. 441").move_to([-3.25, 1.15, 0])
        e2 = boxed(r"Katriel & Pauncz, *Adv. Quantum Chem.* 10, 143 is from 1977", "erratum", width=5.9, size=28,
                   tag="Citation, ref. 11").next_to(e1, m.DOWN, buff=0.4)
        e3 = boxed('"triplet ground state, predicted on the basis of disjoint NBMOs" contradicts the review\'s own '
                   'disjoint/nondisjoint rule', "claim", width=5.9, size=28, tag="Possible slip, p. 445")
        e3.move_to([3.25, 1.15, 0])
        note = rich("these errata do not change the review's chemistry; but its distonic pH switch we reproduce only with "
                    "CAM-B3LYP", 27, width=5.9).next_to(e3, m.DOWN, buff=0.4)
        self.say("[The errors, once more. The sign error on page four hundred and forty one: one half of D three plus D "
                 "four is the M S zero triplet; the open-shell singlet is one half of D four minus D three.]",
                 m.FadeIn(e1))
        self.say("[The citation, reference eleven: Katriel and Pauncz, Advances in Quantum Chemistry volume ten, page one "
                 "hundred and forty three, is from nineteen seventy seven.]", m.FadeIn(e2))
        self.say("[A possible slip on page four hundred and forty five: a triplet ground state predicted on the basis of "
                 "disjoint orbitals contradicts the review's own rule.]", m.FadeIn(e3))
        self.say("[None of these changes the review's chemistry. But its distonic pH switch we reproduce only with the "
                 "range-separated functional.]", m.FadeIn(note))
        self.wait(0.4)


class S133TakeHome(Frame):
    """19-verdict.tex, frame 4: 'Take-home'."""

    TITLE = "Take-home"

    def construct(self) -> None:
        self.setup_frame()
        items = [r"1. a spin state is decided by **correlation**, not by a single term: Hund's rule, aufbau and topology "
                 r"rules are derived within *models*: orbital, Hückel, Hubbard",
                 r"2. the **virial theorem** plus the computed $\Delta V_{ee}>0$ explain Hund's rule in He: the high-spin "
                 r"state wins on nuclear attraction",
                 r"3. **disjointness** removes first-order exchange; second-order spin polarisation then picks the singlet",
                 r"4. **orbital energies are not observables**: judge non-aufbau claims by redox energetics",
                 r"5. distonic radical anions **do** oxidise to diradicals at CAM-B3LYP, *but* B3LYP misses by "
                 r"0.06–0.07 eV: a functional-sensitive claim"]
        lst = m.VGroup(*[rich(t, 29, width=12.4) for t in items]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.26)
        lst.move_to([0, 0.55, 0])
        last = rich("Even the open-shell singlet in print can fluctuate.", 46, GOLD, font="TeX Gyre Chorus")
        last.move_to([0, -2.45, 0])
        self.say("[What to take home. First: a spin state is decided by correlation, not by any single term. Hund's rule, "
                 "aufbau and the topology rules are all derived within models: the orbital model, Hückel theory, the "
                 "Hubbard model.]", m.FadeIn(lst[0]))
        self.say("[Second: the virial theorem, together with the computed increase in electron repulsion, explains Hund's "
                 "rule in helium. The high-spin state wins on nuclear attraction.]", m.FadeIn(lst[1]))
        self.say("[Third: disjointness removes first-order exchange, and second-order spin polarisation then picks the "
                 "singlet.]", m.FadeIn(lst[2]))
        self.say("[Fourth: orbital energies are not observables, so judge non-aufbau claims by redox energetics.]",
                 m.FadeIn(lst[3]))
        self.say("[Fifth: distonic radical anions do oxidise to diradicals with CAM B three L Y P, but B three L Y P misses by six to "
                 "seven hundredths of an electron volt. The claim is sensitive to the functional.]", m.FadeIn(lst[4]))
        self.say("[And one last lesson: even the open-shell singlet in print can fluctuate.]", m.Write(last))
        self.wait(0.6)


REFS = [r"G. Gryn'ova, M. L. Coote, C. Corminboeuf, *WIREs Comput. Mol. Sci.* **5**, 440, 2015",
        r"K. Hongo et al., *J. Chem. Phys.* **121**, 7144, 2004 — carbon, QMC, less screening",
        r"R. J. Boyd, *Nature* **310**, 480, 1984",
        r"J. Katriel, R. Pauncz, *Adv. Quantum Chem.* **10**, 143, 1977",
        r"W. T. Borden, E. R. Davidson, *J. Am. Chem. Soc.* **99**, 4587, 1977",
        r"A. A. Ovchinnikov, *Theor. Chim. Acta* **47**, 297, 1978",
        r"E. H. Lieb, *Phys. Rev. Lett.* **62**, 1201, 1989",
        r"J. F. Janak, *Phys. Rev. B* **18**, 7165, 1978",
        r"A. I. Krylov, *Chem. Phys. Lett.* **338**, 375, 2001",
        r"A. Balková, R. J. Bartlett, *J. Chem. Phys.* **101**, 8972, 1994",
        r"K. R. Glaesemann, M. W. Schmidt, *J. Phys. Chem. A* **114**, 8772, 2010",
        r"G. Gryn'ova, D. L. Marshall, S. J. Blanksby, M. L. Coote, *Nat. Chem.* **5**, 474, 2013"]


class S134References(Frame):
    """19-verdict.tex, frame 5: 'Key references'."""

    TITLE = "Key references"

    def construct(self) -> None:
        self.setup_frame()
        lst = m.VGroup(*[rich(r, 25) for r in REFS]).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.12)
        lst.move_to([0, 0.15, 0])
        note = rich("full access status of every source: derivations, §17", 24, MUTED).next_to(lst, m.DOWN, buff=0.25)
        self.say("[The key references: the review itself, by Gryn'ova, Coote and Corminboeuf, in WIREs Computational "
                 "Molecular Science, twenty fifteen; Hongo and coworkers on carbon; Boyd in Nature; Katriel and Pauncz; "
                 "Borden and Davidson; Ovchinnikov; Lieb; Janak; Krylov; Balková and Bartlett; Glaesemann and Schmidt; "
                 "and Gryn'ova, Marshall, Blanksby and Coote in Nature Chemistry.]", m.FadeIn(lst))
        self.say("[The access status of every source is listed in section seventeen of the derivations.]", m.FadeIn(note))
        self.wait(0.5)


class S135ThankYou(Frame):
    """19-verdict.tex, frame 6: the closing slide."""

    TITLE = ""

    def construct(self) -> None:
        thanks = rich("Thank you", 96, GOLD, font="TeX Gyre Chorus").move_to([0, 0.7, 0])
        what = rich("derivations • code • proofs • slides • video", 34, FG, font="EB Garamond").next_to(thanks, m.DOWN, buff=0.5)
        url = rich("`github.com/Shuvam-Banerji-Seal/CH5103_Term_Paper`", 28, MUTED).next_to(what, m.DOWN, buff=0.35)
        self.say("[Thank you for watching.] [The derivations, the code, the proofs, the slides and this video are all in "
                 "the repository on GitHub.]", m.Write(thanks), m.AnimationGroup(m.FadeIn(what), m.FadeIn(url)))
        self.wait(2.0)
