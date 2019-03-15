import os
from contextlib import contextmanager
from typing import IO, List, Tuple, Iterable, Iterator, TextIO

import pytest
from openpyxl import load_workbook, Workbook

from jinja2xlsx.api import render
from jinja2xlsx.config import TEST_DATA_DIR


def get_test_file_path(file_: str) -> str:
    return os.path.join(TEST_DATA_DIR, file_)


@contextmanager
def read_from_test_dir(file_: str) -> Iterator[TextIO]:
    with open(get_test_file_path(file_)) as f:
        yield f


def get_wb_values(wb: Workbook) -> List[Tuple]:
    return list(wb.active.values)


def test_xlsx_table_creation_from_html_table() -> None:
    with read_from_test_dir("table.html") as f:
        html_table = f.read()

    wb = render(html_table)
    assert get_wb_values(wb) == [("1", "2"), ("3", "4")]


@pytest.mark.skip("WIP")
def test_xlsx_table_creation_from_html_table_with_merged_cells() -> None:
    with read_from_test_dir("table_with_merged_cells.html") as f:
        html_table = f.read()
        actual_wb = render(html_table)
        actual_wb_values = get_wb_values(actual_wb)

    expected_wb = load_workbook(get_test_file_path("table_with_merged_cells.html.xlsx"))
    expected_wb_values = get_wb_values(expected_wb)

    assert actual_wb_values == expected_wb_values
