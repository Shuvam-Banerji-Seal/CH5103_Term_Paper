"""Background music for the explainer: an original ambient score generated here (additive synthesis; no samples, no
recordings, nothing to license or to be claimed), laid out on the programme and mixed under the narration.

compose  one chord every 8 s, all in D major / B minor so no two chapters can clash where they overlap; each chapter
         starts a fresh phrase on its title card and has its own pair of progressions and its own sparse felt-piano
         line. Warm pads (four soft partials, slow swell, each voice panned), a centred sine bass, a synthetic hall
         reverb (the only decorrelated part, so a mono downmix loses nothing).
         Rendered in 30 s chunks (in parallel, then reverberated in order) to a 48 kHz FLAC exactly as long as the
         programme.
mix      the score at a fixed loudness, ducked by the narration (a sidechain compressor keyed on the voice: about
         11 dB down while someone speaks, back up in pauses and on the chapter cards), added to the voice,
         normalised to -16 LUFS, and muxed with the video stream copied (the picture is not re-encoded).
check    how far the ducked music sits under the voice, and whether Whisper hears the narration as well with the
         music as without it (the same pause-to-pause excerpts transcribed from both soundtracks, against a control
         with inaudible noise for Whisper's own sensitivity).

usage (from the repo root):
  uv run --project video/tts python -E -s video/tools/bgm.py compose [--program video/build/program.json]
  uv run --project video/tts python -E -s video/tools/bgm.py mix --video video/build/final/ch5103-explainer.mp4 \
      --out video/build/final-music/ch5103-explainer.mp4 [--music-lufs -26] [--ratio 4]
  uv run --project video/tts python -E -s video/tools/bgm.py remux --video video/build/final/ch5103-explainer-4k.mp4 \
      --out video/build/final-music/ch5103-explainer-4k.mp4
  uv run --project video/tts python -E -s video/tools/bgm.py check [--n 12]
"""
from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, oaconvolve, sosfilt

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "video" / "build"
MUSIC = BUILD / "music"
SCORE = MUSIC / "score.flac"
SR = 48000
CHORD_S = 8.0
CHUNK_S = 30.0

# D major / B minor; a chord is (root in semitones above D, intervals above the root). All diatonic.
CHORDS = {
    "I": (0, (0, 4, 7, 11, 14)),    # Dmaj9
    "ii": (2, (0, 3, 7, 10, 14)),   # Em9
    "iii": (4, (0, 3, 7, 10)),      # F#m7
    "IV": (5, (0, 4, 7, 11, 14)),   # Gmaj9
    "V": (7, (0, 5, 7, 14)),        # Asus4(add9)
    "vi": (9, (0, 3, 7, 10, 14)),   # Bm9
}
PROGRESSIONS = [("I", "vi", "IV", "V"), ("vi", "IV", "I", "V"), ("IV", "V", "iii", "vi"), ("ii", "V", "I", "vi"),
                ("I", "IV", "vi", "V"), ("vi", "iii", "IV", "I")]
PENTATONIC = {0, 2, 4, 7, 9}        # D E F# A B: the melody's notes
D2 = 38                             # MIDI


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def envelope(t: np.ndarray, attack: float, hold: float, release: float) -> np.ndarray:
    """Raised-cosine swell in over `attack` times raised-cosine fade from `hold` over `release` (a product, so a note cut
    short before its swell ends fades from where it got to)."""
    up = 0.5 - 0.5 * np.cos(np.pi * np.clip(t / attack, 0.0, 1.0))
    down = 0.5 + 0.5 * np.cos(np.pi * np.clip((t - hold) / release, 0.0, 1.0))
    return up * down


def harmonics(theta: np.ndarray, amps: tuple[float, ...]) -> np.ndarray:
    """sum_k a_k sin(k theta), by the Chebyshev recurrence (one sine and one cosine for all partials)."""
    c2 = 2 * np.cos(theta)
    s_prev, s = np.zeros_like(theta), np.sin(theta)
    out = amps[0] * s
    for a in amps[1:]:
        s_prev, s = s, c2 * s - s_prev
        out += a * s
    return out


def panned(mono: np.ndarray, pan: float) -> np.ndarray:
    """Constant-power pan, -1 (left) to 1 (right): the two channels are the same signal, so a mono downmix loses
    nothing (independent phases per channel made the left and right uncorrelated and could cancel the bass)."""
    a = (pan + 1) * np.pi / 4
    return mono[:, None] * np.array([np.cos(a), np.sin(a)])[None, :]


