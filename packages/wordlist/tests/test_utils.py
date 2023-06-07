import pytest
from loguru import logger

from src.wordlist.utils import path_jump_to, path_search, traverse_dir


def test_path_jump_to():
    path_jump_to("../../")


def test_path_search():
    path_search("toolbox")


def test_load_dir():
    p = path_jump_to("../../../tmp/")

    files = traverse_dir(p)
    print(files)


def test_load_dir2():
    root_dir = path_search("toolbox")

    res_dirs = [
        "tmp/English-words-cards/CET4/images",
        "tmp/English-words-cards/CET6/images",
        "tmp/English-words-cards/TOEFL/images",
        "tmp/English-words-cards/IELTS/images",
        "tmp/English-words-cards/GRE/images",
    ]

    for res_dir in res_dirs:
        res_dir = root_dir.joinpath(res_dir)
        # files = traverse_dir(res_dir)

        files = set()
        for f in res_dir.iterdir():
            if f.is_file() and f.suffix == '.png':
                word = f.name.lower().removesuffix(".png")
                # logger.debug(f"file name: {f.name}, word: {word}")
                files.add(word)

        logger.debug(f"files: {len(files)}, dir: {res_dir}")

