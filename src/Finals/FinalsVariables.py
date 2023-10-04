"""
https://lenta.ru/parts/news/
https://ria.ru/
https://www.rbc.ru/
https://tass.ru/
https://russian.rt.com/
https://iz.ru/
https://dzen.ru/
https://cyber.sports.ru/dota2/
https://readovka.space/
"""
from enum import Enum
from typing import Final


class STATUS(Enum):
    wait: int = 0
    successfully: int = 1
    endWithError: int = -1


LENTA_NEWS_PARSER_DICT = {
    'divTag': 'li',
    'divClass': 'parts-page__item',
    'titleTag': 'h3',
    'titleClass': 'card-full-news__title',
}
CYBERSPORT_NEWS_PARSER_DICT = {
    'divTag': 'div',
    'divClass': 'short-news',
    'titleTag': 'a',
    'titleClass': 'short-text',
}
CYBERSPORT_NEWS_GAME: Final = {
    hash('dota'): 'dota2',
    hash('cs'): 'cs',
    hash('lol'): 'lol',
    hash('valorant'): 'valorant',
    hash('pubg'): 'pubg',
    hash('cinema'): 'cinema',
    hash('streamers-twitch'): 'streamers-twitch',
    hash('games'): 'games',
    hash('all-news'): str(),
}
IntegerURLs: Final = {
    1: hash("lentaURL"),
    2: hash("cybersportURL"),
    3: hash("readovkaURL"),
}

URLS: Final = {
    hash("lentaURL"): "https://lenta.ru/parts/news/",
    hash("cybersportURL"): "https://cyber.sports.ru/",
    hash("readovkaURL"): "https://readovka.space/",
}
