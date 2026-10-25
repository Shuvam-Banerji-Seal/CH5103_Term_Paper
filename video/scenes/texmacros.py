"""Expand the slide deck's LaTeX macros (presentation/theme/noir-macros.sty) into plain LaTeX maths.

ManimGX typesets MathTex with Typst and accepts a LaTeX-maths subset without \\def or packages, so the deck's
own macros have to be written out before a formula from the slides can be reused in a scene.

- expand(s): notation macros (\\braket, \\mel, \\eri, \\Hop, \\OSS, ...) -> standard commands; colour shortcuts
  (\\cgold{x} ...) -> {x}; overlay helpers -> their content (see strip_overlays).
- strip_overlays(s): \\hl<n>{x}, \\hlr<n>{x}, \\hlg<n>{x}, \\canc<n>{x}, \\uncover<n>{x}, \\onslide<n>{x},
  \\only<n>{x} -> {x}. In the video the highlighting, striking out and step-by-step reveal are animations,
  so the formula itself carries only its content.
"""
from __future__ import annotations

import re

# name -> (number of arguments, template with #1..#n)
NOTATION: dict[str, tuple[int, str]] = {
    "pa": (0, r"\varphi_a"),
    "pb": (0, r"\varphi_b"),
    "ket": (1, r"\lvert #1\rangle"),
    "bra": (1, r"\langle #1\rvert"),
    "braket": (2, r"\langle #1\vert #2\rangle"),
    "mel": (3, r"\langle #1\vert #2\vert #3\rangle"),
    "ev": (1, r"\langle #1\rangle"),
    "eri": (4, r"(#1#2\vert #3#4)"),
    "Hop": (0, r"\hat H"),
    "dd": (0, r"\mathrm{d}"),
    "Eh": (0, r"E_{\mathrm h}"),
    "OSS": (0, r"\mathrm{OSS}"),
    "up": (0, r"\uparrow"),
    "dn": (0, r"\downarrow"),
    "stepno": (1, r"\text{(#1)}"),
}
COLOURS = ("cgold", "ccyan", "crose", "cgreen", "cviolet", "cblue", "cmuted")
OVERLAY = ("hl", "hlr", "hlg", "canc", "uncover", "onslide", "only", "visible", "invisible")


def _group(s: str, i: int) -> tuple[str, int]:
    """Read one macro argument at s[i]: a {balanced group} or a single token. Returns (content, next index)."""
    while i < len(s) and s[i] == " ":
        i += 1
    if i >= len(s):
        raise ValueError("missing macro argument")
    if s[i] == "{":
        depth = 0
        for j in range(i, len(s)):
            c = s[j]
            if c == "\\":  # skip escaped characters such as \{ \}
                continue
            if c == "{" and s[j - 1] != "\\":
                depth += 1
            elif c == "}" and s[j - 1] != "\\":
                depth -= 1
                if depth == 0:
                    return s[i + 1:j], j + 1
        raise ValueError(f"unbalanced braces in {s!r}")
    if s[i] == "\\":
        m = re.match(r"\\([A-Za-z]+|.)", s[i:])
        assert m
        return m.group(0), i + len(m.group(0))
    return s[i], i + 1


def _macro_iter(s: str, names: tuple[str, ...] | list[str]):
    """Positions of \\name for the given names, respecting word boundaries (\\pa does not match \\partial)."""
    pat = re.compile(r"\\(" + "|".join(sorted(map(re.escape, names), key=len, reverse=True)) + r")(?![A-Za-z])")
    return pat


def strip_overlays(s: str) -> str:
    pat = _macro_iter(s, OVERLAY)
    out, i = [], 0
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:])
            return "".join(out)
        out.append(s[i:m.start()])
        j = m.end()
        if j < len(s) and s[j] == "<":  # overlay specification <...>
            j = s.index(">", j) + 1
        arg, j = _group(s, j)
        out.append("{" + strip_overlays(arg) + "}")
        i = j


def expand(s: str) -> str:
    s = strip_overlays(s)
    names = list(NOTATION) + list(COLOURS)
    pat = _macro_iter(s, names)
    for _ in range(50):  # nested macros: repeat until nothing changes
        m = pat.search(s)
        if not m:
            return no_part_markers(s)
        name = m.group(1)
        j = m.end()
        if name in COLOURS:
            arg, j = _group(s, j)
            s = s[:m.start()] + "{" + arg + "}" + s[j:]
            continue
        n, template = NOTATION[name]
        args = []
        for _k in range(n):
            a, j = _group(s, j)
            args.append(a)
        rep = template
        for k, a in enumerate(args, 1):
            rep = rep.replace(f"#{k}", a)
        # a replacement ending in a command name must not run into a following letter (\rangle h, not \rangleh)
        if re.search(r"\\[A-Za-z]+$", rep) and j < len(s) and s[j].isalpha():
            rep += " "
        s = s[:m.start()] + rep + s[j:]
    raise RuntimeError(f"macro expansion did not terminate: {s!r}")


_DOUBLE_OPEN = re.compile(r"(?<!\\)\{\{")
_DOUBLE_CLOSE = re.compile(r"(?<!\\)\}\}")


def no_part_markers(s: str) -> str:
    """ManimGX's MathTex reads {{...}} as a part of the formula. Separate every pair of adjacent braces with a
    space (no change to the maths) so that expanded slide formulas never split by accident."""
    while True:
        t = _DOUBLE_CLOSE.sub("} }", _DOUBLE_OPEN.sub("{ {", s))
        if t == s:
            return s
        s = t
