"""
Play game for a predefined word.
"""

import logging

import fire
import wordfreq

from wordle_benchmark.game import Game

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def play_manual_games(word: str, max_guesses: int = 6) -> None:
    """
    Begin a standard manual game.

    Args:
        word: target word.
        max_guesses: max number guesses.
    """

    game = Game(word, max_guesses=max_guesses)

    session = game.start_game()
    next(session)

    while True:

        try:
            session.send(input())

            possible_words = game.possible_words
            words_with_freqs = [
                (word, wordfreq.zipf_frequency(word, "en")) for word in possible_words
            ]
            words_with_freqs = sorted(
                words_with_freqs, key=lambda x: x[1], reverse=True
            )[:10]

            print(f"Ten most common possible words: {words_with_freqs}")

        except StopIteration:
            break


if __name__ == "__main__":
    fire.Fire(play_manual_games)
