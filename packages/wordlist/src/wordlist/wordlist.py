import json
from collections import OrderedDict
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

    def parse_txt(self):

        res = "IELTS/IELTS Word List.txt"
        file = self.resource_path.joinpath(res)

        # parse
        words = {}
        with open(file, "r") as fp:
            for line in fp.readlines():
                line = line.strip()
                if not line:
                    continue

                # clean line:
                # start with alphabet:
                if not line[0].isascii():
                    logger.warning(f"⚠️ skip line: {line}")
                    continue
                if line.find("Word List") != -1:
                    logger.warning(f"⚠️ skip line: {line}")
                    continue

                # =============

                # if line.count("/") == 2:
                #     # ok:
                #     ret = line.split("/", maxsplit=2)
                #     if len(ret) != 3:
                #         logger.warning(f"🍄️ skip line: {line}")
                #         continue
                #     word, pronounce, meaning = ret
                #     word = word.strip("*")

                # ok:
                ret = line.split(maxsplit=2)
                if len(ret) != 3:
                    logger.warning(f"⚠️ skip line: {len(ret)}, {ret}")
                    continue
                word, pronounce, meaning = ret
                word = word.lower().strip("*")  # 小写+去掉*

                #
                # fix word:
                #
                if pronounce.count("/") == 0 and pronounce.count("[") == 0 and pronounce.count("{") == 0:
                    word = f"{word} {pronounce}".strip("*")  # 短语
                    pronounce = ""
                    if meaning.count("*") > 0:
                        head, tail = meaning.split("*", maxsplit=1)
                        word = f"{word} {head}".strip("*")  # 短语
                        meaning = tail

                    logger.warning(f"✅️ fix word: {word}, {pronounce}, {meaning}")
                elif pronounce.count("/") == 1 and meaning.count("/") > 0:  # 音标切分异常，从词义中提取音标部分
                    p_fix, meaning = meaning.split("/", maxsplit=1)
                    pronounce = f"{pronounce}{p_fix}/"
                    logger.warning(f"⛔️ fix pronounce: {word}, {pronounce}, {meaning}")

                # 统一音标格式:
                if pronounce.count("{") > 0:
                    pronounce = pronounce.replace("{", "/").replace("}", "/")
                elif pronounce.count("[") > 0:
                    pronounce = pronounce.replace("[", "/").replace("]", "/")

                words[word] = {
                    "pronounce": pronounce.strip(),
                    "meaning": meaning.strip(),
                }

        # ====================
        logger.debug(f"words: {len(words)}")
        return words

    def save_csv(self, data: dict):
        """保存 csv 文件
        :return:
        """

        dist_file = self.dist_path.joinpath("ielts.csv")  # 雅思词汇表 + 发音 + 词义

        # sort:
        data = OrderedDict(sorted(data.items(), key=lambda x: x[0]))

        # save to csv:
        with open(dist_file, "w") as fp:
            for k, v in data.items():
                fp.write(f"{k}, {v['pronounce']}, {v['meaning']}\n")

    def parse_vocabulary_by_dirs(self):
        """解析词库文件

        :param
        :return:
        """

        self.parse_dirs()
        self.save_files()

    def handle2(self):
        """处理词库文件
        :return:
        """
        # parse:
        self.parse_dir_files()
        self.save_files("2")

    def handle3(self):
        words = self.parse_txt()
        self.save_csv(words)

    def save_files(self, file_suffix: str = None):
        """保存文件

        :param file_suffix: 文件后缀
        :return:
        """
        for k, v in self.words.items():
            kk = f"{k}" if not file_suffix else f"{k}_{file_suffix}"
            f_txt = self.dist_path.joinpath(f"{kk}.txt")
            f_json = self.dist_path.joinpath(f"{kk}.json")

            # sort:
            v = sorted(v)

            # save to json:
            with open(f_json, "w") as fp:
                fp.write(json.dumps(v))

            # save to txt:
            with open(f_txt, "w") as fp:
                for word in v:
                    fp.write(word + "\n")

    def parse_dir_files(self):
        res_dirs = {
            "cet4": "English-words-cards/CET4/manifest.json",
            "cet6": "English-words-cards/CET6/manifest.json",
            "toefl": "English-words-cards/TOEFL/manifest.json",
            "ielts": "English-words-cards/IELTS/manifest.json",
            "gre": "English-words-cards/GRE/manifest.json",
        }

        # parse json file:
        for k, v in res_dirs.items():
            res_dir = self.resource_path.joinpath(v)

            words = set()
            with open(res_dir, "r") as fp:
                data = json.loads(fp.read())
                items = data["items"] or []

                for item in items:
                    v = item["url"] or ""
                    if not v:
                        continue

                    # fmt:
                    word = v.lower().rsplit("/", 1)[-1].removesuffix(".png")
                    # logger.debug(f"word: {word}")
                    if word in words:
                        logger.warning(f"word: {word} already exist in {res_dir}.")
                    # save set:
                    words.add(word)

            # save:
            logger.debug(f"words num: {len(words)}, dir: {res_dir}")
            self.words[k] = sorted(words)

        # ===================================================

        self.merge_words()

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
                    # if exist
                    if word in words:
                        logger.warning(f"word: {word} already exist in {res_dir}.")
                    words.add(word)

            logger.debug(f"words: {len(words)}, dir: {res_dir}")
            # sorted
            self.words[k] = sorted(words)

        # ===================================================

        # merge words:
        self.merge_words()

    def merge_words(self):
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
