from loguru import logger
from src.wordlist.utils import path_jump_to, path_search, load_dir


class WordListTool(object):
    """
    词库工具, 清洗一些词库数据（CET4,CET6, GRE, TOEFL, IELTS, etc.）
    """

    def __init__(self, root_dir: str = None, resource_dir: str = None):
        self._root_dir = root_dir or "toolbox"
        self._resource_dir = resource_dir or "tmp"
        self._dist_dir = "dist"

        # 默认的词库源根路径是： tmp/
        self.resource_path = path_search(self._root_dir).joinpath(self._resource_dir)
        # 默认处理结果根路径：tmp/dist/
        self.dist_path = self.resource_path.joinpath(self._dist_dir)

        logger.debug(f"resource_path: {self.resource_path}, dist_path: {self.dist_path}")

    def parse_xlsx(self, filename: str):
        """解析 xlsx 文件
        :param filename: 文件名
        :return:
        """
        pass

    def parse_dir(self, dir_path: str, file_type: str = ".png"):
        """解析目录下所有文件

        :param dir_path: 目录路径
        :param file_type: 目标文件类型
        """
        pass
