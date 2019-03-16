from dataclasses import dataclass

from openpyxl.styles import Border, Font, Alignment


@dataclass()
class Style:
    border: Border
    alignment: Alignment
    font: Font
