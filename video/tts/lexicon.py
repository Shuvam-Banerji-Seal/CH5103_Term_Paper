"""Pronunciation lexicon: respell words that Breeze-TTS-2 mispronounces, keeping the narration text as written.

The captions and ManimGX see the narration as written; the model hears the respelled text. `pairs` keeps the
correspondence token by token (a written token may become several spoken words), so the aligner can time each
written token by the letters of its spoken form.

Entries were chosen from a Whisper round trip of probe sentences (video/tts/probes/pronunciation.txt): a word is
here because it came back wrong ("wavefunction" -> "one-fumption", "antisymmetric" -> "anti-septic", "aufbau" ->
"Au-Bao", "zwitterionic" -> "visiterion", ...). Changing an entry changes the spoken text of every line that uses
it; synth.py re-synthesises a line whenever its stored spoken text differs.
"""
from __future__ import annotations

import re

LEXICON = {
    "wavefunction": "wave function",
    "wavefunctions": "wave functions",
    "antisymmetric": "anti symmetric",
    "antisymmetry": "anti symmetry",
    "antisymmetrised": "anti symmetrised",
    "antisymmetrise": "anti symmetrise",
    "zwitterionic": "zwitter ionic",
    "aufbau": "owf bow",
    "non-aufbau": "non owf bow",
    "xylylene": "zylileen",
    "cyclobutadiene": "cyclo buta diene",
    "tetramethyleneethane": "tetramethylene ethane",
    "trimethylenebenzene": "trimethylene benzene",
    "tetramethylenebenzene": "tetramethylene benzene",
    "laplacian": "la play see an",
    "psi": "sigh",
    "chi": "kai",
    "mathlib": "math lib",
    "sympy": "sim pie",
    "mott": "mot",
}

_TOKEN = re.compile(r"^(?P<lead>[^\w]*)(?P<core>.*?)(?P<poss>'s)?(?P<trail>[^\w]*)$", re.UNICODE)


def _respell_token(token: str) -> str:
    m = _TOKEN.match(token)
    core = m.group("core")
    spoken = LEXICON.get(core.lower())
    if spoken is None:
        return token
    if core[:1].isupper():
        spoken = spoken[:1].upper() + spoken[1:]
    return m.group("lead") + spoken + (m.group("poss") or "") + m.group("trail")


def pairs(text: str) -> list[tuple[str, str]]:
    """(written token, spoken form) for every whitespace token of the text."""
    return [(tok, _respell_token(tok)) for tok in text.split()]


def spoken(text: str) -> str:
    """The text the model is given."""
    return " ".join(s for _, s in pairs(text))
