import datetime
import json
import logging
from typing import Any

import requests
from bs4 import BeautifulSoup
from requests import Response

from src.Base import BaseParser, mkdir, isdir



class ReadovkaParser(BaseParser):
    """

    """

    def __init__(self, url: str):
        ...