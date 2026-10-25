"""The slides' "Noir" look, rebuilt in ManimGX for the explainer video.

Colours, fonts and furniture follow presentation/theme/beamerthemeNoir.sty and noir-macros.sty: calligraphic gold
frame titles with a fading gold rule, panels with a coloured left edge and a small-caps tag (the paper says /
assumptions / result / verified / erratum), verdict pills, blue-italic "why" notes beside derivation steps and a
symbols strip at the foot of the frame.

Frame layout (scene units; the frame is 14.22 × 8, centred on the origin):
  y ∈ [ 3.0,  4.0]  title and subtitle
  y ∈ [-2.95, 2.9]  content
  y ∈ [-3.55,-3.0]  symbols strip
  y < -3.6         reserved for the editor's footline (section name, progress bar), drawn by video/editor
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

import manimgx as m

from texmacros import expand
from voice import Breeze, store_digest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FONTS = [str(HERE / "fonts")]
FIGURES = ROOT / "assets" / "figures"
SHOTS = ROOT / "presentation" / "figures" / "screenshots"

# ------------------------------------------------------------------ palette (beamerthemeNoir.sty)
BG, PANEL, PANEL_HI, TRACK = "#000000", "#111116", "#1A1A22", "#24242C"
FG, MUTED = "#ECE8E1", "#9C9AA6"
GOLD, CYAN, ROSE, GREEN = "#E9B95B", "#5FD4D0", "#FF5D8F", "#72DD8F"
VIOLET, BLUE, ORANGE, EXPL = "#AE8FFF", "#7DB9FF", "#FF9F55", "#A9D8E6"

m.config.background_color = BG

# ------------------------------------------------------------------ fonts (video/scenes/fonts)
CALLI, SERIF, GARAMOND, MONO = "TeX Gyre Chorus", "Libertinus Serif", "EB Garamond", "JetBrains Mono"
MATH_PREAMBLE = '#show math.equation: set text(font: "Libertinus Math")\n'
TEXT_PREAMBLE = MATH_PREAMBLE + '#set text(font: "Libertinus Serif")\n'

TOP, BOTTOM = 2.9, -2.95  # content area
LEFT, RIGHT = -6.75, 6.75


def T(text: str, size: float = 30, color: str = FG, font: str = SERIF, **kw) -> m.Text:
    """Plain text in a slide font."""
    return m.Text(text, font=font, font_size=size, color=color, font_paths=FONTS, **kw)


def M(*tex: str, size: float = 40, color: str = FG, **kw) -> m.MathTex:
    """A formula from slide LaTeX: the deck's macros are expanded, maths is set in Libertinus Math. Several strings
    become separately addressable parts (formula[i])."""
    return m.MathTex(*[expand(t) for t in tex], font_size=size, color=color, font_paths=FONTS,
                     typst_preamble=MATH_PREAMBLE, **kw)


def X(tex: str, size: float = 30, color: str = FG, **kw) -> m.Tex:
    """Prose with inline maths ($...$), in Libertinus."""
    return m.Tex(expand(tex), font_size=size, color=color, font_paths=FONTS, typst_preamble=TEXT_PREAMBLE, **kw)


def SC(text: str, size: float = 22, color: str = BG, font: str = GARAMOND) -> m.Typst:
    """Small-capital labels as in the slides' box tags, pills and headings, set as tracked capitals at 85 % size so
    every letter has full cap height (true small caps are too short to read at 1080p)."""
    safe = re.sub(r"([\\#*_@<>`\[\]$~])", r"\\\1", text)
    return m.Typst(f'#set text(font: "{font}", tracking: 0.06em)\n#upper[{safe}]', font_size=size * 0.85,
                   color=color, font_paths=FONTS)


def why(text: str, size: float = 22) -> m.Mobject:
    """A derivation step's reason: blue italic EB Garamond with $...$ maths (\\why in the slides)."""
    return rich(text, size=size, color=EXPL, font=GARAMOND, italic=True)


