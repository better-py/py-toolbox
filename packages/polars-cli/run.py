import click
import pyexcel as pe
import pandas as pd
import polars as pl


class CSVParser(object):
    """表格处理工具

    """

    def __init__(self, infile_a: str, infile_b: str, outfile: str):
        self.infile_a = infile_a or None
        self.infile_b = infile_b or None
        self.outfile = outfile or None

        # sheet book:
        self.book_a = None
        self.book_b = None

        # data frame:
        self.df_a = None
        self.df_b = None

        # 目标列：
        self.pick_col_name = '住院号'

    @staticmethod
    def pd_read(filename: str):
        if not filename:
            return None
        book = pd.read_excel(filename)

        print(f"file <{filename}>:\n{book}")
        print(f"columns:\n\t{book.columns}")
        print(f"index:\n\t{book.index}")

        return book

    @staticmethod
    def pl_read(filename: str):
        if not filename:
            return None

        # 自定义表列数据类型：
        dtypes = {
            "SpO2": pl.Float64,
            "心率": pl.Float64,
            "PULSE": pl.Float64,
            "动脉收缩压": pl.Float64,
            "动脉舒张压": pl.Float64,
            "动脉平均压": pl.Float64,
            "肺动脉收缩压": pl.Float64,
            "肺动脉舒张压": pl.Float64,
            "肺动脉平均压": pl.Float64,
            "收缩压": pl.Float64,
            "舒张压": pl.Float64,
            "平均压": pl.Float64,
            "体温": pl.Float64,
            "ETCO2": pl.Float64,
            "呼吸": pl.Float64,
            "CVP": pl.Float64,

        }

        book = pl.read_excel(
            filename,
            read_csv_options={
                'dtypes': dtypes,
            }
        )

        print(f"file <{filename}>:\n{book}")
        print(f"columns:\n\t{book.columns}")
        return book

    def read(self, filename: str):
        """excel 读取（弃用）

        :param filename:
        :return:
        """
        if not filename:
            return None

        # read file:
        book = pe.get_book(file_name=filename)

        # print limit of sheets
        self.print_rows(book)
        # self.print_cols(book)

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
        # self.df_a = self.pd_read(self.infile_a)
        # self.df_b = self.pd_read(self.infile_b)

        self.df_a = self.pl_read(self.infile_a)
        self.df_b = self.pl_read(self.infile_b)
        #
        # 处理具体功能：
        #
        self.do_task()

    def do_task(self):
        self.task_calc_avg()
        self.task_calc_num()

    def task_calc_avg(self):
        # 根据住院号，筛选同一个病人记录， 批量计算平均值， 并写入文件
        data = self.df_b.groupby(self.pick_col_name).mean()

        # data.to_excel(self.outfile, sheet_name='avg')
        print(f"group calc: \n{data}")

    def task_calc_num(self):
        """计算指定行的平均值

        :return:
        """

        # 去重复：
        unique_hospital_ids = set(self.df_b[self.pick_col_name])

        print(f"number of unique_hospital_ids: {len(unique_hospital_ids)}")

        # # 筛选单个病人的就诊记录：
        # for uid in unique_hospital_ids:
        #     data = self.df_b[self.df_b['住院号'] == uid]
        #     # 计算平均值， 保留2位小数
        #     avg = data.mean(numeric_only=True).round(2)
        #     pd.melt(avg).to_excel(self.outfile, sheet_name='avg')
        #
        #     print(f"{data}")
        #     print(f"avg:{pd.melt(avg)}\n")


@click.command()
@click.option("--infile_a", default="input/1.xlsx", help="sheet input filename")
@click.option("--infile_b", default="input/2.xlsx", help="sheet input filename")
@click.option("--outfile", default="output/out.xlsx", help="sheet output filename")
def main(infile_a: str, infile_b: str, outfile: str):
    print(f"input args: {infile_a}, {infile_b}, {outfile}")
    r = CSVParser(infile_a=infile_a, infile_b=infile_b, outfile=outfile)
    r.handle()


if __name__ == '__main__':
    main()
