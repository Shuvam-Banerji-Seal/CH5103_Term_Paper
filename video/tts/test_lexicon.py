"""The pronunciation lexicon keeps punctuation, capitals, possessives and the written/spoken correspondence."""
from lexicon import LEXICON, pairs, spoken


def test_respelling_keeps_punctuation_and_case():
    assert spoken("The wavefunction, antisymmetric.") == "The wave function, anti symmetric."
    assert spoken("Aufbau fails; non-aufbau states.") == "Owf bow fails; non owf bow states."
    assert spoken("the wavefunction's sign") == "the wave function's sign"
    assert spoken("(chi)") == "(kai)"


def test_untouched_text_is_identical():
    t = "Hund's rule: the triplet lies lower — by two K."
    assert spoken(t) == t


def test_pairs_cover_every_written_token():
    t = "A meta xylylene wavefunction."
    p = pairs(t)
    assert [w for w, _ in p] == t.split()
    assert p[2] == ("xylylene", "zylileen") and p[3] == ("wavefunction.", "wave function.")


def test_entries_are_lower_case_keys():
    assert all(k == k.lower() for k in LEXICON)
