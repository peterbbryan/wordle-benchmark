"""
Play game for a predefined word.
"""

import logging

import fire

from wordle_benchmark.game import Game

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def play_manual_games(word: str) -> None:
    """
    Begin a standard manual game.

    Args:
        word: target word.
    """

    game = Game(word)

    session = game.start_game()
    next(session)

    while True:

        try:
            session.send(input())
            print(game.last_match)

        except StopIteration:
            break


if __name__ == "__main__":
    fire.Fire(play_manual_games)
