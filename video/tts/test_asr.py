"""Normalisation and word error rate of the ASR round trip (no model needed)."""
from asr import spans, wer, words


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


def test_spans_cut_at_sentence_ends_and_stay_under_the_window():
    timed = [["The", 0.0, 0.2], ["review", 0.3, 0.7], ["says:", 0.8, 1.4], ["crucially,", 2.2, 2.9], ["all", 3.0, 3.2],
             ["rules.", 3.3, 4.0], ["Next", 4.6, 4.9], ["one.", 5.0, 5.5]]
    assert spans(timed, 6.0) == [(0.0, 1.8), (1.8, 4.3), (4.3, 6.0)]
    long = [[f"w{k}", k * 0.5, k * 0.5 + 0.4] for k in range(120)]   # 60 s with no punctuation at all
    s = spans(long, 60.0)
    assert s[0] == (0.0, 24.0) and s[-1][1] == 60.0 and all(b - a <= 24.0 for a, b in s)
    assert all(s[k][1] == s[k + 1][0] for k in range(len(s) - 1))
