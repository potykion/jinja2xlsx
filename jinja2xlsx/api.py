from openpyxl import Workbook

from jinja2xlsx.config import Config
from jinja2xlsx.parse import Parser
from jinja2xlsx.render import Renderer
from jinja2xlsx.style import Style, Stylist


def render(html_str: str, default_style: Style = None, config: Config = None) -> Workbook:
    renderer = Renderer(Parser(html_str), Stylist(default_style or Style()), config or Config())
    return renderer()
