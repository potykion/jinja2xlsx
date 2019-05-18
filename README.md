# jinja2xlsx

Create xlsx-tables from html-tables

## Example

Given html table str

When render html to xlsx

Then result xlsx has table values

```python
from jinja2xlsx import render_xlsx
from openpyxl import Workbook

html_str = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Simple table</title>
    </head>
    <body>
        <table>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>4</td>
                </tr>
            </tbody>
        </table>
    </body>
</html>"""

workbook: Workbook = render_xlsx(html_str)
assert tuple(workbook.active.values) == ((1, 2), (3, 4))
```

## Installation 

```
pip install jinja2xlsx
```

## Development

Install dependencies:

```
poetry install
```

Run tests and linting:

```
pre-commit run -a
```

Install pre-commit hooks:

```
pre-commit install
```

## Extra

### Publish to PyPI

```shell
poetry publish --build
```