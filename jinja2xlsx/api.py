from typing import Optional

from openpyxl import Workbook

from jinja2xlsx.parse import Parser
from jinja2xlsx.render import Renderer
from jinja2xlsx.style import Style, Stylist


def render(html_str: str, default_style: Optional[Style] = None) -> Workbook:
    parser = Parser(html_str)
    stylist = Stylist(default_style or Style())
    renderer = Renderer(parser, stylist)
    return renderer()