# ------------------------------------------------------------------ frame title
class Title(m.VGroup):
    """Calligraphic gold title at the top left, an optional muted italic subtitle, and the fading gold rule."""

    def __init__(self, title: str, subtitle: str = "", size: float = 40):
        head = rich(title, size=size, color=GOLD, font=CALLI)
        parts: list[m.Mobject] = [head]
        if subtitle:
            parts.append(rich(subtitle, size=26, color=MUTED, font=GARAMOND, italic=True))
        group = m.VGroup(*parts).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.12)
        rule = m.Line(m.LEFT * 0, m.RIGHT * 0.62 * m.config.frame_width, stroke_width=1.6)
        rule.set_color([GOLD, BG])
        rule.next_to(group, m.DOWN, buff=0.14, aligned_edge=m.LEFT)
        super().__init__(group, rule)
        self.head, self.rule = head, rule
        self.to_corner(m.UL, buff=0.3)


# ------------------------------------------------------------------ boxes (tcolorbox styles in noir-macros.sty)
KIND = {
    "claim": ("The paper says", GOLD),
    "assume": ("Assumptions", VIOLET),
    "result": ("Result", GREEN),
    "checked": ("Verified", CYAN),
    "erratum": ("Erratum", ROSE),
    "plain": ("", None),
}


class Box(m.VGroup):
    """A panel around `body`, with a coloured left edge and a small-caps tag on its top-left corner."""

    def __init__(self, body: m.Mobject, kind: str = "plain", tag: str | None = None, width: float | None = None,
                 pad: float = 0.22):
        label, colour = KIND[kind]
        label = tag if tag is not None else label
        w = (width if width is not None else body.width + 2 * pad)
        h = body.height + 2 * pad + (0.12 if label else 0)
        panel = m.RoundedRectangle(corner_radius=0.05, width=w, height=h, stroke_width=0,
                                   fill_color=PANEL, fill_opacity=1)
        body.move_to(panel.get_center() + (m.DOWN * 0.06 if label else 0))
        if width is not None:
            body.align_to(panel, m.LEFT).shift(m.RIGHT * pad)
        parts: list[m.Mobject] = [panel]
        if colour:
            edge = m.Rectangle(width=0.045, height=h, stroke_width=0, fill_color=colour, fill_opacity=1)
            edge.align_to(panel, m.LEFT).align_to(panel, m.UP)
            parts.append(edge)
        if label:
            text = SC(label, size=28, color=BG)
            chip = m.RoundedRectangle(corner_radius=0.03, width=text.width + 0.24, height=text.height + 0.14,
                                      stroke_width=0, fill_color=colour, fill_opacity=1)
            text.move_to(chip)
            tagg = m.VGroup(chip, text)
            tagg.move_to(panel.get_corner(m.UL) + m.RIGHT * (tagg.width / 2 + 0.2))
            parts += [body, tagg]
        else:
            parts.append(body)
        super().__init__(*parts)
        self.panel, self.body = panel, body


def boxed(text: str, kind: str = "plain", width: float = 6.0, size: float = 26, tag: str | None = None) -> Box:
    """A box whose body is prose with inline maths, wrapped to `width`."""
    body = paragraph(text, width=width - 0.44, size=size)
    return Box(body, kind=kind, tag=tag, width=width)


def paragraph(text: str, width: float, size: float = 26, color: str = FG) -> m.Typst:
    """Wrapped prose (Typst block of the given width), with $LaTeX$ inline maths converted by mitex as MathTex
    does (manimgx.mobjects.text._math: private, but manimgx is pinned to 0.1.1 in uv.lock)."""
    body = _latex_inline_to_typst(text)
    width_em = width / (size / 96)  # ManimGX: an em is font_size/96 scene units
    code = ('#import "@preview/mitex:0.2.7": mitex-scope\n#set text(font: "Libertinus Serif")\n'
            '#show math.equation: set text(font: "Libertinus Math")\n#set par(leading: 0.5em)\n'
            f'#show raw: set text(font: "{MONO}", size: 0.92em)\n'
            f'#block(width: {width_em:.2f}em)[{body}]')
    return m.Typst(code, font_size=size, color=color, font_paths=FONTS)


