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
    'title_tag': 'a',
    'title_class': 'short-text'
}
CYBERSPORT_NEWS_GAME = {
    hash('dota'): 'dota2',
    hash('cs'): 'cs',
    hash('lol'): 'lol',
    hash('valorant'): 'valorant',
    hash('pubg'): 'pubg',
    hash('cinema'): 'cinema',
    hash('streamers-twitch'): 'streamers-twitch',
    hash('games'): 'games',
    hash('all-news'): str()
}


def choice_cybersport_news(choice: str) -> str:
    res: str | None = CYBERSPORT_NEWS_GAME.get(hash(choice))
    if not res:
        return CYBERSPORT_NEWS_GAME.get(hash('all-news'))
    return res


if __name__ == '__main__':
    parser = CyberSportParser(
        f'https://cyber.sports.ru/{choice_cybersport_news(input("enter game news: "))}/news/top/',
        **CYBERSPORT_NEWS_PARSER_DICT
    )
    parser.parse()
