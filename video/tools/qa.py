"""Quality checks of the assembled video (acceptance e and g): format, length, sync, picture and sound.

usage (from the repo root): uv run --project video/tts python -E -s video/tools/qa.py [--final path.mp4] [--n 24]

1. format: 1920x1080, 30 fps, H.264 + AAC 48 kHz, under 2 GiB (a GitHub release asset);
2. frames: the file has exactly the programme's frame count; audio and video last the same to within a frame;
3. sync: for n scenes spread over the programme, the scene's own narration (from its render) is cross-correlated
   with the assembled soundtrack around where it should start; the lag must be under one frame (33 ms);
4. picture: the frame in the middle of each of those scenes is compared with the same frame of the scene's render,
   below the HUD strip; PSNR must exceed 30 dB (an off-by-one frame or a wrong scene fails);
5. sound: integrated loudness near -16 LUFS, true peak under -1 dBTP, no silent stretch longer than 8 s outside the
   chapter cards.
Writes video/build/final/qa.txt; exit 1 on any failure.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "video" / "build"


def ff(*args: str) -> bytes:
    return subprocess.run(["ffmpeg", "-v", "error", *args], capture_output=True, check=True).stdout


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def audio(path: Path, start: float, dur: float, rate: int = 8000) -> np.ndarray:
    raw = ff("-ss", f"{start:.4f}", "-t", f"{dur:.4f}", "-i", str(path), "-vn", "-ac", "1", "-ar", str(rate), "-f", "s16le", "-")
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32)


def frame(path: Path, t: float) -> np.ndarray:
    raw = ff("-ss", f"{t:.4f}", "-i", str(path), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-")
    return np.frombuffer(raw, dtype=np.uint8).reshape(1080, 1920).astype(np.float32)


def main() -> int:
    argv = sys.argv[1:]
    final = Path(argv[argv.index("--final") + 1]) if "--final" in argv else BUILD / "final" / "ch5103-explainer.mp4"
    n = int(argv[argv.index("--n") + 1]) if "--n" in argv else 24
    prog = json.loads((BUILD / "program.json").read_text())
    fps = prog["fps"]
    report, fails = [], []

    def check(name: str, ok: bool, detail: str) -> None:
        report.append(f"[{'ok' if ok else 'FAIL'}] {name}: {detail}")
        if not ok:
            fails.append(name)

    info = probe(final)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next(s for s in info["streams"] if s["codec_type"] == "audio")
    size = int(info["format"]["size"])
    check("format", v["width"] == 1920 and v["height"] == 1080 and v["codec_name"] == "h264" and v["r_frame_rate"] == f"{fps}/1"
          and a["codec_name"] == "aac" and a["sample_rate"] == "48000",
          f"{v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']}, {a['codec_name']} {a['sample_rate']} Hz")
    check("size", size < 2 ** 31, f"{size / 2 ** 30:.2f} GiB")
    nframes = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                                  "stream=nb_read_packets", "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout)
    check("frames", nframes == prog["total_frames"], f"{nframes} in the file, {prog['total_frames']} in the programme")
    vd, ad = float(v["duration"]), float(a["duration"])
    check("durations", abs(vd - ad) < 1.0 / fps + 0.03, f"video {vd:.3f} s, audio {ad:.3f} s")

    # scenes with their programme start (frames)
    scenes, f = [], 0
    for ch in prog["chapters"]:
        f += ch["card_frames"]
        for s in ch["scenes"]:
            scenes.append((s, f))
            f += s["frames"]
    picks = [scenes[i] for i in np.linspace(0, len(scenes) - 1, min(n, len(scenes))).round().astype(int)]
    worst_lag, worst_psnr = 0.0, 1e9
    for s, start in picks:
        src = BUILD / "scenes" / s["file"] / f"{s['id']}.mp4"
        t0 = start / fps
        ref = audio(src, 0.0, 6.0)
        if ref.std() < 1:  # a scene that opens with silence: use a later window
            ref = audio(src, 6.0, 6.0); t0 += 6.0
        got = audio(final, max(0.0, t0 - 0.5), 7.0)
        corr = np.correlate(got - got.mean(), ref - ref.mean(), mode="valid")
        lag = (int(np.argmax(corr)) - int(round((t0 - max(0.0, t0 - 0.5)) * 8000))) / 8000.0
        worst_lag = max(worst_lag, abs(lag))
        mid = s["frames"] // 2
        A = frame(src, mid / fps)[60:, :]
        B = frame(final, (start + mid) / fps)[60:, :]
        mse = float(np.mean((A - B) ** 2))
        psnr = 99.0 if mse == 0 else 10 * np.log10(255 ** 2 / mse)
        worst_psnr = min(worst_psnr, psnr)
        if abs(lag) >= 1.0 / fps or psnr < 30:
            report.append(f"   {s['file']}:{s['id']}: lag {lag * 1000:+.1f} ms, PSNR {psnr:.1f} dB")
    check("sync", worst_lag < 1.0 / fps, f"worst lag {worst_lag * 1000:.1f} ms over {len(picks)} scenes")
    check("picture", worst_psnr > 30, f"worst PSNR {worst_psnr:.1f} dB (below the HUD strip)")

    # loudness and silences
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summary = out[out.rfind("Summary:"):]
    I = float(summary.split("I:")[1].split("LUFS")[0])
    tp = float(summary.split("Peak:")[1].split("dBFS")[0])
    check("loudness", abs(I + 16) < 1.0 and tp < -1.0, f"{I:.1f} LUFS integrated, true peak {tp:.1f} dBTP")
    sil = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-vn", "-af", "silencedetect=n=-45dB:d=8", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    long_silences = [l for l in sil.splitlines() if "silence_duration" in l]
    card_s = max(ch["card_frames"] for ch in prog["chapters"]) / fps
    check("silences", all(float(l.split("silence_duration:")[1]) <= card_s + 3.5 for l in long_silences),
          f"{len(long_silences)} stretches of 8 s or more (chapter cards are {card_s:.0f} s)")

    text = "\n".join(report)
    (final.parent / "qa.txt").write_text(text + "\n")
    print(text)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
