import dataclasses
import re
from dataclasses import dataclass, field
from typing import Optional, Dict

from openpyxl.cell import Cell
from openpyxl.styles import Border, Side, Alignment, Font
from requests_html import Element

from jinja2xlsx.utils import union_dicts, CellRange

REMOVE_SIDE = Side()


@dataclass()
class Style:
    border: Border = field(default_factory=Border)
    alignment: Alignment = field(default_factory=Alignment)
    font: Font = field(default_factory=Font)

    def union(self, style: 'Style') -> 'Style':
        """
        >>> from openpyxl.styles import Side
        >>> default_style = Style(alignment=Alignment(wrap_text=True), font=Font("Times New Roman", 10))
        >>> style = Style(border=Border(left=Side("medium")), font=Font(sz=11, bold=True))
        >>> new_style = default_style.union(style)
        >>> new_style.border.left.style
        'medium'
        >>> new_style.alignment.wrap_text
        True
        >>> new_style.font == Font("Times New Roman", 11, bold=True)
        True
        """
        border_data = union_dicts(vars(self.border), vars(style.border))
        alignment_data = union_dicts(vars(self.alignment), vars(style.alignment))
        font_data = union_dicts(vars(self.font), vars(style.font))

        return Style(Border(**border_data), Alignment(**alignment_data), Font(**font_data))


def extract_style(style_attr: str) -> Style:
    """
    >>> style = extract_style("border: 1px solid black; text-align: center; font-weight: bold")
    >>> style.alignment.horizontal
    'center'
    >>> style.border.left.style
    'thin'
    >>> style.border.left.style == style.border.right.style == style.border.top.style == style.border.bottom.style
    True
    >>> style.font.bold
    True
    """
    if not style_attr:
        return Style()

    style_dict = parse_style_attr(style_attr)

    border = _build_border(style_dict)
    alignment = _build_alignment(style_dict)
    font = _build_font(style_dict)

    return Style(border, alignment, font)


@dataclass()
class Stylist:
    default_style: 'Style' = field(default_factory=Style)

    def build_style_from_html(self, html_element: Element) -> Style:
        style_attr = html_element.attrs.get("style")
        style = extract_style(style_attr)
        style.font.bold = style.font.bold or html_element.tag == "th"
        style = self.default_style.union(style)
        return style

    def style_single_cell(self, cell: Cell, style: Style) -> None:
        cell.border = style.border
        cell.alignment = style.alignment
        cell.font = style.font

    def style_merged_cells(self, cell_range: CellRange, style: Style) -> None:
        """
        Source:
        https://openpyxl.readthedocs.io/en/2.5/styles.html#styling-merged-cells
        """
        first_cell = cell_range[0][0]
        first_cell.alignment = style.alignment
        first_cell.font = style.font

        top = Border(top=style.border.top)
        left = Border(left=style.border.left)
        right = Border(right=style.border.right)
        bottom = Border(bottom=style.border.bottom)

        for cell in cell_range[0]:
            cell.border = cell.border + top
        for cell in cell_range[-1]:
            cell.border = cell.border + bottom

        for row in cell_range:
            left_cell = row[0]
            right_cell = row[-1]
            left_cell.border = left_cell.border + left
            right_cell.border = right_cell.border + right


def parse_style_attr(style_str: Optional[str]) -> Dict:
    """
    >>> parse_style_attr("border: 1px solid black; text-align: center; font-weight: bold")
    {'border': '1px solid black', 'text-align': 'center', 'font-weight': 'bold'}
    >>> parse_style_attr("")
    {}
    >>> parse_style_attr(None)
    {}
    """
    if not style_str:
        return {}

    return {
        style.strip(): value.strip()
        for style, value in (style.split(":") for style in filter(None, style_str.split(";")))
    }


@dataclasses.dataclass
class ParseBorder:
    style_dict: Dict[str, str]

    def __call__(self) -> Border:
        final_border = Border()

        border_style_attrs = [
            'border',
            'border-left',
            'border-right',
            'border-top',
            'border-bottom',
        ]
        border_style_attrs = [attr for attr in border_style_attrs if attr in self.style_dict]

        for attr in border_style_attrs:
            if attr == 'border':
                final_border.left = self._parse_b_value(self.style_dict[attr])
                final_border.right = self._parse_b_value(self.style_dict[attr])
                final_border.top = self._parse_b_value(self.style_dict[attr])
                final_border.bottom = self._parse_b_value(self.style_dict[attr])
            else:
                side = attr.split('-')[1]
                setattr(final_border, side, self._parse_b_value(self.style_dict[attr]))

        return final_border

    def _parse_b_value(self, b_value: str) -> Side:
        if b_value == '1px solid black':
            return Side('thin')
        if re.match(r'\d+px solid black', b_value):
            return Side('medium')
        if b_value == '0' or b_value == 'none':
            return Side()


def _build_border(style_dict: Dict[str, str]) -> Border:
    """
    >>> border = _build_border({"border": "1px solid black"})
    >>> border.left.style
    'thin'
    >>> border.left.style == border.right.style == border.top.style == border.bottom.style
    True
    >>> border = _build_border({"border-right": "2px solid black"})
    >>> border.right.style
    'medium'
    >>> border = _build_border({"border": "1px solid black", "border-bottom": "0"})
    >>> border.left == border.right == border.top == Side("thin")
    True
    >>> border.bottom == Side()
    True
    >>> border = _build_border({"border": "1px solid black", "border-top": "none"})
    >>> border.left == border.right == border.bottom == Side("thin")
    True
    >>> border.top == Side()
    True
    """
    return ParseBorder(style_dict)()


def _build_alignment(style_dict: Dict) -> Alignment:
    word_wrap = style_dict.get("word-wrap")

    wrap_text: Optional[bool]
    if word_wrap == "break-word":
        wrap_text = True
    elif word_wrap == "normal":
        wrap_text = False
    else:
        wrap_text = None

    alignment = Alignment(horizontal=style_dict.get("text-align"), wrap_text=wrap_text)
    return alignment


def _build_font(style_dict: Dict) -> Font:
    font = Font(bold=style_dict.get("font-weight") == "bold")
    return font
