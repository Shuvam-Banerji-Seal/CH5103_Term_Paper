"""Word timings for synthesised narration: CTC forced alignment of each line's known text.

usage (from the repo root):
  uv run --project video/tts python -E -s video/tts/align.py [--all]   # every store/<key>.wav without its .json

Emissions come from torchaudio's MMS_FA model (wav2vec2, 16 kHz, 20 ms frames, labels blank + a-z + apostrophe);
ctc.py finds the best path of the letters of the line as spoken (after the pronunciation lexicon). The words
handed to ManimGX keep the text's own spelling
("Hückel", "Hund's"): manimgx.audio.timed matches the letters of these pieces against the narration text, so a
piece is a whitespace-separated token of the text, timed from its first letter's first frame to its last letter's
last frame. Tokens without letters (a dash) are left out; timed() places punctuation itself.
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
import torch  # noqa: E402

from ctc import ctc_viterbi  # noqa: E402
from lexicon import pairs  # noqa: E402

STORE = ROOT / "video" / "build" / "tts" / "store"


def fold(token: str) -> str:
    """The token's letters as the aligner spells them: lower case a-z and apostrophes, accents removed."""
    out = []
    for c in unicodedata.normalize("NFKD", token.lower()):
        if "a" <= c <= "z" or (c == "'" and out):
            out.append(c)
    return "".join(out).strip("'")


def pieces_of(text: str) -> list[tuple[str, str]]:
    """(written token, folded letters of its spoken form) for each whitespace token of the text that has letters.
    The spoken form comes from the pronunciation lexicon ("wavefunction" is spoken "wave function")."""
    out = []
    for tok, said in pairs(text):
        if any(c.isalpha() for c in fold(tok)):
            f = fold(said.replace(" ", ""))
            if not f:
                raise ValueError(f"spoken form of {tok!r} has no letters: {said!r}")
            out.append((tok, f))
    return out


class Aligner:
    def __init__(self, threads: int = 8) -> None:
        import torchaudio

        torch.set_num_threads(threads)
        self.bundle = torchaudio.pipelines.MMS_FA
        self.model = self.bundle.get_model(with_star=False).eval()
        self.labels = {c: i for i, c in enumerate(self.bundle.get_labels(star=None))}
        self.rate = self.bundle.sample_rate

    def emissions(self, audio: np.ndarray, rate: int) -> tuple[np.ndarray, float]:
        import torchaudio.functional as AF

        wave = torch.from_numpy(audio.astype(np.float32))[None]
        if rate != self.rate:
            wave = AF.resample(wave, rate, self.rate)
        with torch.inference_mode():
            em, _ = self.model(wave)
        logp = torch.log_softmax(em[0], dim=-1).numpy()
        seconds_per_frame = wave.shape[1] / self.rate / logp.shape[0]
        return logp, seconds_per_frame

    def align(self, audio: np.ndarray, rate: int, text: str) -> list[tuple[str, float, float]]:
        pieces = pieces_of(text)
        tokens = [self.labels[c] for _, f in pieces for c in f]
        logp, dt = self.emissions(audio, rate)
        spans = ctc_viterbi(logp, tokens, blank=self.labels["-"])
        out, k = [], 0
        for tok, f in pieces:
            a, b = spans[k][0], spans[k + len(f) - 1][1]
            out.append((tok, round(a * dt, 3), round((b + 1) * dt, 3)))
            k += len(f)
        return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true", help="realign lines that already have timings")
    p.add_argument("--threads", type=int, default=8)
    args = p.parse_args()
    todo = []
    for wav in sorted(STORE.glob("*.wav")):
        meta = wav.with_suffix(".json")
        record = json.loads(meta.read_text(encoding="utf-8")) if meta.exists() else None
        if record is None:
            continue  # synth.py writes the record (text, speaker) together with the audio
        if args.all or not record.get("words"):
            todo.append((wav, meta, record))
    if not todo:
        print("nothing to align")
        return
    al = Aligner(args.threads)
    for i, (wav, meta, record) in enumerate(todo, 1):
        audio, rate = sf.read(wav, dtype="float32")
        record["words"] = al.align(audio, rate, record["text"])
        meta.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"[{i}/{len(todo)}] {wav.stem}: {len(record['words'])} words, {len(audio) / rate:.2f} s", flush=True)


if __name__ == "__main__":
    main()
