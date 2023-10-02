from abc import abstractmethod, ABC


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
    def __repr__(self) -> str:
        """

        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def get_page_content(self, url: str) -> object | None:
        """

        :param url:
        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def construct_news_source(self, news_url: str) -> dict:
        """

        :param news_url:
        :return:
        """
        raise NotImplemented('This method not implemented')

    @abstractmethod
    def add_news_to_list(self, news_block: object, news_list: list) -> bool:
        """

        :param news_block:
        :param news_list:
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
    def to_json(self, *args) -> bool:
        """

        :return:
        """
        raise NotImplemented('This method not implemented')
