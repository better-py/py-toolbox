import pytest

from src.wordlist.wordlist import WordListTool


def test_wordlist():
    w = WordListTool()
    w.parse_dir()
