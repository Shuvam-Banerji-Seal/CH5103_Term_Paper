"""Run the rest of the video build unattended: narration → alignment → Whisper check (with automatic re-synthesis
of broken lines) → scene renders → frame counts → cards and HUD → assembly → QA.

usage (from the repo root): python3 video/tools/pipeline.py [--from STAGE] [--to STAGE]
stages: wait tts align asr render probe editor assemble qa

Every stage is resumable (each tool skips finished work), so the pipeline can be restarted at any time; a reboot
clears /tmp, so logs live in video/build/logs/: <stage>.log per stage, and pipeline.status, one line per event
("HH:MM:SS stage state detail"), which is what the monitor watches. Exit 0 when QA passes; otherwise the failing
stage is named in the status file and the exit code is 1.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "video" / "build" / "logs"
STORE = ROOT / "video" / "build" / "tts" / "store"
STATUS = LOGS / "pipeline.status"
STAGES = ["wait", "tts", "align", "asr", "render", "probe", "editor", "assemble", "qa"]
TTS = ["uv", "run", "--project", "video/tts", "python", "-E", "-s", "-u", "video/tts/synth.py", "batch", "--threads",
       "8", "--cfg", "1"]
TTS_SETTINGS = [["--batch", "24", "--depth", "bf16"], ["--batch", "8", "--depth", "int8"],
                ["--batch", "4", "--depth", "int8"]]   # after an OOM kill, try leaner settings
REGEN_WER = 0.5      # Whisper word error rate above which a line is treated as broken and re-synthesised
REGEN_ROUNDS = 2


def status(stage: str, state: str, detail: str = "") -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%H:%M:%S')} {stage} {state} {detail}".rstrip()
    with STATUS.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def run(stage: str, cmd: list[str], env: dict | None = None, progress: str | None = None, cwd: Path = ROOT) -> int:
    """Run a command, logging to <stage>.log; lines matching `progress` are also written to the status file."""
    log = LOGS / f"{stage}.log"
    pat = re.compile(progress) if progress else None
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"\n===== {time.strftime('%F %T')} {' '.join(cmd)}\n")
        p = subprocess.Popen(cmd, cwd=cwd, env={**os.environ, **(env or {})}, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in p.stdout:
            fh.write(line)
            fh.flush()
            if pat and pat.search(line):
                status(stage, "progress", line.strip()[:160])
        return p.wait()


def remaining_lines() -> int:
    r = subprocess.run(["uv", "run", "--project", "video/scenes", "python", "-I", "video/tools/collect_lines.py", "--write"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"collect_lines failed:\n{r.stdout}{r.stderr}")
    reqs = [json.loads(l) for l in (ROOT / "video/build/tts/requests.jsonl").read_text().splitlines() if l]
    missing = 0
    for q in reqs:
        meta = STORE / f"{q['key']}.json"
        if not (STORE / f"{q['key']}.wav").exists() or not meta.exists() or json.loads(meta.read_text())["text"] != q["text"]:
            missing += 1
    return missing


def stage_wait() -> bool:
    # a synthesis or alignment started by hand must finish first: two heavy jobs at once get OOM-killed
    while True:
        busy = subprocess.run(["pgrep", "-f", "video/tts/(synth|align)\\.py"], capture_output=True, text=True).stdout.split()
        busy = [b for b in busy if int(b) != os.getpid()]
        if not busy:
            return True
        time.sleep(30)


def stage_tts(seed: int = 42) -> bool:
    for attempt in range(6):
        left = remaining_lines()
        status("tts", "check", f"{left} lines to synthesise")
        if left == 0:
            return True
        settings = TTS_SETTINGS[min(attempt, len(TTS_SETTINGS) - 1)]
        rc = run("tts", TTS + settings + ["--seed", str(seed)], env={"OMP_NUM_THREADS": "8"},
                 progress=r"^batch \d+:")
        status("tts", "exit", f"code {rc} with {' '.join(settings)}")
        if rc not in (0, 137, -9):
            return False
    return remaining_lines() == 0


def stage_align() -> bool:
    rc = run("align", ["uv", "run", "--project", "video/tts", "python", "-E", "-s", "-u", "video/tts/align.py", "--threads",
                       "8"], env={"OMP_NUM_THREADS": "8"}, progress=r"^aligned |FAIL")
    return rc == 0


def records() -> list[tuple[Path, dict]]:
    keys = {json.loads(l)["key"] for l in (ROOT / "video/build/tts/requests.jsonl").read_text().splitlines() if l}
    return [(p, json.loads(p.read_text())) for p in sorted(STORE.glob("*.json")) if p.stem in keys]


def stage_asr() -> bool:
    for rnd in range(REGEN_ROUNDS + 1):
        rc = run("asr", ["uv", "run", "--project", "video/tts", "python", "-E", "-s", "-u", "video/tts/asr.py"],
                 env={"OMP_NUM_THREADS": "8"}, progress=r"lines over WER")
        if rc != 0:
            return False
        recs = records()
        broken = [(p, r) for p, r in recs if r.get("asr", {}).get("wer", 0) > REGEN_WER or not r.get("words")]
        review = [(p, r) for p, r in recs if 0.12 < r.get("asr", {}).get("wer", 0) <= REGEN_WER]
        with (LOGS / "asr_review.txt").open("w", encoding="utf-8") as f:
            for p, r in sorted(review + broken, key=lambda x: -x[1].get("asr", {}).get("wer", 1)):
                a = r.get("asr", {})
                f.write(f"{p.stem} wer {a.get('wer')} {a.get('seconds')} s\n  said:  {r['text']}\n  heard: {a.get('heard')}\n")
        status("asr", "round", f"{rnd}: {len(broken)} broken (WER > {REGEN_WER} or unaligned), {len(review)} to review")
        if not broken or rnd == REGEN_ROUNDS:
            return True
        for p, _ in broken:  # drop them; synthesise again with another seed, then align and check again
            p.unlink(missing_ok=True)
            p.with_suffix(".wav").unlink(missing_ok=True)
        if not stage_tts(seed=1000 + 97 * (rnd + 1)) or not stage_align():
            return False
    return True


def stage_render() -> bool:
    for attempt in range(2):
        rc = run("render", ["uv", "run", "--project", "video/scenes", "python", "-I", "video/tools/render_all.py"],
                 progress=r"^(ok|FAIL) |scenes rendered")
        if rc == 0:
            return True
        status("render", "retry", f"attempt {attempt + 1} had failures")
    return False


def stage_probe() -> bool:
    return run("probe", ["python3", "video/tools/program.py", "--probe"], progress=r"frames = |PROBLEM") == 0


def stage_editor() -> bool:
    ed = ROOT / "video" / "editor"
    if not (ed / "node_modules").exists() and run("editor", ["bun", "install"], cwd=ed) != 0:
        return False
    return (run("editor", ["bun", "scripts/render.ts", "cards"], cwd=ed, progress=r"frames$") == 0
            and run("editor", ["bun", "scripts/render.ts", "hud"], cwd=ed, progress=r"HUD overlays") == 0)


def stage_assemble() -> bool:
    return run("assemble", ["bun", "scripts/assemble.ts"], cwd=ROOT / "video" / "editor",
               progress=r"^v \d+/\d+ .*card|narration loudness|^frames |^video |^size ") == 0


def stage_qa() -> bool:
    return run("qa", ["uv", "run", "--project", "video/tts", "python", "-E", "-s", "video/tools/qa.py"],
               progress=r"^\[(ok|FAIL)\]") == 0


def main() -> int:
    argv = sys.argv[1:]
    start = STAGES.index(argv[argv.index("--from") + 1]) if "--from" in argv else 0
    stop = STAGES.index(argv[argv.index("--to") + 1]) if "--to" in argv else len(STAGES) - 1
    status("pipeline", "start", f"stages {STAGES[start]}..{STAGES[stop]}")
    for stage in STAGES[start:stop + 1]:
        t0 = time.time()
        status(stage, "begin")
        try:
            ok = globals()[f"stage_{stage}"]()
        except Exception as e:  # noqa: BLE001 - report and stop, so the monitor sees it
            status(stage, "error", f"{type(e).__name__}: {e}"[:200])
            ok = False
        status(stage, "done" if ok else "FAILED", f"{(time.time() - t0) / 60:.1f} min")
        if not ok:
            status("pipeline", "STOPPED", f"at {stage}; see video/build/logs/{stage}.log")
            return 1
    status("pipeline", "FINISHED", "all stages passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
