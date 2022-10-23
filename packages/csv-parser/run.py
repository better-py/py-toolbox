import click
import pyexcel as pe
import pandas as pd


class CSVParser(object):
    """表格处理工具

    """

    def __init__(self, file_a: str, file_b: str):
        self.file_a = file_a or None
        self.file_b = file_b or None

        # sheet book:
        self.df_a = None
        self.df_b = None

        # data frame:
        self.df_a = None
        self.df_b = None

        # 目标列：
        self.pick_cols_a = None

        # task functions:
        self.tasks = []

    @staticmethod
    def pd_read(filename: str):
        if not filename:
            return None
        book = pd.read_excel(filename)

        print(f"file <{filename}>:\n{book}")
        print(f"columns:\n\t{book.columns}")
        print(f"index:\n\t{book.index}")

        return book

    def read(self, filename: str):
        if not filename:
            return None

        # read file:
        book = pe.get_book(file_name=filename)

        # print limit of sheets
        self.print_rows(book)
        self.print_cols(book)

        return book

    @staticmethod
    def print_rows(book):
        if not book:
            return None

        # print:
        for sheet in book:
            print(f"\nsheet <{sheet.name}> rows:")

            i, limit = 0, 5
            for row in sheet.rows():
                if i == limit:
                    break
                print(f"\trow: {row}")
                i += 1

    @staticmethod
    def print_cols(book):
        if not book:
            return None

        # print:
        for sheet in book:
            print(f"\nsheet <{sheet.name}> columns:")

            for col in sheet.columns():
                print(f"\tcol : {col[:8]}")

    def handle(self, ):
        # self.book_a = self.read(self.file_a)
        # self.book_b = self.read(self.file_b)

        self.df_a = self.pd_read(self.file_a)
        self.df_b = self.pd_read(self.file_b)

        result = self.df_b[self.df_b['住院号'] == 'H80008']
        print(f"{result}")

        self.add_task(self.task_calc_avg)
        self.do_task()

    def add_task(self, task_fn):
        if task_fn:
            self.tasks.append(task_fn)

    def do_task(self):
        for task_fn in self.tasks:
            task_fn()

    def task_calc_avg(self):
        """计算指定行的平均值

        :return:
        """

        # 去重复：
        unique_hospital_ids = set(self.df_b['住院号'])

        # 筛选单个病人的就诊记录：
        for uid in unique_hospital_ids:
            data = self.df_b[self.df_b['住院号'] == uid]

            # 计算平均值， 保留2位小数
            avg = data.mean(numeric_only=True).round(2)
            print(f"{data}")
            print(f"avg:{avg}\n")


@click.command()
@click.option("--file_a", default="input/1.xlsx", help="sheet filename")
@click.option("--file_b", default="input/2.xlsx", help="sheet filename")
def main(file_a: str, file_b: str):
    print(f"input args: {file_a}, {file_b}")
    r = CSVParser(file_a=file_a, file_b=file_b)
    r.handle()


if __name__ == '__main__':
    main()
