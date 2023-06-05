import pytest

from src.wordlist.utils import path_jump_to


def test_path_jump_to():
    path_jump_to("../../")
