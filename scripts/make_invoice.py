import os
import os.path
import subprocess
import sys
from datetime import datetime

import xlwings as xw
from dotenv import load_dotenv

load_dotenv()

ORIGINAL_FILE_PATH = "/bin/invoice_sample.xlsx"
OUTPUT_ABS_PATH = os.getenv("INVOICE_OUTPUT_PATH")
SHEET_INDEX = 0
WORK_HOUR_CELL = "P19"

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
example_file_path = parent_dir + ORIGINAL_FILE_PATH
working_hours = sys.argv[1]
file_name = f"請求書{datetime.now().month - 1}月分"


def get_xlsx_pdf_path(file_name):
    base = OUTPUT_ABS_PATH + "/" + file_name
    return f"{base}.xlsx", f"{base}.pdf"


def make_invoice():
    try:
        print("started loading")
        app = xw.App(visible=False)
        book = app.books.open(example_file_path)
        print("opened the file")

        book.sheets[SHEET_INDEX][WORK_HOUR_CELL].value = working_hours
        print("wrote working hours")

        xlsx_path, pdf_path = get_xlsx_pdf_path(file_name)

        book.save(path=xlsx_path)
        print('saved as ".xlsx"')

        book.to_pdf(path=pdf_path)
        print('saved as ".pdf"')
    except Exception as e:
        print(e)
    finally:
        book.close()
        app.kill()


def open_invoice_at_finder():
    subprocess.call(["open", OUTPUT_ABS_PATH])
    print("opened the directory")


def main():
    make_invoice()
    open_invoice_at_finder()
    print("successfully done")


if __name__ == "__main__":
    main()