def rich(text: str, size: float = 30, color: str = FG, font: str = SERIF, width: float | None = None,
         italic: bool = False) -> m.Typst:
    """A line (or, with `width`, a wrapped block) of text in `font` with $LaTeX$ maths in Libertinus Math."""
    body = _latex_inline_to_typst(text)
    style = ', style: "italic"' if italic else ""
    code = (f'#import "@preview/mitex:0.2.7": mitex-scope\n#set text(font: "{font}"{style})\n'
            '#show math.equation: set text(font: "Libertinus Math")\n#set par(leading: 0.5em)\n'
            f'#show raw: set text(font: "{MONO}", size: 0.92em)\n')
    code += f'#block(width: {width / (size / 96):.2f}em)[{body}]' if width else body
    return m.Typst(code, font_size=size, color=color, font_paths=FONTS)


_STRONG, _EMPH, _CODE = "\x01", "\x02", "\x03"


def _mark_emphasis(text: str, codes: list[str] | None = None) -> str:
    """**bold**, *italic* and `code` outside $maths$ become placeholders that survive escaping (Typst *strong*,
    _emph_ and raw); the code spans' contents are moved to `codes`."""
    out, in_math, i = [], False, 0
    while i < len(text):
        c = text[i]
        if c == "`" and not in_math and codes is not None:
            j = text.index("`", i + 1)
            codes.append(text[i + 1:j])
            out.append(_CODE)
            i = j + 1
            continue
        if c == "$":
            in_math = not in_math
        elif not in_math and text.startswith("**", i):
            out.append(_STRONG)
            i += 2
            continue
        elif not in_math and c == "*":
            out.append(_EMPH)
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _latex_inline_to_typst(text: str) -> str:
    """Prose with $LaTeX$ -> Typst markup: text escaped, maths converted by mitex and evaluated in its scope;
    **bold** and *italic* outside maths become Typst strong and emphasis."""
    from manimgx.mobjects.text import _math

    codes: list[str] = []
    out, parts = [], _mark_emphasis(text, codes).split("$")
    if len(parts) % 2 == 0:
        raise ValueError(f"unbalanced $ in {text!r}")
    for i, p in enumerate(parts):
        if i % 2:
            out.append("$#" + _math(expand(p)) + "$")
        else:
            esc = re.sub(r"([\\#*_@<>`\[\]$~])", r"\\\1", p)
            if i == 0 and esc[:1] in ("+", "-", "=", "/"):
                esc = "\\" + esc  # Typst reads "+ ", "- ", "= ", "/ " at a line start as list/heading/term markup
            out.append(esc)
    typst = "".join(out).replace(_STRONG, "*").replace(_EMPH, "_")
    for code in codes:
        literal = code.replace("\\", "\\\\").replace('"', '\\"')
        typst = typst.replace(_CODE, f'#raw("{literal}")', 1)
    return typst


# ------------------------------------------------------------------ pills
PILL = {"verified": GREEN, "error": ROSE, "overstated": ORANGE, "partial": GOLD, "fail": ROSE,
        "inconsistent": ORANGE, "imprecise": ORANGE, "pass": GREEN, "by hand": MUTED}


def pill(label: str, colour: str | None = None, size: float = 28) -> m.VGroup:
    text = SC(label, size=size, color=BG)
    chip = m.RoundedRectangle(corner_radius=0.04, width=text.width + 0.2, height=text.height + 0.12,
                              stroke_width=0, fill_color=colour or PILL.get(label, MUTED), fill_opacity=1)
    text.move_to(chip)
    return m.VGroup(chip, text)


