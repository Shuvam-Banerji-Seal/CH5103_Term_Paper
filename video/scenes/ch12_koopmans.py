"""Chapter 12: Koopmans' and Janak's theorems, the gap as a HOMO difference (presentation/sections/14-koopmans.tex)."""
import manimgx as m

from ch01_foundations import explain
from noir import CYAN, FG, GOLD, GREEN, MUTED, ROSE, Box, Derivation, Frame, M, boxed, pill, rich


class S90Claim(Frame):
    """14-koopmans.tex, frame 1: 'The claim'."""

    TITLE = "The claim"
    SYMBOLS = (r"STG: $E_S-E_T$ — HOMO: highest occupied molecular orbital — Koopmans: orbital energy ≈ minus the "
               r"ionisation energy, Hartree–Fock — Janak: orbital energy = slope of $E$ with occupation, DFT — “…” omits "
               r"“in excited state DFT for multiplets”")

    def construct(self) -> None:
        self.setup_frame()
        claim = boxed('"An alternative theoretical interpretation of the Hund\'s multiplicity rule has been proposed on the '
                      'basis of Janak theorem (or extended Koopmans\' theorem) …: at the Hartree–Fock level, the '
                      'singlet-triplet gap (STG) is equal to the difference between the energies of the triplet\'s and '
                      'open-shell singlet\'s HOMOs." — p. 442–443', "claim", width=12.6, size=29).move_to([0, 1.2, 0])
        steps = m.VGroup(rich("**Koopmans' theorem**", 32, GOLD), rich("⟶", 40, FG), rich("**Janak's theorem**", 32, GOLD),
                         rich("⟶", 40, FG), rich("**the gap**", 32, GOLD)).arrange(m.RIGHT, buff=0.35)
        steps.move_to([0, -0.85, 0])
        q = rich("which difference, which sign? the review does not say; the derivation will", 26, MUTED)
        q.move_to([0, -1.75, 0])
        self.say("[Part thirteen: Koopmans and Janak. The review mentions an alternative interpretation of Hund's rule: "
                 "an alternative theoretical interpretation of the Hund's multiplicity rule has been proposed on the "
                 "basis of Janak theorem, or extended Koopmans' theorem: at the Hartree Fock level, the singlet-triplet "
                 "gap is equal to the difference between the energies of the triplet's and open-shell singlet's highest "
                 "occupied orbitals.]", m.FadeIn(claim))
        self.say("[We derive it in three steps: Koopmans' theorem, then Janak's theorem, then the gap.]", m.FadeIn(steps))
        self.say("[Which difference, and with which sign? The review does not say. The derivation will.]", m.FadeIn(q))
        self.wait(0.4)


