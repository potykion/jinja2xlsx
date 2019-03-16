from dataclasses import dataclass, field

from openpyxl.styles import Border, Font, Alignment


@dataclass()
class Style:
    border: Border = field(default_factory=Border)
    alignment: Alignment = field(default_factory=Alignment)
    font: Font = field(default_factory=Font)
