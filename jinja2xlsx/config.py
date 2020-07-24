import os
from dataclasses import dataclass
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(BASE_DIR, "test_data")


@dataclass
class Config:
    # if td contains img tag => get base64 src from img and insert to xlsx
    parse_img: bool = False
    # get url src from img, download it via requests and insert to xlsx
    parse_img_url: bool = False
    # required for relative image url like /img/cat.jpg
    base_url: Optional[str] = None
