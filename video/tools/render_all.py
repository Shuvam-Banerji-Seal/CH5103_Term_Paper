"""Render every scene with the final narration (VIDEO_VOICE=final) at 1080p, 30 fps, into video/build/scenes/.

usage (from the repo root): uv run --project video/scenes python -I video/tools/render_all.py [--only ch03_two_electrons]
                            [--force] [--crf 12] [--preset veryfast] [--res 3840x2160 --out video/build/scenes4k]

A scene is rendered again only when its chapter file, the theme (noir.py, texmacros.py, voice.py) or the narration
store changed since its last render (a stamp file beside the video records them). Each render runs in its own
`manimgx render` process; a failure is reported and the next scene continues, and the run exits 1 at the end.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENES = ROOT / "video" / "scenes"
OUT = ROOT / "video" / "build" / "scenes"
sys.path.insert(0, str(ROOT / "video" / "tools"))
sys.path.insert(0, str(SCENES))

from program import CHAPTERS, FPS, scene_classes  # noqa: E402
from voice import store_digest  # noqa: E402


def digest(*paths: Path) -> str:
    h = hashlib.sha256()
    for p in paths:
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def main() -> int:
    argv = sys.argv[1:]
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    crf = argv[argv.index("--crf") + 1] if "--crf" in argv else "12"
    # intermediates: every scene is encoded once more, with the final settings, by the assembler
    preset = argv[argv.index("--preset") + 1] if "--preset" in argv else "veryfast"
    res = argv[argv.index("--res") + 1] if "--res" in argv else "1920x1080"
    out = ROOT / argv[argv.index("--out") + 1] if "--out" in argv else OUT
    force = "--force" in argv
    theme = digest(SCENES / "noir.py", SCENES / "texmacros.py", SCENES / "voice.py")
    store = store_digest()
    env = {**os.environ, "VIDEO_VOICE": "final"}
    failures, done, t_all = [], 0, time.time()
    for stem in CHAPTERS:
        if only and stem not in only:
            continue
        src = SCENES / f"{stem}.py"
        deps = [src] + ([SCENES / "ch18_tests.py"] if stem == "ch19_lean" else [])
        stamp_value = {"chapter": digest(*deps), "theme": theme, "store": store, "fps": FPS, "crf": crf, "res": res, "preset": preset}
        for cls in scene_classes(src):
            mp4 = out / stem / f"{cls}.mp4"
            stamp = mp4.with_suffix(".stamp.json")
            if not force and mp4.exists() and stamp.exists() and json.loads(stamp.read_text()) == stamp_value:
                continue
            mp4.parent.mkdir(parents=True, exist_ok=True)
            t0 = time.time()
            r = subprocess.run(["manimgx", "render", src.name, cls, "-r", res, "--fps", str(FPS), "--crf", crf, "--preset", preset,
                                "-o", str(mp4)], cwd=SCENES, env=env, capture_output=True, text=True)
            if r.returncode != 0 or not mp4.exists():
                failures.append(f"{stem}:{cls}")
                print(f"FAIL {stem}:{cls}\n{(r.stdout + r.stderr)[-1500:]}", flush=True)
                continue
            stamp.write_text(json.dumps(stamp_value))
            done += 1
            print(f"ok   {stem}:{cls} in {time.time() - t0:.0f} s  ({done} rendered, {(time.time() - t_all) / 60:.1f} min)",
                  flush=True)
    print(f"{done} scenes rendered, {len(failures)} failed: {' '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
