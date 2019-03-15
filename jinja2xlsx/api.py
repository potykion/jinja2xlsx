from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from requests_html import HTML


def render(html_str: str) -> Workbook:
    html = HTML(html=html_str)

    table = html.find("table", first=True)

    columns = table.find("colgroup", first=True).find("col")
    assert columns, "No colgroup with col defined"

    table_rows = table.find("tbody", first=True).find("tr")
    row_values = ([td.text for td in row.find("td")] for row in table_rows)

    wb = Workbook()
    ws: Worksheet = wb.active

    for row_index, row in enumerate(row_values):
        for col_index, col in enumerate(columns):
            ws.cell(row_index + 1, col_index + 1).value = row[col_index]

    return wb
