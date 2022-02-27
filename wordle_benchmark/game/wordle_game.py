"""
Classes to represent game logic.
"""

import logging
from enum import Enum, auto
from typing import TYPE_CHECKING, Generator, List, Optional, Tuple

from wordle_benchmark.dictionary.wordle_dictionary import RemoteDictionary
from wordle_benchmark.game.wordle_words import GuessWord, LetterState, TargetWord

if TYPE_CHECKING:

    from wordle_benchmark.dictionary.wordle_dictionary import Dictionary
    from wordle_benchmark.game.wordle_words import MatchState

log = logging.getLogger(__name__)


DEFAULT_DICTIONARY = RemoteDictionary(
    "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json",  # pylint: disable=line-too-long
    word_len=5,
    seed=42,
)


class GameState(Enum):
    """ Enum of possible Wordle game states """

    UNSTARTED = auto()
    STARTED = auto()
    FINISHED = auto()


class IllegalGuessError(Exception):
    """ Guess is not the right length or is not a word """


class Game:  # pylint: disable=too-many-instance-attributes
    """ Logic for game """

    def __init__(
        self,
        target_word: str,
        dictionary: "Dictionary" = DEFAULT_DICTIONARY,
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
        self._guesses: List[List["MatchState"]] = []

        self._greens: List[Tuple[str, int]] = []
        self._yellows: List[Tuple[str, int]] = []
        self._blacks: List[str] = []

        self._game_state = GameState.UNSTARTED

    @property
    def last_match(self) -> Optional[List["MatchState"]]:
        """ Most recent match. """

        if len(self._guesses) == 0:
            return None

        return self._guesses[-1]

    @property
    def n_guesses(self) -> int:
        """ Number of guesses so far. """

        return len(self._guesses)

    @property
    def possible_words(self) -> List[str]:
        """ Words that are still legal based on the dictionary. """

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

    @property
    def success(self) -> bool:
        """ Whether the most recent guess was correct. """

        last_match = self.last_match

        if last_match is None:
            return False

        return all(letter_state == LetterState.GREEN for _, letter_state in last_match)

    def _transition_to_started(self):
        """ State machine transition to started """

        assert self._game_state == GameState.UNSTARTED

        log.info("Starting game...")
        self._game_state = GameState.STARTED

    def _transition_to_finished(self):
        """ State machine transition to finished. """

        assert self._game_state == GameState.STARTED

        log.info("Ending game")
        self._game_state = GameState.FINISHED

    def _handle_match(self, match_state: "MatchState", ind: int) -> None:
        """
        Update knowledge of black, yellow, green letters after guess.
        A match state represents a letter and it's black, yellow, green state.

        Args:
            match_state: Tuple[str, LetterState].
            ind: Letter position in guess word.
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

    def _register_guess(self, guess_word: "GuessWord") -> bool:
        """
        Register guess and update game state if necessary.

        Args:
            guess_word: Word guessed by user.
        Raises:
            IllegalGuessError in the event of an illegal word.
        """

        if not guess_word.is_valid(self._word_len):
            raise IllegalGuessError(
                f"{guess_word} is not valid word of len {self._word_len}"
            )

        if not guess_word.in_dictionary(self._dictionary):
            raise IllegalGuessError(f"{guess_word} is not in the dictionary")

        # black, yellow, green match outcome given guess
        comparison: List["MatchState"] = guess_word.compare_to(self._target_word)
        self._guesses.append(comparison)

        for ind, match in enumerate(comparison):
            self._handle_match(match, ind)

        # if all characters matched, that's the end of the game
        return self.success

    def start_game(self) -> Generator[None, str, None]:
        """
        Initiate game, await user input.
        NOTE: should be refactored to async await.

        Sample use of a manual game:
            game = Game(word, max_guesses=max_guesses)
            session = game.start_game()
            next(session)

            while True:
                session.send(input())

        Returns:
            A generator. Use ".send()" to pass guesses.
        """

        self._transition_to_started()

        log.debug("The target word is %s", self._target_word)

        while not self._game_state == GameState.FINISHED:

            log.info("Waiting for guess...")
            guess_word_str = yield
            log.info("Received guess %s", guess_word_str)
            guess_word = GuessWord(guess_word_str)

            try:
                end_game: bool = self._register_guess(guess_word)
            except IllegalGuessError as exception:
                log.warning(exception)
            else:
                if end_game:
                    self._transition_to_finished()
                    log.info("Correct! The word was %s", self._target_word)
                    break

                log.debug("These remain possible: %s", self.possible_words)

                if len(self._guesses) > self._max_guesses:
                    self._transition_to_finished()
                    log.info("Uh oh! You lose!")
                    break
