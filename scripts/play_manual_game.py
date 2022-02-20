"""
Play game for a predefined word.
"""

import fire

from wordle_benchmark.game import Game


def play_manual_games(word: str, max_guesses: int = 6) -> None:
    """
    Begin a standard manual game.

    Args:
        word: target word.
        max_guesses: max number guesses.
    """

    game = Game(word, max_guesses)

    del game


if __name__ == "__main__":
    fire.Fire(play_manual_games)
