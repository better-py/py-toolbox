import click
from loguru import logger
from src.wordlist.utils import path_jump_to


@click.command()
@click.option("--input_dir", default="", help="input dir")
@click.option("--output_dir", default="", help="output dir")
def main(input_dir, output_dir):
    logger.debug(f"input args: {input_dir}, {output_dir}")

    logger.debug("hello world")

    path_jump_to(relative_path="../", from_path=None)

    pass


if __name__ == '__main__':
    main()
