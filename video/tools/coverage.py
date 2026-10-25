"""Acceptance (a): every frame of the slide deck has its scene, exactly once.

usage: python3 video/tools/coverage.py      (exit 1 on a gap or a duplicate)

Each slide scene's docstring names its source: "NN-name.tex, frame k: 'title'." (k counts the frames of that
section file from 1). The frames themselves come from video/build/inventory.json (video/tools/inventory.py, which
parses presentation/sections/*.tex). Titles are compared after removing LaTeX markup; a differing title is listed
for review but is not an error (scene titles may spell out what the slide abbreviates).
"""
from __future__ import annotations

import ast
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENES = ROOT / "video" / "scenes"
DOC = re.compile(r"^(?P<file>\d\d-[\w-]+\.tex), frame (?P<k>\d+)(?:: '(?P<title>.*)')?")


def plain(s: str) -> str:
    s = re.sub(r"\\texorpdfstring\{([^}]*)\}\{[^}]*\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = re.sub(r"[{}$\\^_&~]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def main() -> int:
    frames = json.loads((ROOT / "video" / "build" / "inventory.json").read_text(encoding="utf-8"))
    per_file: Counter = Counter()
    want = {}
    for fr in frames:
        per_file[fr["file"]] += 1
        want[(fr["file"], per_file[fr["file"]])] = fr["title"]
    have: Counter = Counter()
    titles = {}
    for path in sorted(SCENES.glob("ch*.py")):
        for cls in [n for n in ast.parse(path.read_text(encoding="utf-8")).body if isinstance(n, ast.ClassDef)]:
            doc = ast.get_docstring(cls) or ""
            m = DOC.match(doc)
            if m:
                key = (m["file"], int(m["k"]))
                have[key] += 1
                titles[key] = (f"{path.name}:{cls.name}", m["title"] or "")
    missing = sorted(set(want) - set(have))
    extra = sorted(set(have) - set(want))
    dup = sorted(k for k, n in have.items() if n > 1)
    for k in missing:
        print(f"MISSING {k[0]} frame {k[1]}: {want[k]!r}")
    for k in extra:
        print(f"UNKNOWN {titles[k][0]} claims {k[0]} frame {k[1]}")
    for k in dup:
        print(f"DUPLICATE {k[0]} frame {k[1]}")
    differ = [(k, want[k], titles[k]) for k in sorted(set(want) & set(have))
              if titles[k][1] and plain(titles[k][1]) != plain(want[k])]
    for k, w, (where, t) in differ:
        print(f"  title differs  {where}: slide {w!r} / scene {t!r}")
    print(f"{len(want)} slide frames, {sum(have.values())} scenes claim one: {len(missing)} missing, {len(extra)} unknown, "
          f"{len(dup)} duplicated; {len(differ)} titles worded differently")
    return 1 if missing or extra or dup else 0


if __name__ == "__main__":
    sys.exit(main())
