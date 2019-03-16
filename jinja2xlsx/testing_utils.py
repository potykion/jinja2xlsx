import os
from contextlib import contextmanager
from typing import List, Tuple, Iterator, TextIO

from openpyxl import Workbook

from jinja2xlsx.config import TEST_DATA_DIR


def get_test_file_path(file_: str) -> str:
    return os.path.join(TEST_DATA_DIR, file_)


@contextmanager
def read_from_test_dir(file_: str) -> Iterator[TextIO]:
    with open(get_test_file_path(file_)) as f:
        yield f


def get_wb_values(wb: Workbook) -> List[Tuple]:
    return list(wb.active.values)
