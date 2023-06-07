import pytest

from src.wordlist.utils import path_jump_to, path_search
from src.wordlist.utils import load_dir


def test_path_jump_to():
    path_jump_to("../../")


def test_path_search():
    path_search("toolbox")


def test_load_dir():
    p = path_jump_to("../../../tmp/")

    files = load_dir(p)
    print(files)
