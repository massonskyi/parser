import datetime
import json
import logging

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

    def setup_logger(self) -> None:
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler to log to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Handler to log to file
        fh = logging.FileHandler(filename='cyber_sport_parser.log')
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
        if "moslenta.ru" in news_url:
            source_block = soup.find('div', attrs={'data-qa': "lb-block"})
            source = {
                'title': source_block.find('h1', attrs={'data-qa': 'lb-topic-header-texts-title'}).get_text(),
                'sub_title': source_block.find('div', attrs={'data-qa': 'lb-topic-header-texts-lead'}).find(
                    'p').get_text(),
                'source': [i.get_text() for i in source_block.find('div', class_='text').findAll('p')]
            }
            return source
        elif "motor.ru" in news_url:
            source_block = soup.find('div', class_='content')
            source = {
                'title': source_block.find('h1', attrs={'data-qa': 'lb-topic-header-texts-title'}).get_text(),
                'sub_title': source_block.find('span', class_='subtitle').get_text(),
                'source': [i.get_text() for i in
                           source_block.find('div', attrs={'data-qa': 'lb-topic-header-texts-lead'}).findAll('p')]
            }
            return source
        else:  # Assuming this is for "https://lenta.ru"
            source_block = soup.find('div', class_='topic-body')
            source = {}
            if source_block.find('h1', class_='topic-body__titles'):
                source['title'] = source_block.find('h1', class_='topic-body__titles').get_text()
            if source_block.find('div', class_='topic-body__title-yandex'):
                source['sub_title'] = source_block.find('div', class_='topic-body__title-yandex').get_text()
            if source_block.find("div", class_="topic-body__content").find_all('p'):
                source['source'] = [i.get_text() for i in
                                    source_block.find("div", class_="topic-body__content").find_all('p')]
            return source

    def add_news_to_list(self, news_block, news_list: list) -> bool:
        find_h3 = news_block.find(self.title_tag, self.title_class)
        if not find_h3:
            return False
        news_title = find_h3.get_text()
        news_url = news_block.find('a')['href']
        if not news_url.startswith('http'):
            news_url = "https://lenta.ru" + news_url
        source = self.construct_news_source(news_url)
        news_list.append({"title": news_title, "url": news_url, "source": source})
        return True

    def parse(self):
        try:
            response = requests.get(self.url)
        except Exception as e:
            self.logger.error(f"Error while making a request to {self.url}: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        for article in soup.find_all('div', class_='short-news'):
            try:
                title = article.find('strong').text.strip()
                data = f"{article.find('b').text} {article.find('span').text}"
                description = article.find('strong').text.strip()
                url = article.find('a')['href']
                self.logger.info(f"data: {data}")
                self.logger.info(f"Title: {title}")
                self.logger.info(f"Description: {description}")
                self.logger.info(f"URL: {url}")
                self.logger.info("--------------------------")  # separator for easier reading of logs
            except AttributeError as e:
                self.logger.warning(f"Problem while parsing article: {e}")

    def to_json(self, *args) -> bool:
        """

        :param args:
        :return:
        """
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"json/{self.__class__.__name__}/{self.__class__.__name__}_{current_time}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(*args, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            self.logger.error(e)
            return False
