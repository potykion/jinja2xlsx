from typing import Union

from openpyxl import Workbook
from openpyxl.cell import MergedCell
from openpyxl.worksheet.worksheet import Worksheet
from requests_html import HTML, Element


def render(html_str: str) -> Workbook:
    html = HTML(html=html_str)

    table = html.find("table", first=True)

    # colgroup = table.find("colgroup", first=True)
    # assert colgroup, "No colgroup with col defined"
    # columns = colgroup.find("col")
    # assert columns, "No colgroup with col defined"

    wb = Workbook()
    ws: Worksheet = wb.active

    table_body = table.find("tbody", first=True)
    fill_sheet_with_table_data(ws, table_body)

    return wb


def fill_sheet_with_table_data(sheet: Worksheet, table: Element) -> None:
    row_index = 0
    col_index = 0

    for row in table.find("tr"):
        for cell in row.find("td"):
            target_cell = sheet.cell(row_index + 1, col_index + 1)
            while True:
                if isinstance(target_cell, MergedCell):
                    col_index += 1
                    target_cell = sheet.cell(row_index + 1, col_index + 1)
                else:
                    break

            target_cell.value = parse_cell_value(cell.text)

            colspan = int(cell.attrs.get("colspan", 1))
            rowspan = int(cell.attrs.get("rowspan", 1))

            if colspan > 1 or rowspan > 1:
                sheet.merge_cells(
                    start_row=row_index + 1,
                    start_column=col_index + 1,
                    end_row=row_index + rowspan,
                    end_column=col_index + colspan,
                )

            col_index += colspan

        row_index += 1
        col_index = 0


def parse_cell_value(cell_text: str) -> Union[int, float, str]:
    """
    >>> parse_cell_value("")
    ''
    >>> parse_cell_value("ass")
    'ass'
    >>> parse_cell_value("1")
    1
    >>> parse_cell_value("1.2")
    1.2
    """
    try:
        return int(cell_text)
    except ValueError:
        try:
            return float(cell_text)
        except ValueError:
            return cell_text
