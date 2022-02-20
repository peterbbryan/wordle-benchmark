"""
Classes to represent game logic.
"""

from wordle_benchmark.dictionary.wordle_dictionary import Dictionary, RemoteDictionary
from wordle_benchmark.game.wordle_words import TargetWord

DEFAULT_DICTIONARY = RemoteDictionary(
    "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json",  # pylint: disable=line-too-long
    word_len=5,
    seed=42,
)


class GameManager:  # pylint: disable=too-few-public-methods
    """
    Wordle game logic.
    """

    def __init__(
        self, dictionary: Dictionary = DEFAULT_DICTIONARY, max_guesses: int = 6
    ):
        """
        Args:
            dictionary: Wordle dictionary.
            max_guesses: Max number of guesses.
        """

        self._dictionary = dictionary
        self._word_len = dictionary.word_len
        self._max_guesses = max_guesses
        self._current_guess_count = 0


class Game:  # pylint: disable=too-few-public-methods
    """
    Logic for game.
    """

    def __init__(self, target_word: str, max_guesses: int):
        """
        Args:
            word: target word.
            max_guesses: max number guesses.
        """

        del max_guesses

        self._target_word = TargetWord(target_word)
