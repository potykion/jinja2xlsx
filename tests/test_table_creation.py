from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Side, Font

from jinja2xlsx.api import render
from jinja2xlsx.testing_utils import read_from_test_dir, get_wb_values, get_test_file_path


def test_xlsx_table_creation_from_html_table() -> None:
    with read_from_test_dir("table.html") as f:
        html_table = f.read()

    wb = render(html_table)
    assert get_wb_values(wb) == [(1, 2), (3, 4)]


def test_xlsx_table_creation_from_html_table_with_merged_cells() -> None:
    with read_from_test_dir("table_with_merged_cells.html") as f:
        html_table = f.read()
        actual_wb = render(html_table)
        actual_wb_values = get_wb_values(actual_wb)

    expected_wb = load_workbook(get_test_file_path("table_with_merged_cells.html.xlsx"))
    expected_wb_values = get_wb_values(expected_wb)

    assert actual_wb_values == expected_wb_values


def test_xlsx_table_created_from_html_table_has_styles() -> None:
    with read_from_test_dir("table_with_inline_styles.html") as f:
        html_table = f.read()
        actual_wb = render(html_table)
        styled_cell = actual_wb.active.cell(1, 1)

    assert styled_cell.alignment == Alignment(horizontal="center")
    assert styled_cell.border == Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )
    assert styled_cell.font == Font(bold=True)


def test_xlsx_table_created_from_html_table_has_side_border() -> None:
    with read_from_test_dir("table_with_side_borders.html") as f:
        html_table = f.read()
        actual_wb = render(html_table)
        styled_cell = actual_wb.active.cell(1, 1)

    assert styled_cell.border == Border(bottom=Side("medium"))
