"""
Classes to measure Wordle agent performance.
"""

from dataclasses import dataclass
import logging
import time
from typing import TYPE_CHECKING, List

import numpy as np

from wordle_benchmark.game import Game

if TYPE_CHECKING:
    from wordle_benchmark.agent import Agent

log = logging.getLogger(__name__)


@dataclass
class BenchmarkResults:
    """ Quantitative summarization of game outcomes """

    average_n_turns: float
    average_turn_time: float
    percent_successes: float
    std_turn_time: float


class Benchmark:  # pylint: disable=too-few-public-methods
    """ Performance measuring logic """

    def __init__(self, agent: "Agent", target_words: List[str], **game_kwargs):
        """
        Args:
            agent: Wordle playing agent.
            target_words: List of target words.
            game_kwargs: Optional game config keyword arguments.
        """

        self._agent = agent
        self._target_words = target_words
        self._game_kwargs = game_kwargs

    def run_games(self) -> BenchmarkResults:
        """ Run games against agent and record results """

        successes: List[bool] = []
        n_turns: List[int] = []
        turn_times: List[float] = []

        for target_word in self._target_words:

            log.info('Playing game with target word "%s"', target_word)

            game = Game(target_word, **self._game_kwargs)

            session = game.start_game()
            next(session)

            while True:

                try:

                    start = time.time()
                    session.send(self._agent.play(game))
                    end = time.time()

                    turn_times.append(end - start)

                except StopIteration:
                    break

            n_turns.append(game.n_guesses)
            successes.append(game.success)

        average_n_turns = np.mean(n_turns)
        average_turn_time = np.mean(turn_times)
        percent_successes = np.sum(successes) / len(successes)
        std_turn_time = np.std(turn_times)

        return BenchmarkResults(
            average_n_turns=average_n_turns,
            average_turn_time=average_turn_time,
            percent_successes=percent_successes,
            std_turn_time=std_turn_time,
        )
