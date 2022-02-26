"""
Classes to represent Wordle words we want to guess and our guesses.
"""

from abc import ABC
from enum import Enum, auto
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from wordle_benchmark.dictionary.wordle_dictionary import Dictionary


class LetterState(Enum):
    """ Enum of possible Wordle letter states """

    GREEN = auto()
    YELLOW = auto()
    BLACK = auto()


MatchState = Tuple[str, LetterState]


class Word(ABC):
    """ Word ABC """

    def __init__(self, word: str) -> None:
        """
        Args:
            word: Guess word or target word.
        """

        self._word = word.lower()

    def __contains__(self, value):
        return value in self._word

    def __iter__(self):
        return self._word.__iter__()

    def __len__(self) -> int:
        return len(self._word)

    def __str__(self) -> str:
        return self._word

    def in_dictionary(self, dictionary: "Dictionary") -> bool:
        """
        Check if a guess is in a dictionary.

        Args:
            dictionary: Dictionary to check membership in.
        """

        return self._word in dictionary

    def is_valid(self, word_len: int) -> bool:
        """
        Check if a guess is valid given board length constraint.

        Args:
            word_len: Length of word.
        """

        if not str(self).isalpha():
            return False

        if len(self) != word_len:
            return False

        return True


class TargetWord(Word):  # pylint: disable=too-few-public-methods
    """ Word we are trying to guess """

    ...


class GuessWord(Word):
    """ Word we have guessed """

    def compare_to(self, target_word: TargetWord) -> List[MatchState]:
        """
        Check matching letters between the guess and the target word.

        Args:
            target_word: Actual word being guessed.
        """

        match_list: List[MatchState] = []

        for self_letter, target_letter in zip(self, target_word):
            if self_letter == target_letter:
                match_list.append((self_letter, LetterState.GREEN))
            elif self_letter in target_word:
                match_list.append((self_letter, LetterState.YELLOW))
            else:
                match_list.append((self_letter, LetterState.BLACK))

        return match_list