class Pad:
    """A sustained voice: four soft partials, a slow swell and a slow tremolo, panned to its own place."""
    ATTACK, RELEASE, AMPS = 3.0, 4.5, (1.0, 0.32, 0.12, 0.05)

    def __init__(self, t0: float, hold: float, midi: float, amp: float, rng: np.random.Generator,
                 amps: tuple[float, ...] | None = None, pan: float = 0.0, attack: float | None = None) -> None:
        self.t0, self.hold, self.f, self.amp, self.pan = t0, hold, hz(midi), amp, pan
        self.amps = amps or self.AMPS
        self.attack = attack or self.ATTACK
        self.t1 = t0 + hold + self.RELEASE
        self.phase = rng.uniform(0, 2 * np.pi)
        self.lfo = (rng.uniform(0.04, 0.09), rng.uniform(0, 2 * np.pi))

    def render(self, t: np.ndarray) -> np.ndarray:
        g = self.amp * envelope(t, self.attack, self.hold, self.RELEASE) * (1 + 0.1 * np.sin(2 * np.pi * self.lfo[0] * t + self.lfo[1]))
        return panned(g * harmonics(2 * np.pi * self.f * t + self.phase, self.amps), self.pan)


class Bell:
    """A felt-piano note: a soft 6 ms onset, partials that die away faster the higher they are, panned."""
    AMPS, T60 = (1.0, 0.42, 0.16, 0.07), 3.6

    def __init__(self, t0: float, midi: float, amp: float, pan: float, rng: np.random.Generator) -> None:
        self.t0, self.f, self.amp = t0, hz(midi), amp
        self.t1 = t0 + self.T60 + 0.3
        self.pan = pan
        self.phase = rng.uniform(0, 2 * np.pi)

    def render(self, t: np.ndarray) -> np.ndarray:
        theta = 2 * np.pi * self.f * t + self.phase
        mono = np.zeros_like(t)
        for k, a in enumerate(self.AMPS, 1):
            mono += a * np.exp(-6.91 * t / (self.T60 / k ** 0.7)) * np.sin(k * theta)
        mono *= self.amp * (1 - np.exp(-t / 0.006))
        return panned(mono, self.pan)


def voicing(chord: str, prev: list[int]) -> list[int]:
    """Four notes of the chord, distinct pitch classes, between E3 and E5, moving as little as possible from `prev`."""
    root, iv = CHORDS[chord]
    pcs = {(root + i) % 12 for i in iv}
    cands = [m for m in range(52, 77) if (m - D2) % 12 in pcs]
    best, cost = None, 1e9
    for combo in itertools.combinations(cands, 4):
        if len({(m - D2) % 12 for m in combo}) < 4:
            continue
        c = sum(abs(a - b) for a, b in zip(combo, prev))
        if c < cost:
            best, cost = list(combo), c
    return best  # type: ignore[return-value]


def chapter_spans(program: dict) -> list[tuple[float, float]]:
    fps, t, spans = program["fps"], 0.0, []
    for ch in program["chapters"]:
        n = ch["card_frames"] + sum(s["frames"] for s in ch["scenes"])
        spans.append((t, t + n / fps))
        t += n / fps
    return spans


def events(program: dict) -> list:
    out: list = []
    prev = [57, 62, 66, 69]
    for i, (a, b) in enumerate(chapter_spans(program)):
        rng = np.random.default_rng(5103 + i)
        pa, pb = rng.choice(len(PROGRESSIONS), 2, replace=False)
        phrase = itertools.cycle([PROGRESSIONS[pa]] * 2 + [PROGRESSIONS[pb]] + [PROGRESSIONS[pa]])
        t = a
        while t < b - 0.5:
            for chord in next(phrase):
                if t >= b - 0.5:
                    break
                hold = min(CHORD_S, b - t)   # a chapter's last chord ends at the next card, which starts a new phrase
                notes = voicing(chord, prev)
                prev = notes
                for m, pan in zip(notes, (-0.45, 0.3, -0.2, 0.45)):   # voices spread across the stereo field
                    out.append(Pad(t, hold, m, 0.05, rng, pan=pan))
                root = CHORDS[chord][0]
                out.append(Pad(t, hold, D2 + root, 0.065, rng, amps=(1.0, 0.18), attack=2.0))   # bass, centre
                pool = [m for m in range(69, 84) if (m - D2) % 12 in PENTATONIC
                        and (m - D2) % 12 in {(root + j) % 12 for j in CHORDS[chord][1]}]
                grid = np.arange(0.5, hold - 0.9, 0.5)
                n = min(len(grid), rng.choice([0, 1, 1, 2, 2, 3]))
                times = sorted(rng.choice(grid, size=n, replace=False)) if n else []
                last = -9.0
                for dt in times:
                    if dt - last < 1.0:
                        continue
                    out.append(Bell(t + dt, rng.choice(pool), 0.03 * rng.uniform(0.7, 1.0), rng.uniform(-0.35, 0.35), rng))
                    last = dt
                t += CHORD_S
    return out


