"""
Реализует поддельный User-Agent

Функции:
    1. get_header - возвращает заголовок с поддельным User-Agent
"""
from fake_useragent import UserAgent

ua = UserAgent()


def get_header() -> dict:
    """
    Возвращает случайный заголовок с User-Agent
    """
    return {'User-Agent': str(ua.random)}
