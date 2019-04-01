# Changelog


## Unreleased 

### Fixed 

- None border as 0px border

## 0.2.0 - 01.04.2019

### Added 

- Imports in `__init__.py`:

    ```pydocstring
    # render func
    >>> from jinja2xlsx import render
    >>> from jinja2xlsx import render_xlsx
    # style class
    >>> from jinja2xlsx import Style
    ```

- Merge multiple borders:
    
    ```pydocstring
    >>> wb = render_xlsx("""<table>
    ...     <tbody>
    ...     <tr>
    ...         <td style="border: 1px solid black; border-bottom: 0">Cell without bottom border</td>
    ...     </tr>
    ...     </tbody>
    ... </table>""")
    >>> wb.active.cell.border
    Border(left=Side("thin"), right=Side("thin"), top=Side("thin"), bottom=Side())
    ```

## 0.1.0 - 24.03.2019

### Added 

- jinja2xlsx.api.render: render xlsx from html