# ------------------------------------------------------------------ symbols strip
class SymbolStrip(m.VGroup):
    """The glossary at the foot of the frame: 'symbols' in gold small caps, then prose with inline maths."""

    def __init__(self, text: str, size: float = 24):
        label = SC("symbols", size=32, color=GOLD)
        body = paragraph(text, width=13.5 - 0.3 - label.width - 0.3, size=size, color=FG)
        row = m.VGroup(label, body).arrange(m.RIGHT, buff=0.25, aligned_edge=m.UP)
        panel = m.RoundedRectangle(corner_radius=0.03, width=13.5, height=max(0.42, row.height + 0.16),
                                   stroke_width=0, fill_color=PANEL, fill_opacity=1)
        row.move_to(panel).align_to(panel, m.LEFT).shift(m.RIGHT * 0.15)
        super().__init__(panel, row)
        self.move_to([0, -3.0 - panel.height / 2 + 0.0, 0]).align_to([0, -3.0, 0], m.UP)


# ------------------------------------------------------------------ derivations
class Derivation(m.VGroup):
    """Rows of a derivation, aligned at their relation sign: lhs | rhs (starting with '=' or similar) | why.

    rows: (lhs, rhs, why) with LaTeX strings; lhs may be "" (a continuation row). rhs may be a list of LaTeX
    parts (to colour or address them). Each row is (row.lhs, row.rhs, row.why); reveal them with show_row().
    """

    def __init__(self, rows: Sequence[tuple[str, str | Sequence[str], str]], size: float = 38,
                 why_size: float = 26, row_buff: float = 0.32, why_gap: float = 0.6):
        made = []
        for lhs, rhs, note in rows:
            L = M(lhs, size=size) if lhs else m.VGroup()
            R = M(*(rhs if isinstance(rhs, (list, tuple)) else [rhs]), size=size)
            W = why(note, size=why_size) if note else m.VGroup()
            made.append((L, R, W))
        super().__init__()
        y = 0.0
        x_eq = max((L.width for L, _, _ in made), default=0) + 0.12
        x_why = x_eq + max(R.width for _, R, _ in made) + why_gap
        self.rows = []
        for L, R, W in made:
            h = max(L.height if len(L) else 0, R.height)
            R.move_to([x_eq + R.width / 2, y - h / 2, 0])
            if len(L):
                L.move_to([x_eq - 0.12 - L.width / 2, R.get_center()[1], 0])
            if len(W):
                W.move_to([x_why + W.width / 2, R.get_center()[1], 0])
            row = m.VGroup(L, R, W)
            self.rows.append(row)
            self.add(row)
            y -= h + row_buff
        self.center()


# ------------------------------------------------------------------ orbital levels (\orblevel, \elup, \eldn)
def level(x: float, y: float, w: float = 0.7, label: str = "", colour: str = FG) -> m.VGroup:
    line = m.Line([x - w / 2, y, 0], [x + w / 2, y, 0], stroke_width=3.2, color=colour)
    grp = m.VGroup(line)
    if label:
        grp.add(T(label, size=20, color=MUTED, font=GARAMOND).next_to(line, m.RIGHT, buff=0.12))
    return grp


def spin(x: float, y: float, up: bool = True, h: float = 0.42) -> m.Arrow:
    dx = -0.09 if up else 0.09
    a, b = ([x + dx, y - h * 0.45, 0], [x + dx, y + h * 0.55, 0]) if up else ([x + dx, y + h * 0.55, 0], [x + dx, y - h * 0.45, 0])
    return m.Arrow(a, b, buff=0, stroke_width=4, color=ROSE if up else BLUE, max_tip_length_to_length_ratio=0.3)


# ------------------------------------------------------------------ figures
DIAGRAMS = ROOT / "presentation" / "figures" / "diagrams-svg"
RASTER = ROOT / "video" / "build" / "raster"


