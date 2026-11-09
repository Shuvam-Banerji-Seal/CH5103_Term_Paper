"""The narration script as a handout: every line the voice speaks, scene by scene, beside the slide it narrates.

usage (from the repo root): video/scenes/.venv/bin/python -I video/tools/script_handout.py
then:                       make -C presentation script      (-> presentation/ch5103-script.pdf)

Sources, all of them the ones the video was built from:
  * the lines: the first argument of every say() in video/scenes/ch*.py, read statically by collect_lines.lines()
    (exactly the text handed to Breeze-TTS-2);
  * their order and timing: each scene's subtitle file, video/build/scenes/<file>/<Scene>.srt, written while the scene
    rendered, so a line's time is when the voice starts it; the scene's place in the programme comes from
    video/editor/public/program.json (chapter cards and scene lengths, in frames);
  * the slide: each scene's docstring names its frame ("05-two-electrons.tex, frame 6"), turned into a page of
    presentation/ch5103-handout.pdf by counting frames and section dividers in presentation/main.tex's \\input order.
    Every mapping is checked against the text pdftotext finds on that page.

Writes presentation/script/body.tex and stats.tex (included by presentation/script/script.tex) and prints a summary. Stops with
an error if any line is missing from its scene's subtitles, any slide page does not carry its frame's title,
or a file an appendix scene reads is not in the repository.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from collect_lines import SCENES, lines  # noqa: E402
from texmacros import expand  # noqa: E402  (video/scenes is on the path)

PROGRAM = ROOT / "video/editor/public/program.json"
SRT_DIR = ROOT / "video/build/scenes"
DECK = ROOT / "presentation"
HANDOUT = DECK / "ch5103-handout.pdf"
OUT = DECK / "script/body.tex"
STATS = DECK / "script/stats.tex"
PRESENTER = DECK / "script/presenter-body.tex"
PRESENTER_SLIDES = (10, 130)   # the slides (footer numbers, inclusive) the presenter script covers
FPS = 30
UNTITLED = {"S00Title": "Uncommon Molecular Electronic Configurations", "S135ThankYou": "Thank you"}  # no TITLE


# ----------------------------------------------------------------------------------------------- scenes (static)
def scene_info() -> dict[str, dict]:
    """For every scene class: file, TITLE, SUBTITLE, slide reference from the docstring, and the files a Walk scene
    reads (its STEPS)."""
    info = {}
    for path in sorted(SCENES.glob("ch*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        consts = {t.id: n.value.value for n in tree.body if isinstance(n, ast.Assign)
                  and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)
                  for t in n.targets if isinstance(t, ast.Name)}
        for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
            attrs, files = {}, []
            for node in cls.body:
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    name = node.targets[0].id
                    if name in ("TITLE", "SUBTITLE"):
                        attrs[name] = ast.literal_eval(node.value)
                    elif name == "STEPS":
                        for step in node.value.elts:
                            kind = step.elts[0].value
                            if kind in ("code", "out"):   # Walk reads code from V + path, output from R + path
                                arg = step.elts[1]
                                name = consts[arg.id] if isinstance(arg, ast.Name) else _joined(arg, consts)
                                files.append(("verification/" if kind == "code" else "verification/results/") + name)
            doc = ast.get_docstring(cls) or ""
            ref = re.match(r"(\d\d-[\w-]+)\.tex, frame (\d+): (?:'(.+)'\.)?", doc)
            info[cls.name] = {"file": path.stem, "title": attrs.get("TITLE") or UNTITLED.get(cls.name, ""),
                              "subtitle": attrs.get("SUBTITLE", ""),
                              "slide": (ref.group(1), int(ref.group(2))) if ref else None,
                              "slide_title": (ref.group(3) or "") if ref else "",
                              "reads": list(dict.fromkeys(files))}
    return info


def _joined(node: ast.AST, consts: dict) -> str:
    """V + "t1_spin.py" style paths in STEPS."""
    if isinstance(node, ast.BinOp):
        return _joined(node.left, consts) + _joined(node.right, consts)
    if isinstance(node, ast.Name):
        return consts[node.id]
    return node.value


# ----------------------------------------------------------------------------------------------- slides
def slide_pages() -> tuple[dict[tuple[str, int], tuple[int, int | None]], int]:
    """(section file, frame in file) -> (page of the handout PDF, frame number printed in the deck's footer, or None
    for a [noframenumbering] frame: the title and closing slides), and the number of numbered frames.
    Each section file opens with \\section, which inserts a divider page (AtBeginSection, noframenumbering)."""
    order = re.findall(r"\\input\{sections/([\w-]+)\}", (DECK / "main.tex").read_text(encoding="utf-8"))
    pages, page, number = {}, 0, 0
    for name in order:
        src = "\n".join(l.split("%")[0] if not l.lstrip().startswith("%") else ""
                        for l in (DECK / "sections" / f"{name}.tex").read_text(encoding="utf-8").splitlines())
        k = 0
        for tok in re.findall(r"\\section\{|\\begin\{frame\}(?:\[[^\]]*\])?", src):
            page += 1
            if tok.startswith("\\begin"):
                k += 1
                numbered = "noframenumbering" not in tok
                number += numbered
                pages[(name, k)] = (page, number if numbered else None)
    return pages, number


def page_text(page: int) -> str:
    return subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), str(HANDOUT), "-"],
                          capture_output=True, text=True, check=True).stdout


def squeeze(s: str) -> str:
    """Letters and digits only, lower case, after NFKD (pdftotext gives maths as 𝑀𝑆, ₂, 𝑧̂: NFKD makes them MS, 2, z + a mark) and
    with LaTeX control words (\\hat, \\text, \\ge) dropped, so "$M_S=\\pm1$: one" and "𝑀𝑆 = ±1: one" agree."""
    s = re.sub(r"\\[a-zA-Z]+", "", unicodedata.normalize("NFKD", s))
    return "".join(re.findall(r"[a-z0-9]", s.lower()))


def check_slide(page: int, titles: list[str], number: int | None, total: int) -> bool:
    """The page carries the frame's title (the scene's TITLE or the docstring's frame title, squeezed, is a substring
    of the squeezed page text) and its footer reads "number / total" (an unnumbered frame: no such counter)."""
    text = squeeze(page_text(page))
    corner = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-x", "380", "-y", "236", "-W", "74",
                             "-H", "19", str(HANDOUT), "-"], capture_output=True, text=True, check=True).stdout
    counter = re.findall(rf"(\d+)\s*/\s*{total}", corner)   # the footer's counter, bottom right of the frame
    footer_ok = counter == [str(number)] if number else not counter
    return footer_ok and any(squeeze(t) and squeeze(t) in text for t in titles)


# ----------------------------------------------------------------------------------------------- timing
def srt_cues(path: Path) -> list[tuple[float, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        rows = block.strip().splitlines()
        if len(rows) < 3:
            continue
        h, mi, s, ms = map(int, re.match(r"(\d+):(\d+):(\d+),(\d+)", rows[1]).groups())
        cues.append((h * 3600 + mi * 60 + s + ms / 1000, " ".join(rows[2:])))
    return cues


def ordered_lines(scene: str, file: str, said: list[str]) -> list[tuple[float, str]]:
    """The scene's lines in spoken order, each with the time (s, from the scene's start) its first caption begins."""
    cues = srt_cues(SRT_DIR / file / f"{scene}.srt")
    stream, starts = "", []
    for t, text in cues:
        starts.append((len(stream), t))
        stream += re.sub(r"\s+", " ", text).strip() + " "
    found, used = [], set()
    for text in said:
        pos = stream.find(text)
        while pos in used:
            pos = stream.find(text, pos + 1)
        if pos < 0:
            raise SystemExit(f"{scene}: line not in its subtitles:\n  {text}")
        used.add(pos)
        t = max(t for p, t in starts if p <= pos)
        found.append((pos, t, text))
    covered = sum(len(text) + 1 for _, _, text in found)
    if covered != len(stream):
        raise SystemExit(f"{scene}: subtitles hold {len(stream)} characters, the lines {covered}")
    return [(t, text) for _, t, text in sorted(found)]


# ----------------------------------------------------------------------------------------------- LaTeX
SPECIAL = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
           "^": r"\textasciicircum{}", "\\": r"\textbackslash{}"}


def esc(s: str) -> str:
    s = "".join(SPECIAL.get(c, c) for c in s)
    s = re.sub(r"(?<=\w)'(?=\w)", "\u2019", s)      # Gryn'ova, Hund's
    s = re.sub(r"(^|[\s(])'", "\\1\u2018", s)
    s = s.replace("'", "\u2019")
    s = re.sub(r'(^|[\s(])"', "\\1\u201c", s).replace('"', "\u201d")
    return s


def tex_inline(s: str) -> str:
    """A scene TITLE/SUBTITLE: $maths$ kept, the text escaped, `code` / **strong** / *emphasis* as in noir.rich."""
    parts = re.split(r"(\$[^$]+\$)", s)
    out = []
    for i, p in enumerate(parts):
        if i % 2:
            out.append(expand(p))      # the deck's macros (\\eri, \\Eh, \\braket ...) written out, as in the video
            continue
        p = esc(p).replace("∝", r"$\propto$")       # not in Libertinus Serif's text fonts
        p = re.sub(r"`([^`]+)`", r"\\texttt{\1}", p)
        p = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", p)
        p = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"\\emph{\1}", p)
        out.append(p)
    return "".join(out)


UNI = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "Delta": "Δ", "lambda": "λ", "mu": "μ", "nu": "ν",
       "pi": "π", "sigma": "σ", "chi": "χ", "varphi": "φ", "Psi": "Ψ", "pm": "±", "le": "≤", "ge": "≥", "neq": "≠",
       "times": "×", "to": "→", "infty": "∞", "approx": "≈", "gg": "≫", "cdots": "⋯", "langle": "⟨", "rangle": "⟩",
       "vert": "|", "sin": "sin ", "sqrt": "√"}


def plain(s: str) -> str:
    """A title as plain Unicode text, for PDF bookmarks (which cannot hold typeset maths)."""
    out = []
    for i, p in enumerate(re.split(r"(\$[^$]+\$)", s)):
        if i % 2:
            m = expand(p[1:-1]).replace("^2", "²")
            m = re.sub(r"\\(?:text|mathrm|mathbf)\{([^}]*)\}", r"\1", m)
            m = re.sub(r"\\tfrac\{([^}]*)\}\{([^}]*)\}", r"\1/\2", m)
            m = re.sub(r"\\([a-zA-Z]+)", lambda k: UNI.get(k.group(1), ""), m)
            out.append(re.sub(r"[{}^_\\]", "", m).replace(" ", ""))
        else:
            out.append(re.sub(r"[`*]", "", p))
    return esc(re.sub(r"\s+", " ", "".join(out)).strip())


# ------------------------------------------------------------------ presenter script: what gets highlighted
# Key terms (as the voice says them), bold at their first appearance on each slide.
TERMS = ["Hund's rule", "Hund's multiplicity rule", "open-shell singlet", "triplet", "singlet", "closed-shell",
         "closed shell", "closed shells", "open shell", "open shells", "high spin", "low spin", "diradical", "diradicals", "exchange integral K", "exchange integral", "Coulomb integral",
         "Slater determinant", "antisymmetric", "antisymmetry", "Pauli", "dynamic spin polarisation",
         "spin polarisation", "kinetic exchange", "superexchange", "static correlation", "dynamic correlation",
         "disjoint", "nondisjoint", "N B M Os", "N B M O", "non-bonding molecular orbitals", "Fermi hole",
         "virial theorem", "less screening", "frozen orbitals", "variational principle", "Hückel", "pairing theorem",
         "zero-sum rule", "Ovchinnikov", "Lieb", "Koopmans", "Janak", "non-aufbau", "aufbau", "SOMO", "HOMO", "LUMO",
         "quasi-closed-shell", "quasi-closed", "distonic", "broken-symmetry", "broken symmetry", "Yamaguchi", "Hubbard",
         "restricted open-shell", "unrestricted", "full configuration interaction", "configuration interaction",
         "multiplicity", "Hamiltonian", "spin eigenfunction", "density functional", "ionic", "covalent", "alternant",
         "redox", "protonation", "Lean", "SymPy", "PySCF"]
# Errors and mistakes (the review's, and those our tests caught in our own work): bold, underlined, every time.
ERRORS = ["sign error", "erratum", "wrong", "mistake", "typo", "slip"]
# A sentence that lands a point: highlighted.
TAKEAWAY = re.compile(r"(So|Therefore|Hence|Thus|In short|In other words|The lesson|The point|The upshot|The answer|"
                      r"The verdict|That is why|This is why|The conclusion)\b")
# Structure cues in derivations and the aufbau trial: bold.
CUE = re.compile(r"\b(Step (?:one|two|three|four|five|six|seven|eight|nine|ten)\.|Exhibit [ABC]\b)")
_TERM = re.compile(r"(?<![\w-])(" + "|".join(sorted(map(re.escape, TERMS + ERRORS), key=len, reverse=True))
                   + r")(?![\w-])", re.I)
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
MARK_COUNTS = {"term": 0, "error": 0, "takeaway": 0, "cue": 0}


def mark(text: str, used: set[str]) -> str:
    """One line for the presenter script: the verbatim text, escaped, with the highlighting rules applied."""
    errors = {e.lower() for e in ERRORS}
    sentences = SENTENCE.split(text)
    assert " ".join(sentences) == text           # whitespace is single spaces (collect_lines.spoken)

    def term(m: re.Match) -> str:
        w = m.group(1)
        if w.lower() in errors:
            MARK_COUNTS["error"] += 1
            return f"\x05{w}\x06"
        if w.lower() in used:
            return w
        used.add(w.lower())
        MARK_COUNTS["term"] += 1
        return f"\x03{w}\x04"

    out = []
    for sent in sentences:
        s = _TERM.sub(term, sent)
        s, n = CUE.subn(lambda m: f"\x07{m.group(1)}\x08", s)
        MARK_COUNTS["cue"] += n
        if TAKEAWAY.match(sent):
            MARK_COUNTS["takeaway"] += 1
            s = f"\x01{s}\x02"
        out.append(s)
    s = esc(" ".join(out))
    for a, b in (("\x01", r"\Take{"), ("\x02", "}"), ("\x03", r"\textbf{"), ("\x04", "}"), ("\x05", r"\Err{"),
                 ("\x06", "}"), ("\x07", r"\textbf{"), ("\x08", "}")):
        s = s.replace(a, b)
    return s


def stamp(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}"


def main() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    info = scene_info()
    pages, numbered = slide_pages()
    said: dict[str, list[str]] = {}
    for _, cls, text in lines():
        said.setdefault(cls, []).append(text)

    body, frame, n_lines, n_words, bad, missing = [], 0, 0, 0, [], []
    presenter, n_presenter, n_pslides = [], 0, 0
    for ch in program["chapters"]:
        ch_start = frame / FPS
        frame += ch["card_frames"]
        ch_end = (frame + sum(s["frames"] for s in ch["scenes"])) / FPS
        body.append(f"\\Part{{{esc(ch['part'])}}}{{{tex_inline(ch['title'])}}}{{{stamp(ch_start)}}}"
                    f"{{{stamp(ch_end)}}}")
        part_head = (f"\\PPart{{{esc(ch['part'])}: {tex_inline(ch['title'])}}}{{{esc(ch['part'])}: "
                     f"{plain(ch['title'])}}}")      # written before the part's first slide in the presenter range
        letter, k = ch["part"].split()[-1] if ch["part"].startswith("Appendix") else "", 0
        for sc in ch["scenes"]:
            start, end = frame / FPS, (frame + sc["frames"]) / FPS
            frame += sc["frames"]
            meta = info[sc["id"]]
            spoken = ordered_lines(sc["id"], sc["file"], said.get(sc["id"], []))
            if meta["slide"]:
                page, number = pages[meta["slide"]]
                if not check_slide(page, [meta["title"], meta["slide_title"]], number, numbered):
                    bad.append((sc["id"], page, meta["title"]))
                source = f"presentation/sections/{meta['slide'][0]}.tex, frame {meta['slide'][1]}"
                label = f"Slide {number}" if number else ("Title slide" if page == 1 else "Closing slide")
                if number and PRESENTER_SLIDES[0] <= number <= PRESENTER_SLIDES[1]:
                    if part_head:
                        presenter.append(part_head)
                        part_head = ""
                    presenter.append(f"\\PSlide{{{label}}}{{{tex_inline(meta['title'])}}}"
                                     f"{{{label}: {plain(meta['title'])}}}")
                    used: set[str] = set()
                    for _, text in spoken:
                        presenter.append(f"\\PLine{{{mark(text, used)}}}")
                        n_presenter += 1
                    n_pslides += 1
                body.append(f"\\Slide{{{label}}}{{{number or ''}}}{{{page}}}{{{tex_inline(meta['title'])}}}"
                            f"{{{tex_inline(meta['subtitle'])}}}{{{stamp(start)}}}{{{stamp(end)}}}"
                            f"{{\\texttt{{{esc(source)}}}\\ \\ ·\\ \\ scene \\texttt{{{esc(sc['id'])}}}}}"
                            f"{{{plain(meta['title'])}}}")
            else:
                files = meta["reads"]
                missing += [f for f in files if not (ROOT / f).is_file()]
                reads = ", ".join(f"\\path{{{f}}}" for f in files)
                k += 1
                body.append(f"\\VideoOnly{{{letter}{k}}}{{{tex_inline(meta['title'])}}}{{{tex_inline(meta['subtitle'])}}}"
                            f"{{{stamp(start)}}}{{{stamp(end)}}}{{{reads}}}{{{esc(sc['id'])}}}"
                            f"{{{plain(meta['title'])}}}")
            for t, text in spoken:
                body.append(f"\\Line{{{stamp(start + t)}}}{{{esc(text)}}}")
                n_lines += 1
                n_words += len(text.split())
            body.append("\\EndScene")
    if bad:
        for scene, page, title in bad:
            print(f"slide check failed: {scene} -> page {page}: {title}")
        raise SystemExit(1)
    if missing:
        raise SystemExit(f"files named by Walk scenes but not in the repository: {missing}")
    if frame != program["total_frames"]:
        raise SystemExit(f"programme frames {frame} != total_frames {program['total_frames']}")
    if n_lines != len(lines()):
        raise SystemExit(f"{n_lines} lines placed, {len(lines())} say() calls")

    n_scenes = sum(len(c["scenes"]) for c in program["chapters"])
    n_slides = sum(1 for c in program["chapters"] for s in c["scenes"] if info[s["id"]]["slide"])
    gen = "% generated by video/tools/script_handout.py -- do not edit\n"
    header = (gen + f"\\def\\ScriptScenes{{{n_scenes}}}\\def\\ScriptSlides{{{n_slides}}}\\def\\ScriptLines{{{n_lines}}}"
              f"\\def\\ScriptWords{{{n_words:,}}}\\def\\ScriptLength{{{stamp(frame / FPS)}}}\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    STATS.write_text(header, encoding="utf-8")
    OUT.write_text(gen + "\n".join(body) + "\n", encoding="utf-8")
    PRESENTER.write_text(gen + "\n".join(presenter) + "\n", encoding="utf-8")
    print(f"presenter script: slides {PRESENTER_SLIDES[0]}-{PRESENTER_SLIDES[1]} ({n_pslides}), {n_presenter} lines; "
          f"marked {MARK_COUNTS}")
    print(f"{n_scenes} scenes ({n_slides} with a slide, every slide page checked), {n_lines} lines, {n_words} words, "
          f"{stamp(frame / FPS)} -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
