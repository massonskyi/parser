import os
from abc import abstractmethod, ABC


def mkdir(directoryName: str = "template", directoryPath: str = "./") -> bool:
    if not directoryName or not directoryPath:
        return False
    os.makedirs(f"{directoryPath}/{directoryName}")
    return True


def isdir(directoryName: str = "template", directoryPath: str = "./") -> bool:
    if not directoryName or not directoryPath:
        return False
    return os.path.isdir(f"{directoryPath}/{directoryName}")


class BaseParser(ABC):
    """

    """

    @property
    @abstractmethod
    def url(self) -> str:
        """

        :return:
        """
        raise NotImplemented('This method not implemented')

    @url.setter
    @abstractmethod
    def url(self, url: str):
        """

        :param url:
        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def setupLogger(self) -> None:
        """

        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def __repr__(self) -> str:
        """

        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def getPageContent(self, url: str) -> object | None:
        """

        :param url:
        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def constructNewsSource(self, newsUrl: str) -> dict:
        """

        :param newsUrl:
        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def addNewsToList(self, newsBlock: object, newsList: list) -> bool:
        """

        :param newsBlock:
        :param newsList:
        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def parse(self) -> list:
        """

        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def createJson(self, *args) -> bool:
        """

        :return:
        """
        raise NotImplemented('This method not implemented')
