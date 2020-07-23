from dataclasses import dataclass
from typing import Sequence, Optional

from cached_property import cached_property
from requests_html import HTML, Element


@dataclass()
class Parser:
    html_str: str

    @cached_property
    def html(self) -> HTML:
        return HTML(html=self.html_str)

    @cached_property
    def table(self) -> Element:
        table = self.html.find("table", first=True)
        assert table
        return table

    @cached_property
    def table_head(self) -> Element:
        thead = self.table.find("thead", first=True)
        return thead

    @cached_property
    def table_body(self) -> Element:
        tbody = self.table.find("tbody", first=True)
        assert tbody
        return tbody

    @cached_property
    def rows(self) -> Sequence[Element]:
        return [
            *(self.table_head.find("tr") if self.table_head else []),
            *(self.table_body.find("tr")),
        ]

    @cached_property
    def colgroup(self) -> Optional[Element]:
        return self.table.find("colgroup", first=True)

    @cached_property
    def columns(self) -> Sequence[Element]:
        return self.colgroup.find("col") if self.colgroup else []
