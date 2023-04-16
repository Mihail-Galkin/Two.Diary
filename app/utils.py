"""
Содержит вспомогательные функции:
    1. get_monday - Возвращает дату понедельника недели, заданного дня
    2. str_to_date - Переводит дату строчного формата в datetime.datetime
    3. date_to_str - Переводит дату datetime.date в строчный формат
    4. get_readable_date - Переводит datetime.date в читаемый формат
    5. get_user - Возвращает пользователя по его session cookie
"""
from datetime import date as d
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Optional

from babel.dates import format_datetime

from app import db
from app.models.sessions import Session
from app.models.users import User


def get_monday(date: d) -> d:
    """
    Возвращает дату понедельника недели, заданного дня

    :param date: День, принадлежащий необходимой неделе
    :return: Дата понедельника
    """
    monday = date - td(days=date.weekday())
    return monday


def str_to_date(str_date: str) -> d:
    """
    Переводит дату строчного формата в datetime.datetime

    :param str_date: Дата - строка в формате *DD.MM.YYYY*
    :return: Дата datetime.date
    """
    return dt.strptime(str_date, "%d.%m.%Y").date()


def date_to_str(date: d) -> str:
    """
    Переводит дату datetime.date в строчный формат

    :param date: Дата datetime.date
    :return: Дата - строка в формате *DD.MM.YYYY*
    """
    return date.strftime("%d.%m.%Y")


def get_readable_date(date: d) -> str:
    """
    Переводит datetime.date в читаемый формат

    :param date: Дата datetime.date
    :return: Дата в формате *"Weekday, DD month"*
    """
    formatted_date = format_datetime(date, "EEEE, d MMMM", locale="ru").capitalize()
    return formatted_date


def get_user(sess_cookie: str) -> Optional[User]:
    """
    Возвращает пользователя по его session cookie

    :param sess_cookie: Сессионное куки
    :return: Пользователь или None, если не найдено
    """
    db_sess = db.session
    q = db_sess.query(Session).filter(Session.value == sess_cookie)
    if q.count() == 0:
        return None
    return q.first().user
