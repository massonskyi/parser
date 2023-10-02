from pprint import pprint

from src.internal.LentaParser import LentaParser
from src.internal.CyberSportParser import CyberSportParser

"""
https://lenta.ru/parts/news/
https://ria.ru/
https://www.rbc.ru/
https://tass.ru/
https://russian.rt.com/
https://iz.ru/
https://dzen.ru/
https://cyber.sports.ru/dota2/

"""
LENTA_NEWS_PARSER_DICT = {
    'div_tag': 'li',
    'div_class': 'parts-page__item',
    'title_tag': 'h3',
    'title_class': 'card-full-news__title'
}
CYBERSPORT_NEWS_PARSER_DICT = {
    'div_tag': 'div',
    'div_class': 'short-news',
    'title_tag': 'div',
    'title_class': 'short-news'
}
if __name__ == '__main__':
    parser = CyberSportParser('https://cyber.sports.ru/dota2/news/top/')
    parser.parse()
