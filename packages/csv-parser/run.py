import click
import pyexcel as pe


class CSVParser(object):
    """表格处理工具

    """

    def __init__(self, file_a: str, file_b: str):
        self.file_a = file_a or None
        self.file_b = file_b or None

        # sheet book:
        self.book_a = None
        self.book_b = None

    def read(self, file: str):
        if not file:
            return None

        # read file:
        book = pe.get_book(file_name=file)

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
        self.book_a = self.read(self.file_a)
        self.book_b = self.read(self.file_b)
        # self.parse_columns()

    def write(self, data):
        pass


@click.command()
@click.option("--file_a", default="input/1.xlsx", help="sheet filename")
@click.option("--file_b", default="input/2.xlsx", help="sheet filename")
def main(file_a: str, file_b: str):
    print(f"input args: {file_a}, {file_b}")
    r = CSVParser(file_a=file_a, file_b=file_b)
    r.handle()


if __name__ == '__main__':
    main()
