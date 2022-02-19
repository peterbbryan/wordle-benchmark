"""
Classes to represent English words.
"""

from abc import ABC


class Dictionary(ABC):  # pylint: disable=too-few-public-methods
    """
    Dictionary ABC.
    """

    ...


class LocalDictionary(Dictionary):  # pylint: disable=too-few-public-methods
    """
    Dictionary from local file
    """

    def __init__(self) -> None:
        raise NotImplementedError


class RemoteDictionary(Dictionary):  # pylint: disable=too-few-public-methods
    """
    Dictionary from remote source.
    """

    def __init__(self) -> None:
        raise NotImplementedError
