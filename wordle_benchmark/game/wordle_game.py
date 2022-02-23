"""
Classes to represent game logic.
"""

import logging
from enum import Enum, auto
from typing import Generator, List, Tuple

from wordle_benchmark.dictionary.wordle_dictionary import Dictionary, RemoteDictionary
from wordle_benchmark.game.wordle_words import (
    GuessWord,
    LetterState,
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


class Game:  # pylint: disable=too-many-instance-attributes
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

        self._greens: List[Tuple[str, int]] = []
        self._yellows: List[Tuple[str, int]] = []
        self._blacks: List[str] = []

        self._game_state = GameStates.UNSTARTED

    @property
    def possible_words(self) -> List[str]:
        """
        Returns:

        """

        possible_words = []

        for word in self._dictionary.word_list:

            # remove a word if it has a black character
            if any(character in word for character in self._blacks):
                continue

            if not all(word[ind] == character for character, ind in self._greens):
                continue

            if not all(character in word for character, _ in self._yellows):
                continue

            if any(word[ind] == character for character, ind in self._yellows):
                continue

            possible_words.append(word)

        return possible_words

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

    def _handle_match(self, match_state: MatchState, ind: int) -> None:
        """


        Args:
            match_state:
            ind:
        """

        character, letter_state = match_state

        assert character.isalpha(), "Character must be standard alphabet"
        assert len(character) == 1, "A character should be length one"

        if letter_state == LetterState.BLACK:
            self._blacks.append(character)

        elif letter_state == LetterState.YELLOW:
            self._yellows.append((character, ind))

        elif letter_state == LetterState.GREEN:
            self._greens.append((character, ind))

        else:
            raise ValueError("Unknown letter state")

    def _register_guess(self, guess_word: GuessWord) -> None:
        """
        Register guess and update game state if necessary.

        Args:
            guess_word: Word guessed by user.
        """

        if not guess_word.is_valid(self._word_len):
            log.warning(
                "'%s' is not valid word of len %d", str(guess_word), self._word_len
            )
            return

        if not guess_word.in_dictionary(self._dictionary):
            log.warning("'%s' is not in the dictionary", str(guess_word))

        # black, yellow, green match outcome given guess
        comparison: List[MatchState] = guess_word.compare_to(self._target_word)
        self._guesses.append(comparison)

        for ind, match in enumerate(comparison):
            self._handle_match(match, ind)

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

            log.debug("These remain possible: %s", self.possible_words)