def hall(rt60: float = 3.4, length: float = 5.0, predelay: float = 0.025) -> np.ndarray:
    """A synthetic hall: decorrelated left/right noise decaying with the given RT60, darkened, unit energy."""
    rng = np.random.default_rng(7)
    n = int(length * SR)
    ir = rng.standard_normal((n, 2)) * np.exp(-6.91 * np.arange(n) / SR / rt60)[:, None]
    ir = sosfilt(butter(2, 4500, fs=SR, output="sos"), ir, axis=0)
    ir = np.vstack([np.zeros((int(predelay * SR), 2)), ir])
    return ir / np.sqrt((ir ** 2).sum(axis=0))


_EVENTS: list = []


def _init(evts: list) -> None:
    global _EVENTS
    _EVENTS = evts


def dry_chunk(args: tuple[int, int]) -> np.ndarray:
    i0, i1 = args
    buf = np.zeros((i1 - i0, 2))
    t0, t1 = i0 / SR, i1 / SR
    for e in _EVENTS:
        if e.t1 <= t0 or e.t0 >= t1:
            continue
        j0, j1 = max(i0, int(np.ceil(e.t0 * SR))), min(i1, int(e.t1 * SR))
        if j1 > j0:
            buf[j0 - i0:j1 - i0] += e.render(np.arange(j0, j1) / SR - e.t0)
    return buf


