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
        # the default iterator for a **Book* instance is a SheetIterator
        for sheet in book:
            # Each sheet has name
            print("sheet name: %s" % sheet.name)

            limit = 5
            i = 0
            for row in sheet:
                if i == limit:
                    break
                print(f"\t{row}")
                i += 1

        return book

    def handle(self, ):
        self.book_a = self.read(self.file_a)
        self.book_b = self.read(self.file_b)

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
