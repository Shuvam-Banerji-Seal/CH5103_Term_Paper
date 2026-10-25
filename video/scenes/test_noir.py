"""Prose-to-Typst conversion of the theme (noir.rich): escaping, emphasis, maths left alone."""
from noir import _latex_inline_to_typst as typst


def test_leading_markup_escaped_once():
    assert typst("+ or − ?") == "\\+ or − ?"
    assert typst("= sign") == "\\= sign"


def test_bold_and_italic_outside_maths():
    assert typst("**rule** and *two*") == "*rule* and _two_"


def test_bold_spanning_maths():
    out = typst(r"**here $\alpha$ is**")
    assert out.startswith("*here $#") and out.endswith("$ is*")


def test_asterisk_inside_maths_untouched():
    assert "_" not in typst(r"$a*b$")


def test_markup_characters_escaped():
    assert typst("a_b # x <y>") == "a\\_b \\# x \\<y\\>"


def test_code_span_becomes_raw():
    assert typst("Lean `three_d_four_s` ok") == 'Lean #raw("three_d_four_s") ok'
    assert typst('`a "b"`') == '#raw("a \\"b\\"")'
