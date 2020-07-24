import base64
import io
import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import requests
from openpyxl.drawing.image import Image
from requests_html import Element

from jinja2xlsx.config import Config


@dataclass
class ImageParse:
    config: Config

    def __call__(self, image_tag: Element) -> Image:
        src = image_tag.attrs["src"]

        base64 = try_base64(src)
        if base64:
            image_stream: io.BytesIO = base64_to_stream(base64)
        elif is_url(src):
            image_stream = io.BytesIO(requests.get(src).content)
        elif self.config.base_url:
            src = urljoin(self.config.base_url, src)
            image_stream = io.BytesIO(requests.get(src).content)
        else:
            raise ValueError(f"No [Config.base_url] set, so cannot resolve image src: {src}")

        return Image(image_stream)


def is_url(src: str) -> bool:
    """
    >>> is_url("http://www.example.com/image.gif")
    True
    >>> is_url("data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA\\nAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO\\n9TXL0Y4OHwAAAABJRU5ErkJggg==")
    False
    >>> is_url("smiley.gif")
    False

    https://stackoverflow.com/a/7160778/5500609
    """

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE,
    )
    return re.match(regex, src) is not None


def try_base64(src: str) -> Optional[str]:
    """
    >>> try_base64("data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA\\nAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO\\n9TXL0Y4OHwAAAABJRU5ErkJggg==")
    'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    >>> try_base64("smiley.gif") is None
    True
    >>> try_base64("http://www.example.com/image.gif") is None
    True
    """
    try:
        base64_str = re.findall(r"data:.*?;base64,([\s\S]*)", src)[0]
        base64_str = base64_str.strip().replace("\n", "")
        return base64_str
    except IndexError:
        return None


def base64_to_stream(base64_str: str) -> io.BytesIO:
    return io.BytesIO(base64.b64decode(base64_str))
