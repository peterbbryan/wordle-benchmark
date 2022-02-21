"""
Classes to represent game logic.
"""

import logging
from enum import Enum, auto
from typing import Generator, List

from wordle_benchmark.dictionary.wordle_dictionary import Dictionary, RemoteDictionary
from wordle_benchmark.game.wordle_words import (
    GuessWord,
    MatchState,
    TargetWord,
)

log = logging.getLogger(__name__)


DEFAULT_DICTIONARY = RemoteDictionary(
    "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json",  # pylint: disable=line-too-long
    word_len=5,
    seed=42,
)


class GameStates(Enum):
    """
    Enum of possible Wordle game states.
    """

    UNSTARTED = auto()
    STARTED = auto()
    FINISHED = auto()


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

    def __init__(
        self,
        target_word: str,
        dictionary: Dictionary = DEFAULT_DICTIONARY,
        max_guesses: int = 6,
    ):
        """
        Args:
            word: target word.
            dictionary: Wordle dictionary.
            max_guesses: max number guesses.
        """

        self._target_word = TargetWord(target_word)
        self._dictionary = dictionary
        self._max_guesses = max_guesses
        self._word_len = len(target_word)
        self._guesses: List[List[MatchState]] = []

        self._game_state = GameStates.UNSTARTED

    def _transition_to_started(self):
        """
        State machine transition to started.
        """

        assert self._game_state == GameStates.UNSTARTED

        log.info("Starting game...")
        self._game_state = GameStates.STARTED

    def _transition_to_finished(self):
        """
        State machine transition to finished.
        """

        assert self._game_state == GameStates.STARTED

        log.info("Ending game")
        self._game_state = GameStates.FINISHED

    def _register_guess(self, guess_word: GuessWord) -> None:
        """
        Register guess and update game state if necessary.

        Args:
            guess_word: Word guessed by user.
        """

        if guess_word.is_valid(self._word_len):
            log.warning(
                "%s is not valid word of len %d", str(guess_word), self._word_len
            )
            return

        comparison = guess_word.compare_to(self._target_word)
        self._guesses.append(comparison)

        print(self._guesses)

    def start_game(self) -> Generator[None, str, None]:
        """
        Initiate game, await user input.
        NOTE: should be refactored to async await.
        """

        self._transition_to_started()

        log.debug("The target word is %s", self._target_word)

        while True:

            log.info("Waiting for guess...")
            guess_word_str = yield
            log.info("Received guess %s", guess_word_str)
            guess_word = GuessWord(guess_word_str)

            self._register_guess(guess_word)
