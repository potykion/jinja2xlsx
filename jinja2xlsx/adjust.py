from dataclasses import dataclass
from typing import Iterable

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.worksheet.worksheet import Worksheet
from requests_html import Element

from jinja2xlsx.style import parse_style_attr
from jinja2xlsx.utils import (
    try_extract_pixels,
    width_pixels_to_xlsx_units,
    height_pixels_to_xlsx_units,
)


@dataclass
class Adjuster:
    sheet: Worksheet

    def adjust_columns(self, columns: Iterable[Element]) -> None:
        for index, column in enumerate(columns):
            col_width_in_pixels = int(column.attrs.get("width", 0))
            if not col_width_in_pixels:
                continue

            column_dimension: ColumnDimension = self.sheet.column_dimensions[
                get_column_letter(index + 1)
            ]
            column_dimension.width = width_pixels_to_xlsx_units(col_width_in_pixels)

    def adjust_rows(self, rows: Iterable[Element]) -> None:
        for index, row in enumerate(rows):
            # todo there must be a better way
            style_dict = parse_style_attr(row.attrs.get("style"))
            height_str = style_dict.get("line-height") or style_dict.get("height") or ""
            row_height = try_extract_pixels(height_str)
            if not row_height:
                continue

            self.sheet.row_dimensions[index + 1].height = height_pixels_to_xlsx_units(row_height)
