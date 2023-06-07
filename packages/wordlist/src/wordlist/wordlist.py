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

        #
        # vocabularies: 分级词库
        #
        self.words = {
            "cet4": set(),  # 英语4级
            "cet6": set(),  # 英语6级
            "toefl": set(),  # 托福
            "ielts": set(),  # 雅思
            "gre": set(),  # GRE
            #
            # merge:
            #
            "cet4_cet6": set(),  # 英语4级 + 英语6级
            "cet4_cet6_toefl": set(),  # 英语4级 + 英语6级 + 托福
            "cet4_cet6_toefl_ielts": set(),  # 英语4级 + 英语6级 + 托福 + 雅思
            "cet4_cet6_toefl_ielts_gre": set(),  # 英语4级 + 英语6级 + 托福 + 雅思 + GRE
        }

    def parse_xlsx(self, filename: str):
        """解析 xlsx 文件
        :param filename: 文件名
        :return:
        """
        pass

    def parse_vocabulary_by_dirs(self):
        """解析词库文件

        :param
        :return:
        """

        self.parse_dirs()
        self.save_files()

    def save_files(self):
        """保存文件
        :return:
        """
        for k, v in self.words.items():
            f_txt = self.dist_path.joinpath(f"{k}.txt")
            f_json = self.dist_path.joinpath(f"{k}.json")

            # sort:
            v = sorted(v)

            # save to json:
            with open(f_json, "w") as fp:
                fp.write(json.dumps(v))

            # save to txt:
            with open(f_txt, "w") as fp:
                for word in v:
                    fp.write(word + "\n")

    def parse_dirs(self, dirs: str = None, file_type: str = ".png"):
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

            words = set()
            for f in res_dir.iterdir():
                if f.is_file() and f.suffix == file_type:
                    word = f.name.lower().removesuffix(file_type)
                    words.add(word)

            logger.debug(f"words: {len(words)}, dir: {res_dir}")
            # sorted
            self.words[k] = sorted(words)

        # merge words:
        merge_words = set()
        # add cet4
        merge_words.update(self.words["cet4"])
        merge_words.update(self.words["cet6"])

        self.words["cet4_cet6"] = set(sorted(merge_words))
        logger.debug(f"words union: cet4_cet6 = {len(self.words['cet4_cet6'])}")

        # add toefl
        merge_words.update(self.words["toefl"])
        self.words["cet4_cet6_toefl"] = set(sorted(merge_words))
        logger.debug(f"words union: cet4_cet6_toefl = {len(self.words['cet4_cet6_toefl'])}")

        # add ielts
        merge_words.update(self.words["ielts"])
        self.words["cet4_cet6_toefl_ielts"] = set(sorted(merge_words))
        logger.debug(f"words union: cet4_cet6_toefl_ielts = {len(self.words['cet4_cet6_toefl_ielts'])}")

        # add gre
        merge_words.update(self.words["gre"])
        self.words["cet4_cet6_toefl_ielts_gre"] = set(sorted(merge_words))
        logger.debug(f"words union: cet4_cet6_toefl_ielts_gre = {len(self.words['cet4_cet6_toefl_ielts_gre'])}")
