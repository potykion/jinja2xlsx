from dataclasses import dataclass
from typing import Sequence, Optional

from requests_html import HTML, Element


@dataclass()
class Parser:
    html_str: str

    @property
    def html(self) -> HTML:
        return HTML(html=self.html_str)

    @property
    def table(self) -> Element:
        table = self.html.find("table", first=True)
        assert table
        return table

    @property
    def table_body(self) -> Element:
        tbody = self.table.find("tbody", first=True)
        assert tbody
        return tbody

    @property
    def rows(self) -> Sequence[Element]:
        return self.table_body.find("tr")

    @property
    def colgroup(self) -> Optional[Element]:
        return self.table.find("colgroup", first=True)

    @property
    def columns(self) -> Sequence[Element]:
        colgroup = self.colgroup
        if colgroup:
            return colgroup.find("col")
        else:
            return []
