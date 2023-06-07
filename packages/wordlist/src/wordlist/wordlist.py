import json

from loguru import logger
from src.wordlist.utils import path_jump_to, path_search, traverse_dir


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

        # mkdir:
        self.dist_path.mkdir(parents=True, exist_ok=True)

        logger.debug(f"resource_path: {self.resource_path}, dist_path: {self.dist_path}")

    def parse_xlsx(self, filename: str):
        """解析 xlsx 文件
        :param filename: 文件名
        :return:
        """
        pass

    def parse_dir(self, dirs: str = None, file_type: str = ".png"):
        """解析目录下所有文件

        :param dirs: 目录路径
        :param file_type: 目标文件类型
        """

        res_dirs = dirs or {
            "cet4": "English-words-cards/CET4/images",
            "cet6": "English-words-cards/CET6/images",
            "toefl": "English-words-cards/TOEFL/images",
            "ielts": "English-words-cards/IELTS/images",
            "gre": "English-words-cards/GRE/images",
        }

        for k, v in res_dirs.items():
            res_dir = self.resource_path.joinpath(v)
            logger.debug(f"res_dir: {res_dir}")

            words = set()
            for f in res_dir.iterdir():
                if f.is_file() and f.suffix == file_type:
                    print(f"file name: {f.name}, file path: {f.absolute()}")
                    word = f.name.lower().removesuffix(file_type)
                    words.add(word)
                logger.debug(f"words: {len(words)}, dir: {res_dir}")

            #
            #
            #
            f_txt = self.dist_path.joinpath(f"{k}.txt")
            f_json = self.dist_path.joinpath(f"{k}.json")

            # save to txt:
            with open(f_txt, "w") as fp:
                for word in words:
                    fp.write(word + "\n")
            # save to json:
            with open(f_json, "w") as fp:
                fp.write(json.dumps(list(words)))
