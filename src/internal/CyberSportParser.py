import datetime
import json
import logging
from typing import Any

import requests
from bs4 import BeautifulSoup

from src.Base import BaseParser


class CyberSportParser(BaseParser):
    def __init__(self, url: str, **kwargs) -> None:
        self.logger = logging.getLogger(__name__)
        self.setup_logger()
        try:
            if type(url) is not str:
                raise TypeError("URL must be a string")
            self.__url: str = url
        except TypeError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error(e)
        if kwargs.get('div_tag'):
            self.div_tag: str = kwargs['div_tag']
        if kwargs.get('div_class'):
            self.div_class: str = kwargs['div_class']
        if kwargs.get('title_tag'):
            self.title_tag: str = kwargs['title_tag']
        if kwargs.get('title_class'):
            self.title_class: str = kwargs['title_class']
        if kwargs.get('date_tag'):
            self.date_tag: str = kwargs['date_tag']
        if kwargs.get('date_class'):
            self.date_class: str = kwargs['date_class']
        if kwargs.get('summary_tag'):
            self.summary_tag: str = kwargs['summary_tag']
        if kwargs.get('summary_class'):
            self.summary_class: str = kwargs['summary_class']

    def setup_logger(self) -> None:
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler to log to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Handler to log to file
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d")
        fh = logging.FileHandler(filename=f'log/CyberSportParser/{self.__class__.__name__}_{current_time}.log')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    @property
    def url(self) -> str:
        self.logger.info("Getting Url")
        return self.__url

    @url.setter
    def url(self, url: str):
        try:
            if type(url) is not str:
                raise TypeError("URL must be a string")
            self.logger.info(f"Changing url from {self.url} to {url}")
            self.__url: str = url
        except TypeError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error(e)

    def __repr__(self) -> str:
        information: str = f'parsing site: {self.url}\n'
        if hasattr(self, 'div_tag'):
            information += f'div tag: {self.div_tag}\n'
        if hasattr(self, 'div_class'):
            information += f'div class: {self.div_class}\n'
        if hasattr(self, 'title_tag'):
            information += f'title tag: {self.title_tag}\n'
        if hasattr(self, 'title_class'):
            information += f'title class: {self.title_class}\n'
        self.logger.info(f"Getting {information}")
        return information

    def get_page_content(self, url: str) -> BeautifulSoup | None:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            self.logger.error(e)
            return None

    def construct_news_source(self, news_url: str) -> dict | None:
        soup: BeautifulSoup = self.get_page_content(news_url)
        self.logger.info(f"Starting parsing {news_url}")
        source_block = soup.find('div', class_='content-wrapper')
        source = {}
        if title := source_block.find('h1', class_='h1_size_tiny'):
            source['title'] = title.get_text()
        if tags := source_block.find('div', class_='news-item__tags-line'):
            source['tags'] = \
                f'{[i["href"] for i in tags.find_all("a")]}\t' + f'{[i["title"] for i in tags.findAll("a")]}'
        if origin := source_block.find('div', class_='news-item__footer-after-news'):
            source['origin'] = [i.get_text() for i in
                                origin.find_all('p')]
        if desc := source_block.find("div", class_="news-item__content"):
            source['source'] = [i.get_text() for i in
                                desc.find_all('p')]
        return source

    def add_news_to_list(self, news_block, news_list: list) -> bool:
        find_a = news_block.find(self.title_tag, self.title_class)
        if not find_a:
            return False
        if not find_a.find('strong'):
            news_title = find_a.get_text()
        else:
            news_title = find_a.find('strong').get_text()
        news_url = f"https://cyber.sports.ru{find_a['href']}"
        source = self.construct_news_source(news_url)
        news_list.append({"title": news_title, "url": news_url, "source": source,
                          "datetime": f"{news_block.find('b').text} {news_block.find('span').text}"})
        return True

    def parse(self):
        self.logger.info(f"Starting parsing {self.url}")
        news_list: list = []
        soup: BeautifulSoup = self.get_page_content(self.url)
        news_blocks: Any = soup.find_all(self.div_tag, self.div_class)
        for news_block in news_blocks:
            if not self.add_news_to_list(news_block, news_list):
                break
        if news_list:
            res: bool | Exception = self.to_json(news_list)
            if not res:
                self.logger.info(f"Write file not complete {self.__class__.__name__}")
            else:
                self.logger.info(f"File {self.__class__.__name__} created")
        self.logger.info(f"Returned results")
        return news_list

    def to_json(self, *args) -> bool:
        """

        :param args:
        :return:
        """
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"json/{self.__class__.__name__}/{self.__class__.__name__}_{current_time}.json"
        data = {"Parsing site": f"{self.url}", "news": args[0]}
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            self.logger.error(e)
            return False
