"""
Classes to represent Wordle playing agents.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wordle_benchmark.game import Game


class Agent(ABC):  # pylint: disable=too-few-public-methods
    """ Wordle agent """

    @abstractmethod
    def play(self, game: "Game") -> str:
        """
        Args:
            game: Game with game state information.
        Returns:
            String of guess word.
        """

        ...
