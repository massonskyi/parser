import datetime
import json
import logging
from typing import Any

import requests
from bs4 import BeautifulSoup
from requests import Response

from src.Base import BaseParser, mkdir, isdir


class LentaParser(BaseParser):
    """

    """

    def __init__(self, url: str, **kwargs) -> None:
        if not isdir(f"{self.__class__.__name__}", "./json/"):
            mkdir(f"{self.__class__.__name__}", "./json/")
        if not isdir(f"{self.__class__.__name__}", './log/'):
            mkdir(f"{self.__class__.__name__}", './log/')

        self.logger = logging.getLogger(__name__)
        self.setupLogger()
        try:
            if type(url) is not str:
                raise TypeError("URL must be a string")
            self.__url: str = url
        except TypeError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error(e)

        if kwargs.get('divTag'):
            self.divTag: str = kwargs['divTag']
        if kwargs.get('divClass'):
            self.divClass: str = kwargs['divClass']
        if kwargs.get('titleTag'):
            self.titleTag: str = kwargs['titleTag']
        if kwargs.get('titleClass'):
            self.titleClass: str = kwargs['titleClass']
        if kwargs.get('dateTag'):
            self.dateTag: str = kwargs['dateTag']
        if kwargs.get('dateClass'):
            self.dateClass: str = kwargs['dateClass']
        if kwargs.get('summaryTag'):
            self.summaryTag: str = kwargs['summaryTag']
        if kwargs.get('summaryClass'):
            self.summaryClass: str = kwargs['summaryClass']

    def setupLogger(self) -> None:
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Обработчик, который выводит сообщения в консоль
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Обработчик, который записывает сообщения в файл
        now = datetime.datetime.now()
        currentTime = now.strftime("%Y-%m-%d")
        fh = logging.FileHandler(filename=f'log/{self.__class__.__name__}/{self.__class__.__name__}_{currentTime}.log')
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
        if hasattr(self, 'divTag'):
            information += f'div tag: {self.divTag}\n'
        if hasattr(self, 'divClass'):
            information += f'div class: {self.divClass}\n'
        if hasattr(self, 'titleTag'):
            information += f'title tag: {self.titleTag}\n'
        if hasattr(self, 'titleClass'):
            information += f'title class: {self.titleClass}\n'
        self.logger.info(f"Getting {information}")
        return information

    def getPageContent(self, url: str) -> BeautifulSoup | None:
        try:
            response: Response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            self.logger.error(e)
            return None

    def constructNewsSource(self, newsUrl: str) -> dict | None:
        soup: BeautifulSoup = self.getPageContent(newsUrl)
        self.logger.info(f"Starting parsing {newsUrl}")
        if "moslenta.ru" in newsUrl:
            sourceBlock: Any = soup.find('div', attrs={'data-qa': "lb-block"})
            source: dict = {
                'title': sourceBlock.find('h1', attrs={'data-qa': 'lb-topic-header-texts-title'}).get_text(),
                'subTitle': sourceBlock.find('div', attrs={'data-qa': 'lb-topic-header-texts-lead'}).find(
                    'p').get_text(),
                'source': [i.get_text() for i in sourceBlock.find('div', class_='text').findAll('p')]
            }
            return source
        elif "motor.ru" in newsUrl:
            sourceBlock: Any = soup.find('div', class_='content')
            source: dict = {
                'title': sourceBlock.find('h1', attrs={'data-qa': 'lb-topic-header-texts-title'}).get_text(),
                'subTitle': sourceBlock.find('span', class_='subtitle').get_text(),
                'source': [i.get_text() for i in
                           sourceBlock.find('div', attrs={'data-qa': 'lb-topic-header-texts-lead'}).findAll('p')]
            }
            return source
        else:  # Assuming this is for "https://lenta.ru"
            sourceBlock: Any = soup.find('div', class_='topic-body')
            source: dict = {}
            if findTitle := sourceBlock.find('h1', class_='topic-body__titles'):
                source['title'] = findTitle.get_text()
            if findSubTitle := sourceBlock.find('div', class_='topic-body__title-yandex'):
                source['subTitle'] = findSubTitle.get_text()
            if findAllDesc := sourceBlock.find("div", class_="topic-body__content").find_all('p'):
                source['source'] = [i.get_text() for i in findAllDesc]
            return source

    def addNewsToList(self, newsBlock: Any, newsList: list) -> bool:
        findHeading: Any = newsBlock.find(self.titleTag, self.titleClass)
        if not findHeading:
            return False
        newsTitle: Any = findHeading.get_text()
        newsUrl: Any = newsBlock.find('a')['href']
        if not newsUrl.startswith('http'):
            newsUrl = "https://lenta.ru" + newsUrl
        source: dict = self.constructNewsSource(newsUrl)
        newsList.append({"title": newsTitle, "url": newsUrl, "source": source})
        return True

    def parse(self) -> list:
        self.logger.info(f"Starting parsing {self.url}")
        newsList: list = []
        soup: BeautifulSoup = self.getPageContent(self.url)
        newsBlocks: Any = soup.find_all(self.divTag, self.divClass)
        for newsBlock in newsBlocks:
            if not self.addNewsToList(newsBlock, newsList):
                break
        if newsList:
            res: bool = self.createJson(newsList)
            if not res:
                self.logger.info(f"Write file not complete {self.__class__.__name__}")
            else:
                self.logger.info(f"File {self.__class__.__name__} created")
        self.logger.info(f"Returned results")
        return newsList

    def createJson(self, *args) -> bool:
        """

        :param args:
        :return:
        """
        now: datetime = datetime.datetime.now()
        currentTime: str = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename: str = f"json/{self.__class__.__name__}/{self.__class__.__name__}_{currentTime}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(*args, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            self.logger.error(e)
            return False
