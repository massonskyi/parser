import logging
from datetime import datetime

from src.Base import mkdir, isdir
from src.Finals.FinalsVariables import URLS, IntegerURLs, \
    CYBERSPORT_NEWS_GAME, STATUS, CYBERSPORT_NEWS_PARSER_DICT, LENTA_NEWS_PARSER_DICT
from src.internal.CyberSportParser import CyberSportParser
from src.internal.LentaParser import LentaParser
from src.internal.ReadovkaParser import ReadovkaParser


def start() -> dict:
    showChoicesURLS()
    number: str = input("Enter the number of the desired URL ")
    try:
        urlNumber: int = int(number)
        url: str = choiceNewsUrl(urlNumber)
        Parser = choiceParser(urlNumber)
        if Parser is CyberSportParser:
            print("Filters:")
            for i, values in enumerate(CYBERSPORT_NEWS_GAME.values()):
                print(f"{i}.: {values}")
            url += f"{choiceCybersportNews(input('Enter search filter'))}/news/"
            logger.info(f"User choices: {urlNumber}: {url}, parser using:{Parser.__name__}")
            logger.info(f"Started parsing")
            parser = Parser(url, **CYBERSPORT_NEWS_PARSER_DICT)
            parser.parse()
        else:
            logger.info(f"User choices: {urlNumber}: {url}, parser using:{Parser.__name__}")
            logger.info(f"Started parsing")
            parser = Parser(url, **LENTA_NEWS_PARSER_DICT)
            parser.parse()
        return {
            "status": STATUS.successfully,
            "message": f"Application end with code:{STATUS.successfully}"
        }
    except Exception as e:
        logger.error(e)
        return {
            "status": STATUS.endWithError,
            "message": f"Application end with code:{STATUS.endWithError}\nError: {e}"
        }


def choiceCybersportNews(choice: str) -> str:
    res: str | None = CYBERSPORT_NEWS_GAME.get(hash(choice))
    if not res:
        return CYBERSPORT_NEWS_GAME.get(hash('all-news'))
    return res


def setupLogger(logger, __name__: str = "main") -> None:
    logger.setLevel(logging.INFO)
    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Обработчик, который выводит сообщения в консоль
    ch: logging.StreamHandler = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Обработчик, который записывает сообщения в файл
    now: datetime = datetime.now()
    currentTime: str = now.strftime("%Y-%m-%d")
    fh: logging.FileHandler = logging.FileHandler(filename=f'log/{__name__}_{currentTime}.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def choiceNewsUrl(choiceURL: int) -> str:
    if type(choiceURL) is not int:
        return "Enter the number of the desired URL "
    if not IntegerURLs.get(choiceURL):
        return "The list did not find a corresponding URL to your number"

    hashURL: str = IntegerURLs[choiceURL]
    if hashURL:
        if not URLS.get(hashURL):
            return "Failed to get URL, possible hash code error"
        return URLS.get(hashURL)


def choiceParser(choiceURL: int):
    if 0 <= choiceURL >= 4:
        return "Not corrected number Parser"
    if choiceURL == 1:
        return LentaParser
    if choiceURL == 2:
        return CyberSportParser
    if choiceURL == 3:
        return ReadovkaParser


def showChoicesURLS() -> None:
    print("URLs available for use:")
    for key, value in zip(IntegerURLs.keys(), URLS.values()):
        print(f"{key}.: {value}")


# TODO This is function will be created for optimization classes in the next time
"""
def parserParams(**kwargs) -> dict:
    options: dict = {}
    if not kwargs.get('url'):
        return {
            "status": "Error",
            "msg": "Cannot create options without main URL parameter"
        }
    else:
        options['url'] = kwargs['url']

    if kwargs.get('divTag'):
        options['divTag'] = kwargs['divTag']
    if kwargs.get('divClass'):
        options['divClass'] = kwargs['divClass']
    if kwargs.get('titleTag'):
        options['titleTag'] = kwargs['titleTag']
    if kwargs.get('titleClass'):
        options['titleClass'] = kwargs['titleClass']
    if kwargs.get('sourceBlock'):
        options['sourceBlockDivTag'] = kwargs['sourceBlock']['divTag']
        options['sourceBlockAttrs'] = kwargs['sourceBlock']['attrs']
    if kwargs.get('subTitle'):
        options['subTitle'] = kwargs['subTitle']
    if kwargs.get('tags'):
        options['tags'] = kwargs['tags']
"""

if __name__ == '__main__':
    if not isdir("log"):
        mkdir("log")
    if not isdir("json"):
        mkdir("json")
    logger = logging.getLogger(__name__)
    setupLogger(logger, __name__)
    logger.info("Starting application")
    start()
