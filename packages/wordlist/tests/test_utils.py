import pytest

from src.wordlist.main import path_jump_to


def test_path_jump_to():
    path_jump_to("../../")