def diagram(name: str, height: float = 4.0, max_width: float | None = None) -> m.ImageMobject:
    """One of the slides' JavaScript NBMO diagrams (presentation/figures/diagrams-svg, drawn on black in the
    noir palette), rasterised at 4x with rsvg-convert against the bundled fonts."""
    svg = DIAGRAMS / name
    png = RASTER / (svg.stem + ".png")
    if not png.exists() or png.stat().st_mtime < svg.stat().st_mtime:
        RASTER.mkdir(parents=True, exist_ok=True)
        conf = RASTER / "fonts.conf"
        conf.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
                        f'<include ignore_missing="yes">/etc/fonts/fonts.conf</include><dir>{FONTS[0]}</dir>'
                        '</fontconfig>')
        subprocess.run(["rsvg-convert", "-z", "4", "-o", str(png), str(svg)], check=True,
                       env={**os.environ, "FONTCONFIG_FILE": str(conf)})
    img = m.ImageMobject(str(png))
    img.height = height
    if max_width is not None and img.width > max_width:
        img.width = max_width
    return img


def figure(name: str, height: float = 5.0, max_width: float | None = None) -> m.Group:
    """One of the review's figures (assets/figures) on a white card, as on the slides."""
    path = FIGURES / name if (FIGURES / name).exists() else SHOTS / name
    img = m.ImageMobject(str(path))
    img.height = height
    if max_width is not None and img.width > max_width:
        img.width = max_width
    card = m.RoundedRectangle(corner_radius=0.05, width=img.width + 0.24, height=img.height + 0.24,
                              stroke_width=0, fill_color="#FFFFFF", fill_opacity=1)
    img.move_to(card)
    return m.Group(card, img)


# ------------------------------------------------------------------ the base scene
class Frame(m.Scene):
    """One slide frame of the deck. Subclasses set TITLE (and SUBTITLE, SYMBOLS) and write construct().
    The narration voice is Breeze-TTS-2 (voice.py); VIDEO_VOICE=draft|collect|final selects how lines are spoken."""

    TITLE = ""
    SUBTITLE = ""
    SYMBOLS = ""
    voice = Breeze(mode=os.environ.get("VIDEO_VOICE", "draft"),
                   digest=store_digest() if os.environ.get("VIDEO_VOICE") == "final" else "")

    def setup_frame(self, animate: bool = True) -> Title | None:
        title = Title(self.TITLE, self.SUBTITLE) if self.TITLE else None
        strip = SymbolStrip(self.SYMBOLS) if self.SYMBOLS else None
        self.title_group, self.strip = title, strip
        shown = [x for x in (title, strip) if x is not None]
        if shown:
            if animate:
                self.play(*[m.FadeIn(x, shift=m.DOWN * 0.1) for x in shown], run_time=0.8)
            else:
                self.add(*shown)
        return title

    def clear_frame(self, run_time: float = 0.6) -> None:
        if self.mobjects:
            self.play(*[m.FadeOut(x) for x in self.mobjects], run_time=run_time)


def table_rows(table: m.Mobject, n: int) -> list[m.VGroup]:
    """The glyphs of a typeset table (MathTex array) grouped into its n rows, top to bottom, by splitting at the n-1
    largest vertical gaps between glyph centres; a rule such as \\hline joins the row above it. For revealing a
    table row by row without typesetting partial tables."""
    glyphs = [g for g in table.family_members_with_points() if len(g.get_points())]
    glyphs.sort(key=lambda g: -g.get_center()[1])
    ys = [g.get_center()[1] for g in glyphs]
    gaps = sorted(range(1, len(ys)), key=lambda i: ys[i - 1] - ys[i], reverse=True)[: n - 1]
    cuts = [0, *sorted(gaps), len(glyphs)]
    return [m.VGroup(*glyphs[a:b]) for a, b in zip(cuts, cuts[1:])]


_LANG = {".py": "python", ".lean": None, ".tex": "latex", ".ts": "typescript", ".js": "js", ".toml": "toml"}


