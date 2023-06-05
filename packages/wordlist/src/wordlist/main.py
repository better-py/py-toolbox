from loguru import logger
from pathlib import Path, PosixPath


def path_jump_to(relative_path: str = "../", from_path: PosixPath = None):
    """从当前目录调整

    :param relative_path: 支持相对路径，"../..", 都是正常处理的
    :param from_path: 从哪个路径开始跳转, 默认不传，取当前运行时目录
    :return:
    """

    # 获取当前工作目录的绝对路径
    base_path = from_path or Path.cwd()

    logger.debug(f"current path: {base_path}, type:{type(base_path)}")
    logger.debug(f"jump with relative_path: {relative_path}")

    # 将相对路径转换为绝对路径
    absolute_path = (base_path / relative_path).resolve()

    logger.debug(f"relative_path: {relative_path}")

    # 打印绝对路径
    logger.debug(f"absolute_path: {absolute_path}, type: {type(absolute_path)}")
    return absolute_path
