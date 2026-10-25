"""Round-trip check of synthesised narration: transcribe each line with Whisper (small.en) and compare with the
text it should say, word by word.

usage (from the repo root):
  uv run --project video/tts python -E -s video/tts/asr.py [--all]        # store/<key>.wav lines not yet checked
  uv run --project video/tts python -E -s video/tts/asr.py --recheck      # + failed lines heard whole, now by sentence
  uv run --project video/tts python -E -s video/tts/asr.py --files a.wav b.wav --texts "..." "..."

A line passes when its word error rate is at most MAX_WER after normalisation (lower case, punctuation dropped,
spelled-out numbers and letter names folded so that "U plus k" and "you plus K" compare equal). Lines that fail
are listed for listening and re-synthesis with another seed; the result is stored in the line's record ("asr").
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
import torch  # noqa: E402

STORE = ROOT / "video" / "build" / "tts" / "store"
WHISPER = HERE / "checkpoints" / "whisper-small.en"
MAX_WER = 0.12

# Whisper hears single letters and symbols as words or digits; fold both sides to one spelling.
_FOLD = {
    "you": "u", "are": "r", "why": "y", "see": "c", "sea": "c", "tea": "t", "bee": "b", "be": "b", "jay": "j",
    "kay": "k", "okay": "ok", "ex": "x", "eks": "x", "pea": "p", "pee": "p", "queue": "q", "cue": "q", "aye": "i",
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
    "8": "eight", "9": "nine", "10": "ten", "+": "plus", "-": "minus", "=": "equals", "×": "times",
}


def _us(w: str) -> str:
    """British and American spellings compare equal (applied to both sides, so collisions only blunt the check)."""
    for gb, us in (("isation", "ization"), ("ised", "ized"), ("ising", "izing"), ("ises", "izes"), ("ise", "ize"),
                   ("ysed", "yzed"), ("yse", "yze"), ("ours", "ors"), ("our", "or"), ("tre", "ter")):
        if w.endswith(gb):
            return w[: -len(gb)] + us
    return w


def words(text: str) -> list[str]:
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", t)  # "c1" -> "c 1"
    t = re.sub(r"([+=×])", r" \1 ", t)
    t = re.sub(r"(?<=\s)-(?=\s)", " - ", t)
    out = []
    for w in re.findall(r"[a-z0-9']+|[+=×]", t.replace("-", " ")):
        w = w.strip("'")
        if w:
            out.append(_us(_FOLD.get(w, w)))
    return out


def wer(ref: list[str], hyp: list[str]) -> float:
    """Word error rate: Levenshtein distance between the word lists over the reference length."""
    d = np.arange(len(hyp) + 1)
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return float(d[len(hyp)]) / max(1, len(ref))


class Whisper:
    def __init__(self, threads: int = 8) -> None:
        from transformers import WhisperForConditionalGeneration, WhisperProcessor

        torch.set_num_threads(threads)
        self.proc = WhisperProcessor.from_pretrained(WHISPER)
        self.model = WhisperForConditionalGeneration.from_pretrained(WHISPER, torch_dtype=torch.float32).eval()

    def transcribe(self, audio: np.ndarray, rate: int) -> str:
        import torchaudio.functional as AF

        wave = torch.from_numpy(audio.astype(np.float32))
        if rate != 16000:
            wave = AF.resample(wave[None], rate, 16000)[0]
        feats = self.proc(wave.numpy(), sampling_rate=16000, return_tensors="pt").input_features
        with torch.inference_mode():
            ids = self.model.generate(feats, max_new_tokens=440)
        return self.proc.batch_decode(ids, skip_special_tokens=True)[0].strip()


def spans(timed: list, seconds: float, longest: float = 24.0) -> list[tuple[float, float]]:
    """Cut a line at its sentence ends (word timings from align.py) into pieces of at most `longest` seconds.
    Whisper sees 30 s at a time and often stops at the pause after a colon, so a long line heard in one go can come
    back truncated although every word was said."""
    cuts, start = [], 0.0
    for k, (tok, _, end) in enumerate(timed):
        last = k == len(timed) - 1
        nxt = timed[k + 1][1] if not last else seconds
        if last or (tok[-1] in ".:;?!" and end - start > 1.0) or (tok[-1] == "," and nxt - start > longest * 0.6):
            cut = seconds if last else (end + nxt) / 2
            while cut - start > longest:  # one sentence longer than Whisper's window: hard cuts
                cuts.append((start, start + longest))
                start += longest
            cuts.append((start, cut))
            start = cut
    return cuts or [(0.0, seconds)]


def check(w: Whisper, wav: Path, text: str, timed: list | None = None) -> dict:
    audio, rate = sf.read(wav, dtype="float32")
    if timed:
        parts = [w.transcribe(audio[int(a * rate): int(b * rate)], rate) for a, b in spans(timed, len(audio) / rate)]
        heard = " ".join(p for p in parts if p)
    else:
        heard = w.transcribe(audio, rate)
    return {"heard": heard, "wer": round(wer(words(text), words(heard)), 3), "seconds": round(len(audio) / rate, 2),
            "words_per_second": round(len(text.split()) / (len(audio) / rate), 2), "chunked": bool(timed)}


def truncated(a: dict, text: str) -> bool:
    return a["wer"] > 0.5 or len(words(a["heard"])) < 0.8 * len(words(text)) or a["seconds"] > 29


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true")
    p.add_argument("--recheck", action="store_true")
    p.add_argument("--files", nargs="*")
    p.add_argument("--texts", nargs="*")
    p.add_argument("--threads", type=int, default=8)
    args = p.parse_args()
    w = Whisper(args.threads)
    if args.files:
        for f, t in zip(args.files, args.texts):
            r = check(w, Path(f), t)
            flag = "ok " if r["wer"] <= MAX_WER else "BAD"
            print(f"{flag} wer {r['wer']:.2f} {r['seconds']:5.1f} s {r['words_per_second']:.2f} w/s  {Path(f).name}\n"
                  f"     said: {t}\n    heard: {r['heard']}", flush=True)
        return
    bad = []
    for meta in sorted(STORE.glob("*.json")):
        record = json.loads(meta.read_text(encoding="utf-8"))
        a = record.get("asr")
        # --recheck: lines heard in one go whose transcript looks cut short, heard again sentence by sentence (a full
        # length transcript over MAX_WER is mostly spelling: "0.077" for "zero point zero seven seven")
        if a and not args.all and not (args.recheck and a["wer"] > MAX_WER and not a.get("chunked") and truncated(a, record["text"])):
            continue
        record["asr"] = check(w, meta.with_suffix(".wav"), record["text"], record.get("words"))
        meta.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        if record["asr"]["wer"] > MAX_WER:
            bad.append(meta.stem)
            print(f"BAD {meta.stem} wer {record['asr']['wer']:.2f}\n     said: {record['text']}\n"
                  f"    heard: {record['asr']['heard']}", flush=True)
    print(f"{len(bad)} lines over WER {MAX_WER}")


if __name__ == "__main__":
    main()
