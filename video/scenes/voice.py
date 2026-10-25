"""The narrator: Breeze-TTS-2 lines, synthesised and aligned offline (video/tts), served to ManimGX as a Voice.

ManimGX calls a scene's voice with the text of each `say`/`speech` line and caches what it returns in `voice/`
beside the scene file. The audio itself comes from video/build/tts/store/: video/tts/synth.py writes
<key>.wav (Breeze-TTS-2, 24 kHz mono) and video/tts/align.py writes <key>.json with the time of every word
(CTC forced alignment), where key = line_key(text, speaker).

Modes (VIDEO_VOICE): "final" (a missing line is an error), "draft" (a missing line is silence of about the
right length, for layout work), "collect" (like draft, and every line is appended to requests.jsonl for the
batch synthesiser). The mode is a field of the voice, so each mode has its own entries in ManimGX's cache.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

import manimgx as m
from manimgx.audio import timed

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / "video" / "build" / "tts" / "store"
REQUESTS = ROOT / "video" / "build" / "tts" / "requests.jsonl"
RATE = 24000
WORDS_PER_SECOND = 2.6  # draft placeholder pacing; replaced by the measured rate once lines exist


def line_key(text: str, speaker: str) -> str:
    return hashlib.sha256(f"{speaker}\n{text}".encode()).hexdigest()[:20]


def ascii_letters(word: str) -> str:
    """The word's letters folded to a-z (ü -> u, é -> e), as the CTC aligner spells them."""
    return "".join(c for c in unicodedata.normalize("NFKD", word.lower()) if "a" <= c <= "z")


def lint(text: str) -> list[str]:
    """Problems that would break synthesis or alignment of a narration line."""
    out = []
    if re.search(r"\d", text):
        out.append("digits (spell numbers out: the aligner and the captions need words)")
    if re.search(r"[()]", text):
        out.append("parentheses (Breeze reads '(laugh)' and the like as vocal events)")
    if re.search(r"[\\$^_{}]", text):
        out.append("LaTeX characters (write symbols as spoken words)")
    if "[" in text or "]" in text:
        out.append("brackets left in the spoken text")
    foreign = sorted({c for c in text if c.isalnum() and not ascii_letters(c)})
    if foreign:
        out.append(f"letters the aligner cannot spell: {''.join(foreign)} (write Greek letters as words)")
    return out


@dataclass(frozen=True)
class Breeze:
    """Breeze-TTS-2 as a ManimGX voice. Its repr names it in ManimGX's cache: change `speaker` when the voice or
    its settings change, and every line is fetched again."""

    mode: str = "draft"
    speaker: str = "narrator-v1"
    digest: str = ""  # final renders: a digest of the store, so ManimGX's cache refetches lines when the store changes
    store: str = field(default=str(STORE), repr=False, compare=False)

    def __call__(self, text: str) -> m.Speech:
        problems = lint(text)
        if problems:
            raise ValueError(f"narration line {text!r}: " + "; ".join(problems))
        key = line_key(text, self.speaker)
        wav, meta = Path(self.store) / f"{key}.wav", Path(self.store) / f"{key}.json"
        if self.mode == "collect":
            _request(text, self.speaker, key)
        if wav.exists() and meta.exists():
            record = json.loads(meta.read_text(encoding="utf-8"))
            if record["text"] != text:
                raise RuntimeError(f"store entry {key} is for a different text")
            pieces = [(w, s, e) for w, s, e in record.get("words") or []]
            if pieces:
                words = timed(text, pieces)
                if not words:
                    raise RuntimeError(f"aligned words do not spell the line: {text!r}")
                return m.Speech(str(wav), text=text, words=words)
            if self.mode == "final":
                raise FileNotFoundError(f"line synthesised but not aligned yet ({key}) — run video/tts/align.py")
            return m.Speech(str(wav), text=text)  # until aligned, ManimGX estimates the word times from the audio
        if self.mode == "final":
            raise FileNotFoundError(f"line not synthesised yet ({key}): {text!r} — run video/tts/synth.py")
        n_words = max(1, len(text.split()))
        seconds = n_words / WORDS_PER_SECOND + 0.35
        return m.Speech(np.zeros(int(seconds * RATE), dtype=np.float32), text=text, rate=RATE)


def store_digest() -> str:
    """Names, sizes and modification times of every store file: changes whenever a line is synthesised again or
    re-aligned."""
    h = hashlib.sha256()
    for p in sorted(STORE.glob("*")) if STORE.exists() else []:
        st = p.stat()
        h.update(f"{p.name}:{st.st_size}:{st.st_mtime_ns}\n".encode())
    return h.hexdigest()[:16]


def _request(text: str, speaker: str, key: str) -> None:
    REQUESTS.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    if REQUESTS.exists():
        seen = {json.loads(line)["key"] for line in REQUESTS.read_text(encoding="utf-8").splitlines() if line}
    if key not in seen:
        with REQUESTS.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"key": key, "speaker": speaker, "text": text}, ensure_ascii=False) + "\n")
