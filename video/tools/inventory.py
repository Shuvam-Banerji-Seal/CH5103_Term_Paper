"""Inventory of the slide deck: every frame with its title, maths, figures and symbol strip.

The explainer video must cover every frame. This script turns presentation/sections/*.tex into
video/build/inventory.json, which the coverage test (video/tools/coverage.py) checks the video script against.
usage: python -I video/tools/inventory.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SECTIONS = sorted((ROOT / "presentation/sections").glob("*.tex"))


def balanced(s: str, i: int) -> tuple[str, int]:
    """Return the {...} group starting at s[i] == '{' and the index after it."""
    assert s[i] == "{", s[i:i + 20]
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "\\":
            continue
        if s[j] == "{" and (j == 0 or s[j - 1] != "\\"):
            depth += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    raise ValueError("unbalanced")


def frames(tex: str):
    for m in re.finditer(r"\\begin\{frame\}", tex):
        i = m.end()
        opts = ""
        if tex[i] == "[":
            k = tex.index("]", i)
            opts, i = tex[i + 1:k], k + 1
        title = subtitle = ""
        while i < len(tex) and tex[i] in " \t":
            i += 1
        if i < len(tex) and tex[i] == "{":
            title, i = balanced(tex, i)
            if i < len(tex) and tex[i] == "{":
                subtitle, i = balanced(tex, i)
        end = tex.index(r"\end{frame}", i)
        yield opts, title, subtitle, tex[i:end], m.start()


def maths(body: str) -> list[str]:
    out = []
    for m in re.finditer(r"\\begin\{(align\*?|equation\*?|gather\*?)\}(.*?)\\end\{\1\}", body, re.S):
        out.append(m.group(2).strip())
    out += [m.group(1).strip() for m in re.finditer(r"\\\[(.*?)\\\]", body, re.S)]
    out += [m.group(1).strip() for m in re.finditer(r"(?<!\\)\$(.+?)(?<!\\)\$", body, re.S)]
    return out


def main() -> None:
    inv = []
    for f in SECTIONS:
        tex = f.read_text()
        sec = re.search(r"\\section\{(.*?)\}", tex)
        for n, (opts, title, subtitle, body, pos) in enumerate(frames(tex)):
            strip = re.search(r"\\symbolstrip\{", body)
            inv.append({
                "file": f.name,
                "section": sec.group(1) if sec else "",
                "index": n,
                "line": tex[:pos].count("\n") + 1,
                "options": opts,
                "title": title.strip(),
                "subtitle": subtitle.strip(),
                "overlays": max([int(x) for x in re.findall(r"<(\d+)", body)] or [1]),
                "figures": re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body),
                "code": re.findall(r"\\inputminted(?:\[[^\]]*\])?\{[^}]+\}\{([^}]+)\}", body),
                "quotes": len(re.findall(r"\\begin\{paperclaim\}", body)),
                "maths": maths(body),
                "symbols": balanced(body, strip.end() - 1)[0] if strip else "",
                "body": body,
            })
    out = ROOT / "video/build/inventory.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inv, indent=1, ensure_ascii=False))
    by_sec: dict[str, int] = {}
    for fr in inv:
        by_sec[fr["file"]] = by_sec.get(fr["file"], 0) + 1
    for k, v in by_sec.items():
        print(f"{k:28s} {v:3d} frames")
    print(f"total {len(inv)} frames, {sum(len(fr['maths']) for fr in inv)} maths blocks, "
          f"{sum(len(fr['figures']) for fr in inv)} figures, {sum(fr['overlays'] for fr in inv)} overlay steps (max per frame summed)")


if __name__ == "__main__":
    main()
