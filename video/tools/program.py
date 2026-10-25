"""The program: chapters in order, each a title card followed by its scenes, with exact frame counts.

usage (from the repo root):
  python3 video/tools/program.py            # list chapters and scenes (no renders needed)
  python3 video/tools/program.py --probe    # read frame counts of video/build/scenes/<file>/<Scene>.mp4, write
                                            # video/build/program.json for the editor and the assembler
  python3 video/tools/program.py --probe --renders video/build/scenes4k --out video/build/program4k.json

A scene's frame count is the number of video frames ffprobe counts in its render; its audio must last exactly as
long (checked here: a scene whose narration ran past its last frame would drift the following scenes).
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENES = ROOT / "video" / "scenes"
RENDERS = ROOT / "video" / "build" / "scenes"
OUT = ROOT / "video" / "build" / "program.json"
FPS = 30
CARD_SECONDS = 3.0

# file stem -> (part label, chapter title); parts follow the deck's \section numbering (02-paper is Part I)
CHAPTERS = {
    "ch00_intro": ("Part I", "The paper"),
    "ch01_foundations": ("Part II", "Foundations"),
    "ch02_spin": ("Part III", "Spin & antisymmetry"),
    "ch03_two_electrons": ("Part IV", "Two electrons, two orbitals"),
    "ch04_energies": ("Part V", "Energies: J and K"),
    "ch05_holes": ("Part VI", "Fermi holes"),
    "ch06_hund": ("Part VII", "Hund’s rule"),
    "ch07_static": ("Part VIII", "Static correlation"),
    "ch08_kinetic": ("Part IX", "Kinetic exchange"),
    "ch09_nbmo": ("Part X", "NBMOs & disjointness"),
    "ch10_spinpol": ("Part XI", "Spin polarisation"),
    "ch11_exciting": ("Part XII", "Switching spin states"),
    "ch12_koopmans": ("Part XIII", "Koopmans & Janak"),
    "ch13_aufbau": ("Part XIV", "Aufbau on trial"),
    "ch14_quasi": ("Part XV", "Quasi-closed shells"),
    "ch15_bs": ("Part XVI", "Broken symmetry"),
    "ch16_verification": ("Part XVII", "Our verification"),
    "ch17_verdict": ("Part XVIII", "Verdict"),
    "ch18_tests": ("Appendix A", "Every test, line by line"),
    "ch19_lean": ("Appendix B", "The Lean proofs"),
}


def scene_classes(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [n.name for n in tree.body if isinstance(n, ast.ClassDef) and n.name != "Walk"
            and any(getattr(b, "id", "") in ("Frame", "Walk") for b in n.bases)]


def probe(mp4: Path) -> tuple[int, float, float]:
    """(video frames, video seconds, audio seconds) of a render."""
    def q(stream: str, entry: str, extra: list[str]) -> str:
        return subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, *extra, "-show_entries",
                               f"stream={entry}", "-of", "csv=p=0", str(mp4)], capture_output=True, text=True,
                              check=True).stdout.strip().split("\n")[0]
    frames = int(q("v:0", "nb_read_frames", ["-count_frames"]))
    vdur = float(q("v:0", "duration", []) or frames / FPS)
    a = q("a:0", "duration", [])
    return frames, vdur, float(a) if a else 0.0


def main() -> int:
    global RENDERS, OUT
    do_probe = "--probe" in sys.argv
    if "--renders" in sys.argv:
        RENDERS = ROOT / sys.argv[sys.argv.index("--renders") + 1]
    if "--out" in sys.argv:
        OUT = ROOT / sys.argv[sys.argv.index("--out") + 1]
    chapters, total, problems = [], 0, []
    for stem, (part, title) in CHAPTERS.items():
        path = SCENES / f"{stem}.py"
        scenes = []
        for cls in scene_classes(path):
            entry = {"id": cls, "file": stem}
            if do_probe:
                mp4 = RENDERS / stem / f"{cls}.mp4"
                if not mp4.exists():
                    problems.append(f"missing render {mp4.relative_to(ROOT)}")
                    continue
                frames, vdur, adur = probe(mp4)
                entry.update(frames=frames, video_seconds=round(vdur, 4), audio_seconds=round(adur, 4))
                if adur > frames / FPS + 0.05:
                    problems.append(f"{stem}:{cls}: audio {adur:.3f} s outlasts video {frames / FPS:.3f} s")
                total += frames
            scenes.append(entry)
        card = round(CARD_SECONDS * FPS)
        total += card if do_probe else 0
        chapters.append({"id": stem, "part": part, "title": title, "card_frames": card, "scenes": scenes})
        print(f"{part:11s} {title:32s} {len(scenes):3d} scenes")
    for p in problems:
        print("PROBLEM", p)
    if do_probe:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({"fps": FPS, "width": 1920, "height": 1080, "total_frames": total,
                                   "chapters": chapters}, indent=1) + "\n", encoding="utf-8")
        print(f"{total} frames = {total / FPS / 3600:.2f} h -> {OUT.relative_to(ROOT)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
