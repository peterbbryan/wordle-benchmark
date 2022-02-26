"""
Classes to represent English words.
"""

import json
import pathlib
import random
from abc import ABC
from typing import List, Optional

import requests


class Dictionary(ABC):
    """ Dictionary ABC """

    def __init__(
        self, word_list: List[str], word_len: int, seed: Optional[int] = None
    ) -> None:
        """
        Args:
            word_list: list of all valid words.
            word_len: filter to apply to word length.
            seed: optional randomization seed to apply.
                NOTE! The default value is None and will result in no shuffle!
        """

        self._word_len = word_len
        self._word_list = word_list

        self._filtered_word_list = Dictionary._filter_by_len(word_list, word_len)
        self._randomized_order = Dictionary._randomize(self._filtered_word_list, seed)

    def __contains__(self, value):
        return self.word_list.__contains__(value)

    def __iter__(self):
        return self.word_list.__iter__()

    @property
    def word_len(self) -> int:  # pylint: disable=missing-function-docstring
        return self._word_len

    @property
    def word_list(self) -> List[str]:  # pylint: disable=missing-function-docstring
        return self._randomized_order.copy()

    @staticmethod
    def _filter_by_len(word_list: List[str], word_len: int) -> List[str]:
        """
        Filter to words of a specific length.
        NOTE: This really should be parallelized.

        Args:
            word_list: list of all valid words.
            word_len: filter to apply to word length.
        Returns:
            Words of length word_len.
        """

        return [word for word in word_list if len(word) == word_len]

    @staticmethod
    def _randomize(word_list: List[str], seed: Optional[int]) -> List[str]:
        """
        Randomize dictionary word list based on optional seed.
        NOTE: returns a copy, no inplace modification.

        Args:
            word_list: list of all valid words.
            seed: optional randomization seed to apply.
                NOTE! The default value is None and will result in no shuffle!
        Returns:
            Generate randomized dictionary order based on seed.
        """

        word_list_copy = word_list.copy()

        if seed is None:
            return word_list_copy

        random.Random(seed).shuffle(word_list_copy)

        return word_list_copy


class CustomDictionary(Dictionary):  # pylint: disable=too-few-public-methods
    """ CustomDictionary from lists """

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        raise NotImplementedError


class LocalDictionary(Dictionary):  # pylint: disable=too-few-public-methods
    """ LocalDictionary from local file """

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        raise NotImplementedError


class RemoteDictionary(Dictionary):  # pylint: disable=too-few-public-methods
    """ RemoteDictionary from remote source """

    def __init__(
        self, remote_source: str, word_len: int, seed: Optional[int] = None
    ) -> None:
        """
        Args:
            remote_source: remote URL for dictionary.
            word_len: filter to apply to word length.
            seed: optional randomization seed to apply.
                NOTE! The default value is None and will result in no shuffle!
        """

        word_list = RemoteDictionary._get_remote_source(remote_source)

        super().__init__(word_list=word_list, word_len=word_len, seed=seed)

    @staticmethod
    def _get_remote_source(remote_source: str) -> List[str]:
        """
        Download data from remote dictionary file.

        Args:
            remote_source: URL of remote.
        Returns:
            Word list.
        """

        return {".json": RemoteDictionary._list_from_json(remote_source)}[
            pathlib.Path(remote_source).suffix
        ]

    @staticmethod
    def _list_from_json(remote_source: str) -> List[str]:
        """
        Download JSON dictionary with key for words, arbitrary values.

        Args:
            remote_source: URL of remote JSON.
        Returns:
            Word list.
        """

        text = json.loads(requests.get(remote_source).text)

        return [word.lower() for word in sorted(text.keys()) if word.isalpha()]
