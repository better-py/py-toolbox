import json
import os
import shutil
from typing import Optional, Callable

import click


class RssHubFeedsParser(object):
    """
    rssHub feeds parser

    """

    BASE_URL = "https://rsshub.app/"
    # telegram:
    URL_PREFIX_TG = "telegram/channel/"

    def __init__(self, txt_file: str = None):
        # root dir:
        self._current_dir = os.path.dirname(os.path.abspath(__file__))

        # input:
        self.f_in_txt = txt_file or os.path.join(self._current_dir, 'build/rss.txt')
        # output
        self.f_out_txt = os.path.join(self._current_dir, 'build/rss.dist.json')

    def parse_tg_channel(self):
        """
        parse tg channel from txt file
        :return:
        """
        data = self.read_txt_file(self.fmt_tg_channel)
        self.save(data)

    def fmt_tg_channel(self, line: str) -> str:
        """
        format tg channel
        :param line:
        :return:
        """
        prefix = "telegram/channel/"
        split_sep = "t.me/"
        return self.fmt_line(line, split_sep, prefix)

    def fmt_line(self, line: str, split_sep: str, prefix: str) -> Optional[str]:
        """
        format tg channel
        :param line:
        :param split_sep: split separator
        :param prefix: rssHub prefix
        :return:
        """
        if line.startswith('#'):
            return None

        if line.find(split_sep) > 0:
            _, item = line.rsplit(split_sep, maxsplit=1)
            s = f"{self.BASE_URL}{prefix}{item}"
            print(f"rss: {s}")
            return s
        return None

    def read_txt_file(self, task_fn: Callable) -> list:
        """
        read raw txt file
        :param task_fn: function to format line
            https://docs.python.org/zh-cn/3/library/typing.html#typing.Callable
        :return:
        """
        result = set()
        with open(self.f_in_txt, 'r') as f:
            for line in f.readlines():
                raw = line.strip()
                # fmt:
                item = task_fn(raw) if task_fn else raw
                if item:
                    result.add(item)
        print(f"parse count: {len(result)}")
        return list(result)

    def save(self, data):
        """
        save data to json file
        :param data:
        :return:
        """
        with open(self.f_out_txt, 'w') as f:
            f.write(json.dumps(data, indent=4))

        print(f"save to: {self.f_out_txt}")


@click.command()
# @click.option("--gen_cmd", default="", help="Directory to read from")
def main():
    r = RssHubFeedsParser()
    r.parse_tg_channel()


if __name__ == '__main__':
    main()
