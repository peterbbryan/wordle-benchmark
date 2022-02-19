"""
Logic to check that the Wordle word representations work as expected.
"""

from wordle_benchmark.game import GuessWord, LetterState, TargetWord, Word


def test_word_iter():
    """
    Verify that word iteration behaves as expected.
    """

    sample_str = "cause"
    sample_word = Word(sample_str)

    for str_letter, word_letter in zip(sample_str, sample_word):
        assert str_letter == word_letter, "Word iter broken"


def test_word_contains():
    """
    Verify that word letter containers behaves as expected.
    """

    assert "a" in Word("cause"), "Contains logic incorrect"
    assert "a" not in Word("pools"), "Containers logic incorrect"


def test_word_comparison():
    """
    Verify that word comparison behaves as expected.
    """

    guess_word = GuessWord("cause")
    target_word = TargetWord("coals")

    matches = guess_word.compare_to(target_word)
    expected_matches = [
        ("c", LetterState.GREEN),
        ("a", LetterState.YELLOW),
        ("u", LetterState.BLACK),
        ("s", LetterState.YELLOW),
        ("e", LetterState.BLACK),
    ]

    assert matches == expected_matches, "Match logic broken"
