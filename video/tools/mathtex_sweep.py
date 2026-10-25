"""D3: typeset every formula of the slide deck with ManimGX's MathTex and report what fails.

Each maths block from build/inventory.json is split the way the scenes use it (align rows at \\\\, columns at &,
\\why{...} notes removed because the video shows them as text), its macros are expanded (texmacros.expand) and
then typeset. Failures are grouped by the command ManimGX names in its error.
usage: uv run --project video/scenes python -I video/tools/mathtex_sweep.py [--show N]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "video/scenes"))

import manimgx as m  # noqa: E402
from texmacros import expand  # noqa: E402

WHY = re.compile(r"\\why\{")


def drop_why(s: str) -> str:
    """Remove \\why{...} (balanced)."""
    out, i = [], 0
    while True:
        mm = WHY.search(s, i)
        if not mm:
            out.append(s[i:])
            return "".join(out)
        out.append(s[i:mm.start()])
        depth, j = 0, mm.end() - 1
        while True:
            if s[j] == "{" and s[j - 1] != "\\":
                depth += 1
            elif s[j] == "}" and s[j - 1] != "\\":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        i = j + 1


def split_top(s: str, sep: str) -> list[str]:
    """Split s at `sep` ("\\\\" or "&") only at brace depth 0 and outside nested \\begin...\\end."""
    parts, depth, env, start, i = [], 0, 0, 0, 0
    while i < len(s):
        if s.startswith("\\begin{", i):
            env += 1
        elif s.startswith("\\end{", i):
            env -= 1
        c = s[i]
        if c == "\\" and not s.startswith(sep, i):
            i += 2  # skip an escaped character / command start
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if depth == 0 and env == 0 and s.startswith(sep, i):
            parts.append(s[start:i])
            i += len(sep)
            if sep == "\\\\" and i < len(s) and s[i] == "[":  # \\[2pt]
                i = s.index("]", i) + 1
            start = i
            continue
        i += 1
    parts.append(s[start:])
    return parts


def pieces(block: str) -> list[str]:
    block = drop_why(block)
    out = []
    for r in split_top(block, "\\\\"):
        cells = [c.strip() for c in split_top(r, "&")]
        joined = " ".join(c for c in cells if c)
        if joined:
            out.append(joined)
    return out


def main() -> None:
    show = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 8
    inv = json.loads((ROOT / "video/build/inventory.json").read_text())
    total, failed = 0, []
    for fr in inv:
        for block in fr["maths"]:
            for p in pieces(block):
                src = expand(p)
                total += 1
                try:
                    m.MathTex(src)
                except Exception as e:  # noqa: BLE001 - we want every failure
                    failed.append((fr["file"], fr["title"], src, f"{type(e).__name__}: {e}"))
    print(f"typeset {total} formula pieces, {len(failed)} failed")
    reasons: Counter[str] = Counter()
    examples: dict[str, list] = defaultdict(list)
    for f in failed:
        msg = f[3]
        cmd = re.findall(r"\\[A-Za-z]+", msg)
        key = cmd[0] if cmd else msg[:80]
        reasons[key] += 1
        examples[key].append(f)
    for key, n in reasons.most_common():
        print(f"\n== {n:4d}  {key}")
        for f in examples[key][:show]:
            print(f"     [{f[0]}] {f[2][:110]!r}\n        -> {f[3][:160]}")
    out = ROOT / "video/build/mathtex_sweep.json"
    out.write_text(json.dumps({"total": total, "failed": failed}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