def excerpt(relpath: str, first: int, last: int, width: float | None = None, height: float | None = None,
            numbers: bool = True) -> m.Code:
    """Lines first..last (1-based, inclusive) of a repository file, highlighted, numbered as in the file. The code
    is read at render time, never retyped, so what is shown is what was run."""
    path = ROOT / relpath
    lines = path.read_text(encoding="utf-8").splitlines()[first - 1:last]
    if len(lines) != last - first + 1:
        raise ValueError(f"{relpath} has no lines {first}-{last}")
    if not lines[0].strip() or not lines[-1].strip():
        # m.Code drops blank lines at the ends, which would shift every index into code_lines
        raise ValueError(f"{relpath} lines {first}-{last}: the range starts or ends on a blank line")
    c = m.Code(code_string="\n".join(lines), language=_LANG.get(path.suffix), add_line_numbers=numbers,
               line_numbers_from=first, background="rectangle")
    # the "vim" style draws comments navy (#000080), unreadable on black: lift every dark glyph to the muted grey
    for g in c.code_lines.family_members_with_points():
        col = m.ManimColor(g.get_fill_color()) if hasattr(g, "get_fill_color") else None
        if col is not None and sum(col.to_rgb()) / 3 < 0.3:
            g.set_fill(EXPL)
    if width is not None and c.width > width:
        c.scale_to_fit_width(width)
    if height is not None and c.height > height:
        c.scale_to_fit_height(height)
    return c


def paint_parts(formula: m.Mobject, colours: dict[str, str]) -> None:
    """Colour the parts of a MathTex whose LaTeX equals a key of `colours` (e.g. {"A": CYAN, "B": ROSE})."""
    strings = getattr(formula, "tex_strings", None)
    if not strings:
        return
    for i, s in enumerate(strings):
        if s.strip() in colours:
            formula[i].set_color(colours[s.strip()])


# ------------------------------------------------------------------ diagrams and lists
def node(text: str, colour: str = GOLD, width: float = 2.6, height: float = 0.85, size: float = 24,
         fill: str = PANEL, font: str = GARAMOND) -> m.VGroup:
    """A rounded box with a coloured outline and centred text (TikZ 'stop' / noirbox nodes of the slides).
    Lines in `text` are separated by '\\n'; $...$ maths is allowed."""
    box = m.RoundedRectangle(corner_radius=0.08, width=width, height=height, stroke_color=colour, stroke_width=2.4,
                             fill_color=fill, fill_opacity=1)
    lines = [rich(t, size=size, color=FG, font=font) for t in text.split("\n")]
    label = m.VGroup(*lines).arrange(m.DOWN, buff=0.06).move_to(box)
    if label.width > width - 0.34:
        label.scale_to_fit_width(width - 0.34)
    return m.VGroup(box, label)


def connect(a: m.Mobject, b: m.Mobject, colour: str = MUTED, buff: float = 0.08) -> m.Arrow:
    """An arrow from the edge of a to the edge of b."""
    return m.Arrow(a.get_center(), b.get_center(), buff=0, stroke_width=3, color=colour,
                   max_tip_length_to_length_ratio=0.12).put_start_and_end_on(
        _edge_toward(a, b.get_center(), buff), _edge_toward(b, a.get_center(), buff))


def _edge_toward(mob: m.Mobject, target, buff: float):
    import numpy as np
    c = np.array(mob.get_center())
    d = np.array(target) - c
    if np.allclose(d, 0):
        return c
    hw, hh = mob.width / 2 + buff, mob.height / 2 + buff
    s = min(hw / abs(d[0]) if d[0] else np.inf, hh / abs(d[1]) if d[1] else np.inf)
    return c + d * s


def diamond(colour: str = GOLD, size: float = 0.13) -> m.Square:
    return m.Square(side_length=size, stroke_width=0, fill_color=colour, fill_opacity=1).rotate(m.PI / 4)


def bullets(items: Sequence[str], width: float = 6.0, size: float = 28, colour: str = GOLD,
            buff: float = 0.28) -> m.VGroup:
    """A list with the slides' gold diamond bullets; each item is prose with $...$ maths, wrapped to `width`."""
    rows = []
    for it in items:
        text = rich(it, size=size, width=width - 0.45)
        mark = diamond(colour)
        mark.next_to(text, m.LEFT, buff=0.22).align_to(text, m.UP).shift(m.DOWN * 0.12)
        rows.append(m.VGroup(mark, text))
    return m.VGroup(*rows).arrange(m.DOWN, aligned_edge=m.LEFT, buff=buff)


