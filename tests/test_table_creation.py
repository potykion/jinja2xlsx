import os

from jinja2xlsx.api import render
from jinja2xlsx.config import TEST_DATA_DIR


def test_xlsx_table_creation_from_html_table() -> None:
    with open(os.path.join(TEST_DATA_DIR, "table.html")) as f:
        html_table = f.read()

    wb = render(html_table)
    assert list(wb.active.values) == [
        ("1", "2"),
        ("3", "4")
    ]
