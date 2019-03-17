from dataclasses import dataclass, field

from openpyxl.styles import Border, Font, Alignment, Side

from jinja2xlsx.utils import union_dicts


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