# ------------------------------------------------------------------ plots
def axes(x_range, y_range, x_length: float, y_length: float, **kw) -> m.Axes:
    """Bare ManimGX axes (lines through zero, no numbers); prefer Plot, which matches the slides' pgfplots."""
    return m.Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_tip": False, "font_size": 24},
                  **kw)


class Plot(m.VGroup):
    """Box-style axes as in the slides' pgfplots: the axis lines lie on the bottom and left edges whatever the
    range, with ticks and numbers at the given values and faint horizontal grid lines (ymajorgrids). Axes through
    zero would put the x axis across the middle of a plot of negative energies.

    c2p(x, y) maps data to the screen (log10 first on a log axis); x_axis / y_axis are the edge lines."""

    def __init__(self, x_range: Sequence[float], y_range: Sequence[float], x_length: float, y_length: float, *,
                 xticks: Sequence[float] = (), yticks: Sequence[float] = (), xfmt: str = "{:g}", yfmt: str = "{:g}",
                 log_x: bool = False, log_y: bool = False, grid: bool = True, num_size: float = 26):
        import math

        super().__init__()
        self.fx = math.log10 if log_x else float
        self.fy = math.log10 if log_y else float
        self.lo = (self.fx(x_range[0]), self.fy(y_range[0]))
        self.hi = (self.fx(x_range[1]), self.fy(y_range[1]))
        self.x_axis = m.Line([0, 0, 0], [x_length, 0, 0], color=MUTED, stroke_width=2)
        self.y_axis = m.Line([0, 0, 0], [0, y_length, 0], color=MUTED, stroke_width=2)
        self.add(self.x_axis, self.y_axis)
        self.grid, self.ticks, self.numbers = m.VGroup(), m.VGroup(), m.VGroup()
        for v in xticks:
            p = self.c2p(v, y_range[0])
            self.ticks.add(m.Line(p, p + np.array([0, 0.1, 0]), color=MUTED, stroke_width=2))
            label = rf"10^{{{round(math.log10(v))}}}" if log_x else xfmt.format(v)
            self.numbers.add(M(label, size=num_size, color=MUTED).next_to(p, m.DOWN, buff=0.12))
        for v in yticks:
            p = self.c2p(x_range[0], v)
            self.ticks.add(m.Line(p, p + np.array([0.1, 0, 0]), color=MUTED, stroke_width=2))
            if grid and abs(self.fy(v) - self.lo[1]) > 1e-9:
                self.grid.add(m.Line(p, p + np.array([x_length, 0, 0]), color=TRACK, stroke_width=1))
            label = rf"10^{{{round(math.log10(v))}}}" if log_y else yfmt.format(v)
            self.numbers.add(M(label, size=num_size, color=MUTED).next_to(p, m.LEFT, buff=0.12))
        self.add_to_back(self.grid)
        self.add(self.ticks, self.numbers)
        self.center()

    def c2p(self, x: float, y: float) -> np.ndarray:
        o = self.x_axis.get_start()
        w = self.x_axis.get_end()[0] - o[0]
        h = self.y_axis.get_end()[1] - o[1]
        u = (self.fx(x) - self.lo[0]) / (self.hi[0] - self.lo[0])
        v = (self.fy(y) - self.lo[1]) / (self.hi[1] - self.lo[1])
        return o + np.array([u * w, v * h, 0.0])


def curve(ax: "m.Axes | Plot", xs, ys, colour: str, width: float = 4, dashed: bool = False) -> m.VMobject:
    """A polyline through data points (x, y) in the axes' coordinates."""
    line = m.VMobject(stroke_color=colour, stroke_width=width)
    line.set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
    return m.DashedVMobject(line, num_dashes=60) if dashed else line
