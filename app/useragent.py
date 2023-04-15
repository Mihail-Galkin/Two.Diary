"""
Реализует поддельный User-Agent

Функции:
    get_header          Возвращает заголовок с поддельным User-Agent
"""
from fake_useragent import UserAgent

ua = UserAgent()


def get_header() -> dict:
    """
    Возвращает случайный заголовок с User-Agent
    """
    return {'User-Agent': str(ua.random)}
