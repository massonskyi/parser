import datetime
import json
import logging
from typing import Any

import requests
from bs4 import BeautifulSoup

from src.Base import BaseParser, mkdir, isdir


class CyberSportParser(BaseParser):
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

        # Handler to log to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Handler to log to file
        now = datetime.datetime.now()
        currentTime = now.strftime("%Y-%m-%d")
        fh = logging.FileHandler(filename=f'log/CyberSportParser/{self.__class__.__name__}_{currentTime}.log')
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
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            self.logger.error(e)
            return None

    def constructNewsSource(self, newsUrl: str) -> dict | None:
        soup: BeautifulSoup = self.getPageContent(newsUrl)
        self.logger.info(f"Starting parsing {newsUrl}")
        sourceBlock = soup.find('div', class_='content-wrapper')
        source = {}
        if title := sourceBlock.find('h1', class_='h1_size_tiny'):
            source['title'] = title.get_text()
        if tags := sourceBlock.find('div', class_='news-item__tags-line'):
            source['tags'] = \
                f'{[i["href"] for i in tags.find_all("a")]}\t' + f'{[i["title"] for i in tags.findAll("a")]}'
        if origin := sourceBlock.find('div', class_='news-item__footer-after-news'):
            source['origin'] = [i.get_text() for i in
                                origin.find_all('p')]
        if desc := sourceBlock.find("div", class_="news-item__content"):
            source['source'] = [i.get_text() for i in
                                desc.find_all('p')]
        return source

    def addNewsToList(self, newsBlock, newsList: list) -> bool:
        findArticle = newsBlock.find(self.titleTag, self.titleClass)
        if not findArticle:
            return False
        if not findArticle.find('strong'):
            newsTitle = findArticle.get_text()
        else:
            newsTitle = findArticle.find('strong').get_text()
        newsUrl = f"https://cyber.sports.ru{findArticle['href']}"
        source = self.constructNewsSource(newsUrl)
        newsList.append({"title": newsTitle, "url": newsUrl, "source": source,
                         "datetime": f"{newsBlock.find('b').text} {newsBlock.find('span').text}"})
        return True

    def parse(self):
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
        now = datetime.datetime.now()
        currentTime = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"json/{self.__class__.__name__}/{self.__class__.__name__}_{currentTime}.json"
        data = {"Parsing site": f"{self.url}", "news": args[0]}
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            self.logger.error(e)
            return False