class S91Koopmans(Frame):
    """14-koopmans.tex, frame 2: 'Koopmans' theorem'."""

    TITLE = "Koopmans' theorem"
    SYMBOLS = (r"$\chi_i$: spin orbital, space × spin — $\hat h$: kinetic + nuclear attraction — "
               r"$[ij|kl]=\iint\chi_i^*(1)\chi_j(1)\,r_{12}^{-1}\,\chi_k^*(2)\chi_l(2)$ — $[ii|jj]$: Coulomb, $[ij|ji]$: "
               r"exchange, zero unless same spin — $\varepsilon_k$: orbital energy — IP: ionisation potential")

    def construct(self) -> None:
        self.setup_frame()
        assume = boxed(r"single determinant of spin orbitals $\chi_i$; remove $\chi_k$ *without* relaxing the others",
                       "assume", width=9.6, size=27).move_to([0, 2.05, 0])
        d = Derivation([
            (r"E_N", r"=\textstyle\sum_i\langle i|\hat h|i\rangle+\tfrac12\sum_{i,j}\bigl([ii|jj]-[ij|ji]\bigr)",
             "Slater–Condon rules"),
            (r"E_N-E_{N-1}^{(k)}", r"=\langle k|\hat h|k\rangle+\tfrac12\textstyle\sum_j(\ldots)_{kj}+\tfrac12\sum_i(\ldots)_{ik}",
             r"keep only terms containing $k$"),
            ("", r"=\langle k|\hat h|k\rangle+\textstyle\sum_j\bigl([kk|jj]-[kj|jk]\bigr)",
             r"halves equal, $[ab|cd]=[cd|ab]$; $j{=}k$ cancels"),
            ("", r"=\varepsilon_k", "definition of the Fock eigenvalue"),
        ], size=32, why_size=24).move_to([0, 0.05, 0])
        ip = m.VGroup(M(r"\mathrm{IP}_k=E_{N-1}^{(k)}-E_N=-\varepsilon_k", size=40), rich("frozen orbitals", 26, MUTED))
        ip.arrange(m.RIGHT, buff=0.4).move_to([0, -2.05, 0])
        self.say("[Koopmans' theorem first. Assume a single determinant of spin orbitals chi i, and remove the electron in "
                 "chi k without relaxing any of the others.]", m.FadeIn(assume))
        self.say("[By the Slater Condon rules, the energy of the N electron determinant is the sum of the one-electron "
                 "energies, plus one half the double sum over pairs of Coulomb minus exchange integrals.]",
                 m.FadeIn(d.rows[0]))
        self.say("[The determinant without chi k has the same sums with k left out. So the difference keeps only the "
                 "terms that contain k: its one-electron energy, the half sum with i equal to k, and the half sum with j "
                 "equal to k.] The term with both equal to k is counted twice, but it is k k k k minus k k k k, which is "
                 "zero.", m.FadeIn(d.rows[1]))
        self.say("[The two half sums are equal, because the integrals are symmetric under swapping their electron pairs, "
                 "so together they make one full sum of Coulomb minus exchange between k and every j.]",
                 m.FadeIn(d.rows[2]))
        self.say("[That is exactly the definition of the Fock eigenvalue epsilon k.]", m.FadeIn(d.rows[3]))
        self.say("[So the ionisation potential of orbital k is minus epsilon k, with frozen orbitals.]", m.FadeIn(ip))
        self.wait(0.4)


class S92Janak(Frame):
    """14-koopmans.tex, frame 3: 'Janak's theorem'."""

    TITLE = "Janak's theorem"
    SYMBOLS = (r"$n_i\in[0,1]$: occupation — $\psi_i$: Kohn–Sham orbital — $v$: nuclear potential — $E_H$, "
               r"$v_H=\delta E_H/\delta\rho$: Hartree, classical, repulsion — $E_{xc}$, $v_{xc}$: exchange–correlation — "
               r"$\rho$: electron density")

    def construct(self) -> None:
        self.setup_frame()
        assume = boxed(r"$E=\sum_in_i\langle\psi_i|-\tfrac12\nabla^2|\psi_i\rangle+\int v\rho+E_H[\rho]+E_{xc}[\rho]$, "
                       r"$\rho=\sum_in_i|\psi_i|^2$", "assume", width=11.2, size=28,
                       tag="Kohn–Sham with fractional occupations $n_i$").move_to([0, 1.9, 0])
        d = Derivation([
            (r"\frac{\partial E}{\partial n_i}\bigg|_{\text{explicit}}",
             r"=\langle\psi_i|-\tfrac12\nabla^2+v+v_H+v_{xc}|\psi_i\rangle=\varepsilon_i",
             r"$n_i$ enters $\rho$ linearly; chain rule"),
            (r"\frac{\partial E}{\partial n_i}\bigg|_{\text{via }\psi_j}",
             r"=\textstyle\sum_jn_j\varepsilon_j\,\partial_{n_i}\langle\psi_j|\psi_j\rangle=0",
             r"$\delta E/\delta\psi_j^*=n_j\varepsilon_j\psi_j$; norms stay 1"),
        ], size=32, why_size=24).move_to([0, 0.2, 0])
        res = m.VGroup(M(r"\boxed{\partial E/\partial n_i=\varepsilon_i}", size=40), rich("for any $E_{xc}$", 28),
                       rich("Janak, Phys. Rev. B 18, 7165, 1978", 24, MUTED)).arrange(m.RIGHT, buff=0.4)
        res.move_to([0, -1.35, 0])
        e = explain("integer occupations and frozen orbitals turn this slope into a finite difference: Koopmans' theorem "
                    "again", width=11).move_to([0, -2.15, 0])
        self.say("[Janak's theorem works in Kohn Sham density functional theory with fractional occupations n i. The "
                 "energy is the occupation-weighted kinetic energy, plus the nuclear attraction of the density, plus the "
                 "Hartree and exchange correlation energies, where the density is the sum of n i times the orbital "
                 "density.]", m.FadeIn(assume))
        self.say("[Differentiate with respect to n i. The explicit dependence: n i enters the density linearly, so by the "
                 "chain rule the derivative is the expectation value of the Kohn Sham operator in orbital i, which is "
                 "epsilon i.]", m.FadeIn(d.rows[0]))
        self.say("[The orbitals also change with n i. But the energy's derivative with respect to each orbital is n j "
                 "epsilon j times that orbital, so this contribution is proportional to the change in each orbital's "
                 "norm, which stays one. It vanishes.]", m.FadeIn(d.rows[1]))
        self.say("[So the derivative of the energy with respect to an occupation is the orbital energy, for any exchange "
                 "correlation functional. This is Janak's theorem, Physical Review B, nineteen seventy eight.]",
                 m.FadeIn(res))
        self.say("[With integer occupations and frozen orbitals, this slope becomes a finite difference, and Koopmans' "
                 "theorem comes back.]", m.FadeIn(e))
        self.wait(0.4)


