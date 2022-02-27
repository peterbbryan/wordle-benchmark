"""
Simple demo of the ABC interface of the sample agent.
"""

import logging
from typing import TYPE_CHECKING, List

import fire
import wordfreq

from wordle_benchmark.agent import Agent
from wordle_benchmark.benchmarker import Benchmark

if TYPE_CHECKING:
    from wordle_benchmark.game import Game

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class SampleSimpleAgent(Agent):  # pylint: disable=too-few-public-methods
    """ Basic example of a Wordle agent. """

    @staticmethod
    def _guess_one(game: "Game") -> str:
        """
        First guess logic.

        Args:
            game: Wordle game.
        Returns:
            Predicted word.
        """

        del game

        return "crane"

    @staticmethod
    def _every_other_guess(game: "Game") -> str:
        """
        Guess the most common word still possible.

        Args:
            game: Wordle game.
        Returns:
            Predicted word.
        """

        possible_words = game.possible_words
        words_with_freqs = [
            (word, wordfreq.zipf_frequency(word, "en")) for word in possible_words
        ]
        word_with_highest_freq: str = sorted(
            words_with_freqs, key=lambda x: x[1], reverse=True
        )[0][0]

        return word_with_highest_freq

    def play(self, game: "Game") -> str:
        """
        Args:
            game: Game with game state information.
        Returns:
            String of guess word.
        """

        if game.n_guesses == 0:
            predicted = self._guess_one(game)
        else:
            predicted = self._every_other_guess(game)

        print(f"This agent predicts {predicted}")
        return predicted


def play_custom_agents_games(target_words: List[str]) -> None:
    """
    Game play for a custom agent.

    Args:
        target_words: list of target words.
    """

    benchmark = Benchmark(SampleSimpleAgent(), target_words=target_words)
    benchmark_results = benchmark.run_games()

    print(benchmark_results)


if __name__ == "__main__":
    fire.Fire(play_custom_agents_games)
