"""CTC forced alignment (Viterbi) of a known text against frame-wise log-probabilities.

Approach after pdoom-video-sbs/analysis/ctcalign.py (MIT): emissions from torchaudio's MMS_FA model, labels
blank + a–z + apostrophe, one best path through the text's characters. Here the speech is clean TTS narration,
so a single unconstrained pass per line is enough (no garbage token, no anchors).
"""
from __future__ import annotations

import re

import numpy as np

_WORD = re.compile(r"[a-z']+")


def normalise_words(text: str) -> list[str]:
    """The text's words as the aligner sees them: lower case, letters and apostrophes only. Characters inside a
    word that are not letters (hyphens) are removed, so "step-by-step" is one word; tokens without letters are
    dropped."""
    out = []
    for raw in text.lower().split():
        w = "".join(_WORD.findall(raw))
        w = w.strip("'")
        if any(c.isalpha() for c in w):
            out.append(w)
    return out


def ctc_viterbi(logp: np.ndarray, tokens: list[int], blank: int = 0) -> list[tuple[int, int]]:
    """Best CTC path of `tokens` through `logp` (T × V log-probabilities).

    Returns, for each token, (first frame, last frame) it occupies. The extended sequence is
    blank, t1, blank, t2, ..., tL, blank; a step may stay, advance by one, or skip a blank between two different
    tokens.
    """
    T, L = logp.shape[0], len(tokens)
    if L == 0:
        return []
    ext = [blank]
    for t in tokens:
        ext += [t, blank]
    S = len(ext)
    # a path needs at least L frames, plus one per adjacent repeated pair (they need a blank between them)
    need = L + sum(1 for a, b in zip(tokens, tokens[1:]) if a == b)
    if T < need:
        raise ValueError(f"{T} frames cannot hold {L} tokens ({need} needed)")
    ext = np.array(ext)
    em = logp[:, ext]  # T × S
    NEG = -1e30
    score = np.full(S, NEG)
    score[0] = em[0, 0]
    score[1] = em[0, 1]
    back = np.zeros((T, S), dtype=np.int8)  # 0 stay, 1 from s-1, 2 from s-2
    can_skip = np.zeros(S, dtype=bool)
    for s in range(2, S):
        can_skip[s] = ext[s] != blank and ext[s] != ext[s - 2]
    for t in range(1, T):
        stay = score
        prev1 = np.concatenate([[NEG], score[:-1]])
        prev2 = np.where(can_skip, np.concatenate([[NEG, NEG], score[:-2]]), NEG)
        stacked = np.stack([stay, prev1, prev2])
        choice = np.argmax(stacked, axis=0)
        score = stacked[choice, np.arange(S)] + em[t]
        back[t] = choice
    # end in the last token or the final blank
    s = S - 1 if score[S - 1] >= score[S - 2] else S - 2
    states = np.empty(T, dtype=np.int64)
    for t in range(T - 1, -1, -1):
        states[t] = s
        s -= back[t, s]
    spans: list[tuple[int, int]] = []
    for i in range(L):
        frames = np.flatnonzero(states == 2 * i + 1)
        if len(frames) == 0:
            raise RuntimeError(f"token {i} not on the path")
        spans.append((int(frames[0]), int(frames[-1])))
    return spans


def word_spans(words: list[str], token_spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Group per-character spans into per-word (first frame, last frame)."""
    out, k = [], 0
    for w in words:
        n = len(w)
        out.append((token_spans[k][0], token_spans[k + n - 1][1]))
        k += n
    if k != len(token_spans):
        raise ValueError("token count does not match the words")
    return out
