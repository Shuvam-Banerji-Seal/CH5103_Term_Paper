"""Normalisation and word error rate of the ASR round trip (no model needed)."""
from asr import wer, words


def test_letters_and_symbols_fold():
    assert words("U plus k") == words("you plus K") == ["u", "plus", "k"]
    assert words("E = 2 + x") == ["e", "equals", "two", "plus", "x"]
    assert words("Hückel's rule — step-by-step.") == ["huckel's", "rule", "step", "by", "step"]
    assert words("forces C1 to be 0") == words("forces c one to be zero")
    assert words("a single neighbour, normalised") == words("a single neighbor, normalized")


def test_wer():
    assert wer(["a", "b", "c"], ["a", "b", "c"]) == 0
    assert wer(["a", "b", "c"], ["a", "c"]) == 1 / 3          # one deletion
    assert wer(["a", "b"], ["a", "x", "b"]) == 1 / 2          # one insertion
    assert wer(["a", "b", "c", "d"], ["a", "x", "c", "y"]) == 2 / 4  # two substitutions
    assert wer([], ["a"]) == 1.0
