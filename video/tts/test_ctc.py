"""Tests for the CTC forced aligner (run: uv run --project video/tts python -I -m pytest -q video/tts/test_ctc.py)."""
import numpy as np
import pytest

from ctc import ctc_viterbi, normalise_words, word_spans

LABELS = ["-", "a", "b", "c", "'"]  # blank first, like MMS_FA


def onehot_emissions(frames: list[int], n_labels: int = len(LABELS), peak: float = 0.97) -> np.ndarray:
    """Log-probabilities with label frames[t] dominant at frame t."""
    rest = (1 - peak) / (n_labels - 1)
    e = np.full((len(frames), n_labels), np.log(rest))
    for t, k in enumerate(frames):
        e[t, k] = np.log(peak)
    return e


def test_simple_path_recovered():
    # blank blank a a blank b blank c c c blank
    frames = [0, 0, 1, 1, 0, 2, 0, 3, 3, 3, 0]
    path = ctc_viterbi(onehot_emissions(frames), [1, 2, 3])
    # path[i] = (first frame, last frame) of token i
    assert path == [(2, 3), (5, 5), (7, 9)]


def test_repeated_label_needs_blank_between():
    # tokens a a must be separated by a blank in CTC
    frames = [1, 1, 0, 1, 0]
    path = ctc_viterbi(onehot_emissions(frames), [1, 1])
    assert path[0][1] < path[1][0]
    assert path == [(0, 1), (3, 3)]


def test_repeat_forces_blank_even_when_unlikely():
    # every frame prefers "a": a legal path for "a a" must still spend >= 1 frame on a blank between them
    frames = [1, 1, 1, 1, 1]
    path = ctc_viterbi(onehot_emissions(frames), [1, 1])
    assert path[1][0] - path[0][1] >= 2, path  # at least one blank frame in between


def test_too_short_raises():
    with pytest.raises(ValueError):
        ctc_viterbi(onehot_emissions([1]), [1, 2, 3])


def test_normalise_words_and_spans():
    words = normalise_words("Hund's rule, step-by-step: K sub a b.")
    assert words == ["hund's", "rule", "stepbystep", "k", "sub", "a", "b"]
    # token spans per word: frames of first..last character
    token_frames = [(i, i) for i in range(sum(len(w) for w in words))]
    spans = word_spans(words, token_frames)
    assert spans[0] == (0, 5) and spans[1] == (6, 9) and len(spans) == len(words)


def test_word_without_letters_is_dropped():
    assert normalise_words("a — b") == ["a", "b"]
