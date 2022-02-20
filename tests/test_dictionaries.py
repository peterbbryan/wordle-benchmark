"""
Logic to check that the Wordle dictionary representations work as expected.
"""

from wordle_benchmark.dictionary import RemoteDictionary


def test_remote_dictionary_connection():
    """
    Verify that remote dictionary downloads appropriately.
    """

    remote_source = "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json"  # pylint: disable=line-too-long
    dictionary = RemoteDictionary(remote_source=remote_source, word_len=5)

    all_words = list(dictionary)

    first_word = all_words[0]
    last_word = all_words[-1]

    assert first_word == "abaca"
    assert last_word == "zymic"

    assert len(all_words) == 6278
