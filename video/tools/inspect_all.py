"""Inspect every scene of one or more chapter files with `manimgx inspect` (storyboard + layout checks).

usage (from video/scenes): uv run --project . python -I ../tools/inspect_all.py ch00_intro.py [more files] [--only S01Journey]
Storyboards go to video/build/inspect/<file>/<Scene>.png; prints each scene's duration and layout problems and
exits 1 if any scene has a layout problem or an error.
"""
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENES = ROOT / "video" / "scenes"
OUT = ROOT / "video" / "build" / "inspect"


def scene_classes(path: Path) -> list[str]:
    tree = ast.parse(path.read_text())
    out = []
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name != "Walk" and any(getattr(b, "id", "") in ("Frame", "Walk") for b in n.bases):
            out.append(n.name)
    return out


def main() -> int:
    argv = sys.argv[1:]
    only = None
    if "--only" in argv:
        k = argv.index("--only")
        only = argv[k + 1].split(",")
        argv = argv[:k] + argv[k + 2:]
    args = [a for a in argv if not a.startswith("--")]
    env = {**os.environ, "VIDEO_VOICE": os.environ.get("VIDEO_VOICE", "draft")}
    bad = 0
    total = 0.0
    ends: list[str] = []
    for f in args:
        path = (SCENES / f).resolve()
        for cls in scene_classes(path):
            if only and cls not in only:
                continue
            out = OUT / path.stem / f"{cls}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(["manimgx", "inspect", str(path), cls, "-o", str(out)], cwd=SCENES, env=env,
                               capture_output=True, text=True)
            text = r.stdout + r.stderr
            dur = re.search(r":\s*\S+,\s*([\d.]+) s,", text)
            secs = float(dur.group(1)) if dur else 0.0
            total += secs
            problems = [l.strip() for l in text.splitlines() if re.match(r"\s*\[\d+\]", l)]
            status = "ok" if r.returncode == 0 else ("LAYOUT" if problems else "ERROR")
            if r.returncode != 0:
                bad += 1
            print(f"{status:6s} {path.name}:{cls:28s} {secs:7.1f} s  {out.relative_to(ROOT)}")
            for p in problems:
                print("         " + p)
            if status == "ERROR":
                print("\n".join("         " + l for l in text.strip().splitlines()[-12:]))
            if "--end" in sys.argv and status != "ERROR":
                end = OUT / path.stem / "end" / f"{cls}.png"
                end.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["manimgx", "inspect", str(path), cls, "-t", "end", "-o", str(end)], cwd=SCENES,
                               env=env, capture_output=True, text=True)
                ends.append(str(end))
    print(f"total {total / 60:.1f} min, {bad} scene(s) with problems")
    if ends:
        sheet = OUT / f"{'-'.join(Path(a).stem for a in args)}.endsheet.png"
        subprocess.run(["montage", *ends, "-tile", "3x", "-geometry", "640x360+3+3", "-background", "#333",
                        str(sheet)], check=False)
        print(f"end-frame sheet: {sheet.relative_to(ROOT)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
