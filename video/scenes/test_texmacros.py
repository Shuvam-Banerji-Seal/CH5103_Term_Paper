"""Unit tests for texmacros.expand (run: uv run --project video/scenes python -I -m pytest -q video/scenes)."""
from texmacros import expand, strip_overlays


def test_notation_macros():
    assert expand(r"\braket{a}{b}") == r"\langle a\vert b\rangle"
    assert expand(r"\mel{\psi_m}{\Hop}{\psi_n}") == r"\langle \psi_m\vert \hat H\vert \psi_n\rangle"
    assert expand(r"\eri abba") == r"(ab\vert ba)"
    assert expand(r"\eri{a}{b}{b}{a}") == r"(ab\vert ba)"
    # adjacent closing braces are separated (ManimGX part markers), harmless in maths mode
    assert expand(r"E_{\OSS}-E_T") == r"E_{\mathrm{OSS} }-E_T"
    assert expand(r"\ket{\Psi}") == r"\lvert \Psi\rangle"
    assert expand(r"\pa(1)\pb(2)") == r"\varphi_a(1)\varphi_b(2)"
    assert expand(r"\ev{\hat S^2}") == r"\langle \hat S^2\rangle"


def test_nested_braces_and_args():
    assert expand(r"\braket{\Theta_{0,0}}{\Theta_{1,M}}") == r"\langle \Theta_{0,0}\vert \Theta_{1,M}\rangle"
    assert expand(r"\mel{\Phi_\pm}{\Hop}{\text{cov}}") == r"\langle \Phi_\pm\vert \hat H\vert \text{cov}\rangle"


def test_overlay_helpers_keep_content():
    assert strip_overlays(r"\hlg<5->{2k}\;\hlr<5->{-\;\frac{4t^2}{U-V}}") == r"{2k}\;{-\;\frac{4t^2}{U-V}}"
    assert strip_overlays(r"\canc<4->{-x_1y_1}+x_1y_2") == r"{-x_1y_1}+x_1y_2"
    assert strip_overlays(r"\uncover<2->{E_N}&\uncover<2->{=h_s}") == r"{E_N}&{=h_s}"
    assert strip_overlays(r"\hl{x}") == r"{x}"


def test_colour_shortcuts_removed():
    assert expand(r"\cgold{x}+\crose{y}") == r"{x}+{y}"


def test_word_boundaries():
    # \pa must not eat \partial, \Hop must not match \Hopf
    assert expand(r"\partial_{n_i}") == r"\partial_{n_i}"
    assert expand(r"\pa\partial") == r"\varphi_a\partial"


def test_command_ending_macro_before_letter_gets_space():
    # \braket{a}{b}h must not become \rangleh (an unknown command)
    assert expand(r"\braket{\pa}{\pa}h_{ab}") == r"\langle \varphi_a\vert \varphi_a\rangle h_{ab}"
    assert expand(r"\braket{\psi_m}{\dot\psi_n}e^{i\theta}") == r"\langle \psi_m\vert \dot\psi_n\rangle e^{i\theta}"


def test_no_accidental_part_markers():
    # ManimGX reads {{...}} as a formula part; expansion must never create adjacent braces
    out = expand(r"\underbrace{x}_{\cmuted{\text{KE}}}")
    assert "{{" not in out and "}}" not in out
    out = expand(r"\frac{\canc<4->{-x_1y_1}+x_1y_2}{r^3}")
    assert "{{" not in out and "}}" not in out


def test_stepno():
    assert expand(r"\stepno{2}\ x") == r"\text{(2)}\ x"
