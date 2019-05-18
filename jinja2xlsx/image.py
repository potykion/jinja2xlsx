import base64
import io
import re

from openpyxl.drawing.image import Image
from requests_html import Element


def parse_img(image_tag: Element) -> Image:
    image_src = image_tag.attrs["src"]
    image_base64 = parse_src(image_src)
    image_stream = base64_to_stream(image_base64)
    return Image(image_stream)


def parse_src(src: str) -> str:
    """
    >>> parse_src("data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA\\nAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO\\n9TXL0Y4OHwAAAABJRU5ErkJggg==")
    'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    >>> parse_src("smiley.gif")
    Traceback (most recent call last):
        ...
    ValueError: Only base64 images supported.
    >>> parse_src("http://www.example.com/image.gif")
    Traceback (most recent call last):
        ...
    ValueError: Only base64 images supported.
    """
    try:
        base64_str = re.findall(r"data:.*?;base64,([\s\S]*)", src)[0]
    except IndexError:
        raise ValueError("Only base64 images supported.")

    base64_str = base64_str.strip().replace("\n", "")
    return base64_str


def base64_to_stream(base64_str: str) -> io.BytesIO:
    return io.BytesIO(base64.b64decode(base64_str))
