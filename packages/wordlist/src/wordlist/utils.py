from loguru import logger
from pathlib import Path, PosixPath
from typing import Union


def traverse_dir(path: Path, only_file: bool = True) -> list:
    """遍历目录下所有文件

    :param path: 目录路径
    :param only_file: 是否只返回文件
    :return: 文件路径列表
    """
    logger.debug(f"traverse dir: {path}")

    if not path.exists():
        logger.warning(f"path: {path} not exists")
        return []

    if only_file:
        return [x for x in path.iterdir() if x.is_file()]

    return [x for x in path.iterdir()]


def path_search_by_folder(path: Path | str = ".", folder_name: str = ".git") -> Path | None:
    """递归搜索包含某个文件夹的根目录

    :param path: 搜索开始路径, 类型可以是 str / Path
    :param folder_name: 指定搜索的文件夹名称, 默认为 `.git/`
    :return: 匹配到的根目录
    """

    # 获取当前目录
    current_dir = Path(path).resolve()

    # 判断当前目录是否存在.git文件夹
    git_folder = current_dir / folder_name
    if git_folder.is_dir() and not git_folder.is_symlink():
        logger.debug(f"find {folder_name} in {current_dir}")
        return current_dir

    # 如果不存在.git文件夹，继续向上搜索
    parent_dir = current_dir.parent
    if parent_dir == current_dir:
        logger.warning(f"can not find {folder_name} in {path}")
        # 已经到达根目录，退出递归
        return None
    else:
        # logger.debug(f"search {folder_name} in {parent_dir}")
        return path_search_by_folder(parent_dir, folder_name)


def path_search(where: str, path: Path = None) -> Path | None:
    """模糊匹配+路径跳转

    :param where: 某个目录名称
    :param path: 路径下搜索
    :return: 匹配到 where 的绝对路径
    """
    base_path = path or Path.cwd()
    logger.debug(f"search: [{where}], in path: {base_path}")

    if not base_path.exists():
        logger.error(f"base_path: {base_path} not exists, type: {type(base_path)}")
        return None

    bp = base_path.absolute().as_posix()
    if not (where in bp):
        logger.error(f"where: {where} not in base_path: {bp}")
        return None

    dist_dir = bp.split(where)[0]
    logger.debug(f"dist_dir: {dist_dir}")

    dist_path = Path(dist_dir).joinpath(where)
    logger.debug(f"dist_path: {dist_path}, type: {type(dist_path)}")

    if not dist_path.exists():
        logger.error(f"dist_path: {dist_path} not exists")
        return None
    return dist_path


def path_jump_to(relative_path: str = "../", from_path: Path = None) -> Path:
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