class S93GapHomo(Frame):
    """14-koopmans.tex, frame 4: 'The gap as a HOMO difference'."""

    TITLE = "The gap as a HOMO difference"
    SUBTITLE = (r"HOMO energy of a state $:=$ minus the cost of removing its $\pb$ electron, $\pa$ frozen; ion: "
                r"$E_{\text{ion}}=h_a$")
    SYMBOLS = (r"$h_a,h_b$: one-electron energies — $J_{ab}$: Coulomb, $K_{ab}\ge0$: exchange integral — ion: one "
               r"electron left, in $\pa$ — hardness: resistance to losing an electron")

    def construct(self) -> None:
        self.setup_frame()
        d = Derivation([
            (r"\varepsilon_b^{T}", r"=E_T-E_{\text{ion}}=h_b+J_{ab}-K_{ab}", r"$E_T=h_a+h_b+J-K$, Part V"),
            (r"\varepsilon_b^{\OSS}", r"=E_{\OSS}-E_{\text{ion}}=h_b+J_{ab}+K_{ab}", r"$E_{\OSS}=h_a+h_b+J+K$"),
            (r"E_{\OSS}-E_T", r"=\varepsilon^{\OSS}_{\text{HOMO}}-\varepsilon^{T}_{\text{HOMO}}=2K_{ab}",
             r"$E_{\text{ion}}$ cancels"),
        ], size=36, why_size=26).move_to([0, 0.9, 0])
        res = Box(m.VGroup(rich('frozen orbitals: the triplet\'s HOMO is lower, "harder", by $2K$, cf. Pearson. Review\'s '
                                'caveat, ref. 20: "lacks dynamic electron correlation"; relaxation is missing too.', 28,
                                width=10.4), pill("verified")).arrange(m.RIGHT, buff=0.3), "result").move_to([0, -1.6, 0])
        self.say("[Now the gap. Define the HOMO energy of a state as minus the cost of removing its phi b electron, with "
                 "phi a frozen. What remains is the ion, one electron in phi a, with energy h a.] For the triplet, the "
                 "HOMO energy is the triplet energy minus the ion's: h b plus J minus K, using the triplet energy from "
                 "Part five.", m.FadeIn(d.rows[0]))
        self.say("[For the open-shell singlet, the same subtraction gives h b plus J plus K.]", m.FadeIn(d.rows[1]))
        self.say("[Subtract: the ion's energy cancels, and the singlet-triplet gap, E O S S minus E T, equals the singlet's "
                 "HOMO energy minus the triplet's, which is two K.] So the review's statement holds, with this sign: "
                 "the singlet's HOMO lies higher.", m.FadeIn(d.rows[2]))
        self.say("[With frozen orbitals, the triplet's HOMO is lower, or harder, by two K, in Pearson's sense. The review "
                 "adds the caveat, from its reference twenty, that this lacks dynamic electron correlation; orbital "
                 "relaxation is missing too. Verified, within those limits.]", m.FadeIn(res))
        self.wait(0.4)