def compose(program_path: Path, out: Path, jobs: int) -> None:
    program = json.loads(program_path.read_text())
    total = program["total_frames"] * (SR // program["fps"])   # samples, exactly the narration's length
    evts = events(program)
    ir = hall()
    chunk = int(CHUNK_S * SR)
    ranges = [(i, min(total, i + chunk)) for i in range(0, total, chunk)]
    out.parent.mkdir(parents=True, exist_ok=True)
    carry = np.zeros((0, 2))
    fade_in, fade_out = int(3 * SR), int(6 * SR)
    peak = 0.0
    with sf.SoundFile(out, "w", SR, 2, subtype="PCM_24", format="FLAC") as f, Pool(jobs, _init, (evts,)) as pool:
        for k, dry in enumerate(pool.imap(dry_chunk, ranges)):
            i0, i1 = ranges[k]
            wet = np.stack([oaconvolve(dry[:, c], ir[:, c]) for c in range(2)], axis=1)
            wet[:len(carry)] += carry
            y = 0.8 * dry + 0.5 * wet[:len(dry)]
            carry = wet[len(dry):]
            n = np.arange(i0, i1)
            y *= np.clip(n / fade_in, 0, 1)[:, None] * np.clip((total - n) / fade_out, 0, 1)[:, None]
            peak = max(peak, float(np.abs(y).max()))
            f.write(np.clip(y, -1, 1).astype(np.float32))
            if k % 40 == 0:
                print(f"chunk {k + 1}/{len(ranges)}", flush=True)
    print(f"{len(evts)} notes, {total / SR:.3f} s, peak {peak:.3f} -> {out.relative_to(ROOT)}")


def loudness(path: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vn", "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(err[err.rfind("Summary:"):].split("I:")[1].split("LUFS")[0])


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def remux(video: Path, out: Path) -> None:
    """The video stream copied, with the mixed soundtrack (the 4K file reuses the 1080p mix: same frames, same audio)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    ff("-i", str(video), "-i", str(MUSIC / "mix.flac"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
       "-b:a", "192k", "-metadata", "title=CH5103: correlation and spin states, explained and checked",
       "-movflags", "+faststart", str(out))


def mix(video: Path, out: Path, voice: Path, music_lufs: float, ratio: float) -> None:
    work = MUSIC
    gain = music_lufs - loudness(SCORE)
    duck = (f"[1:a]volume={gain:.2f}dB[mus];"
            f"[mus][0:a]sidechaincompress=threshold=0.02:ratio={ratio}:attack=80:release=1000:knee=6:detection=rms[duck]")
    # the ducked music alone (for the check), then voice + ducked music
    ff("-i", str(voice), "-i", str(SCORE), "-filter_complex", duck, "-map", "[duck]", "-c:a", "flac", str(work / "ducked.flac"))
    ff("-i", str(voice), "-i", str(work / "ducked.flac"), "-filter_complex",
       "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[m]", "-map", "[m]", "-c:a", "flac",
       str(work / "mix_raw.flac"))
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(work / "mix_raw.flac"), "-af",
                           "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    L = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    ff("-i", str(work / "mix_raw.flac"), "-af",
       f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}"
       f":measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true,aresample={SR}",
       "-c:a", "flac", str(work / "mix.flac"))
    remux(video, out)
    print(f"score {gain:+.1f} dB to {music_lufs} LUFS, ducked by the voice (ratio {ratio}); mix {L['input_i']} LUFS -> -16;"
          f" {out.relative_to(ROOT)}")


def read_mono(path: Path, rate: int, start: float = 0.0, dur: float | None = None) -> np.ndarray:
    cut = ["-ss", f"{start:.3f}", "-t", f"{dur:.3f}"] if dur else []
    raw = subprocess.run(["ffmpeg", "-v", "error", *cut, "-i", str(path), "-vn", "-ac", "1", "-ar", str(rate), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def pause_stretches(voice: np.ndarray, rate: int) -> list[tuple[float, float]]:
    """Stretches of narration 8 to 25 s long that start and end in a pause of at least 0.4 s (0.1 s windows under
    -45 dBFS): excerpts that do not cut through a word, so Whisper is compared on whole sentences."""
    w = rate // 10
    k = len(voice) // w
    quiet = 20 * np.log10(np.sqrt((voice[:k * w].reshape(k, w) ** 2).mean(1)) + 1e-9) <= -45
    runs, start = [], None
    for j in range(k):
        if quiet[j:j + 4].all():
            if start is not None and 80 <= j - start <= 250:
                runs.append((start / 10 - 0.2, j / 10 + 0.2))
            start = j + 4 if start is None or j - start > 3 else start
    return runs


def check(n: int) -> int:
    """How far the ducked music sits under the voice, and whether Whisper hears the narration the same with it: the
    same pause-to-pause excerpts transcribed from the voice alone, from the mix, and (a control for Whisper's own
    sensitivity to any change in its input) from the voice with white noise at -60 dBFS."""
    voice, music = read_mono(BUILD / "assemble" / "narration.wav", 8000), read_mono(MUSIC / "ducked.flac", 8000)
    w = 8000 // 2   # 0.5 s windows
    k = min(len(voice), len(music)) // w
    rv = np.sqrt((voice[:k * w].reshape(k, w) ** 2).mean(1)) + 1e-9
    rm = np.sqrt((music[:k * w].reshape(k, w) ** 2).mean(1)) + 1e-9
    speech = 20 * np.log10(rv) > -35
    margin = 20 * np.log10(rv[speech] / rm[speech])
    print(f"voice over music where someone speaks: median {np.median(margin):.1f} dB, 5th percentile "
          f"{np.percentile(margin, 5):.1f} dB ({speech.mean() * 100:.0f}% of the programme)")
    print(f"music level in pauses: median {np.median(20 * np.log10(rm[~speech])):.1f} dBFS RMS")
    runs = pause_stretches(voice, 8000)
    del voice, music
    sys.path.insert(0, str(ROOT / "video" / "tts"))
    from asr import Whisper, wer, words  # noqa: E402
    whisper = Whisper(8)
    rng = np.random.default_rng(3)
    dm, dn = [], []
    for i in sorted(rng.choice(len(runs), n, replace=False)):
        a, b = runs[i]
        v = read_mono(BUILD / "assemble" / "narration.wav", 16000, a, b - a)
        ref = words(whisper.transcribe(v, 16000))
        dm.append(wer(ref, words(whisper.transcribe(read_mono(MUSIC / "mix.flac", 16000, a, b - a), 16000))))
        noise = np.random.default_rng(int(i)).standard_normal(len(v)).astype(np.float32) * 0.001
        dn.append(wer(ref, words(whisper.transcribe(v + noise, 16000))))
        print(f"{a:8.1f}-{b:7.1f} s  word difference with the music {dm[-1]:.3f}, with -60 dB noise {dn[-1]:.3f}")
    print(f"{len(runs)} pause-to-pause stretches, {n} checked: mean word difference with the music {np.mean(dm):.3f},"
          f" with inaudible noise {np.mean(dn):.3f}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["compose", "mix", "remux", "check"])
    p.add_argument("--program", type=Path, default=BUILD / "program.json")
    p.add_argument("--video", type=Path, default=BUILD / "final" / "ch5103-explainer.mp4")
    p.add_argument("--voice", type=Path, default=BUILD / "assemble" / "narration.wav")
    p.add_argument("--out", type=Path, default=BUILD / "final-music" / "ch5103-explainer.mp4")
    p.add_argument("--music-lufs", type=float, default=-26.0)
    p.add_argument("--ratio", type=float, default=4.0)
    p.add_argument("--jobs", type=int, default=6)
    p.add_argument("--n", type=int, default=12)
    a = p.parse_args()
    if a.cmd == "compose":
        compose(a.program, SCORE, a.jobs)
    elif a.cmd == "mix":
        mix(a.video, a.out, a.voice, a.music_lufs, a.ratio)
    elif a.cmd == "remux":
        remux(a.video, a.out)
    else:
        return check(a.n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
