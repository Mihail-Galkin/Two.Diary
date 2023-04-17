"""
Содержит набор функций для получения информации с one.43edu.ru:
    1. auth - Авторизирует пользователя
    2. get_guid - Получает id пользователя
    3. get_raw_diary - Получает данные о неделе
    4. get_raw_marks - Получает данные о оценках
    5. get_latest_marks - Получает последние оценки текущей четверти с информацией о днях выставления
    6. get_session_cookie - Получает сессионный куки для быстрого восстановления сессии
    7. get_periods - Возвращает учебные периоды
"""
import csv
import logging
from datetime import date as d
from datetime import timedelta as td
from typing import Union, Tuple, Optional, Any

import pandas as pd
import requests
import xlrd
from bs4 import BeautifulSoup, SoupStrainer
from requests import Session

from app import db
from app.models.users import User
from app.useragent import get_header
from app.utils import date_to_str, str_to_date


def auth(login: str, password: str) -> Optional[requests.Session]:
    """
    Авторизирует пользователя

    :param login: Логин пользователя (почта или СНИЛС)
    :param password: Пароль пользователя
    :return: Сессия пользователя (requests.Session) или None если произошла ошибка
    """
    session = requests.Session()
    session.headers.update(get_header())

    url = 'https://passport.43edu.ru/auth/login'
    data = {'login': login, 'password': password, "submit": "submit", "returnTo": "https://one.43edu.ru"}
    session.post(url, data=data)

    if not get_session_cookie(session):
        return None
    return session


def get_guid(session: requests.Session) -> str:
    """
    Получает id пользователя

    :param session: Сессия пользователя
    :return: guid
    """
    response = session.get("https://one.43edu.ru/edv/index/participant")

    strainer = SoupStrainer("div", {"id": "participant"})
    soup = BeautifulSoup(response.text, 'lxml', parse_only=strainer)

    div = soup.select("div")
    guid = div[0].attrs["data-guid"]
    return guid


def get_raw_diary(session: requests.Session, guid: str, date: Union[str, d],
                  retry=True) -> Union[tuple[None, None], tuple[dict, Session]]:
    """
    Получает данные о неделе

    :param session: Сессия пользователя
    :param guid: Guid пользователя
    :param date: Дата для получения
    :param retry: Пытаться ли переподключиться в случае ошибки
    :return: Кортеж из json ответа от one.43edu.ru и сессии. В ответе содержатся дни от заданного до конца недели, а
         также данные об учебных периодах
    """
    if isinstance(date, d):
        date = date_to_str(date)

    url = "https://one.43edu.ru/edv/index/diary/" + guid
    data = {'date': date}
    response = session.get(url, params=data)
    json = response.json()
    if json["success"]:
        return json, session
    user = db.session.query(User).filter(User.guid == guid).first()
    if retry:
        sess = auth(user.email, user.get_password())
        if sess is None:
            db_sess = db.session
            for i in user.sessions:
                db_sess.delete(i)
            db_sess.delete(user)
            db_sess.commit()
            return None, None
        cookie = get_session_cookie(sess)
        user.source_session = cookie
        db.session.commit()

        raw_diary, _ = get_raw_diary(sess, guid, date, retry=False)
        return raw_diary, sess
    logging.error(f"Ошибка при получении данных. Сообщение: {json['message']}, guid: {guid}, "
                  f"session cookies: {session.cookies}")
    return None, None


def get_raw_marks(session: requests.Session, guid: str, begin: str = None, end: str = None,
                  final_grades: bool = False) -> list:
    """
    Получает данные об оценках. Необходимо указать период, либо final_grades=True.
    **Если оценки отсутствуют, будет записано "нет"**

    :param session: Сессия пользователя
    :param guid: Guid пользователя
    :param begin: Начала периода (строка в формате *DD.MM.YYYY*)
    :param end: Конец периода (строка в формате *DD.MM.YYYY*)
    :param final_grades: Итоговые оценки
    """
    if final_grades:
        url = "https://one.43edu.ru/edv/index/report/period/" + guid
        data = {"format": "xls"}
    else:
        url = "https://one.43edu.ru/edv/index/report/marks/" + guid
        data = {"begin": begin, "end": end, "format": "xls"}
    response = session.get(url, params=data)

    workbook = xlrd.open_workbook(file_contents=response.content, ignore_workbook_corruption=True)
    df = pd.read_excel(workbook)
    csv_data = df.to_csv(index=False)

    rows = csv.reader(csv_data.splitlines()[4:])

    return list(rows)


def get_latest_marks(diary, count: int) -> list:
    """
    Получает последние оценки текущей четверти с указанием даты и урока для каждой оценки.

    :param diary: Переменная дневника
    :param count: Количество оценок для полчуения
    :return: Оценки в формате [{"subject": "...", "mark": "...", "date": "...", lesson: ...}, ...]
    """
    date = d.today()
    marks = []
    quarters = diary.quarters
    quarter = None
    for i in quarters:
        if str_to_date(i["dateBegin"]) <= date <= str_to_date(i["dateEnd"]):
            quarter = (str_to_date(i["dateBegin"]), str_to_date(i["dateEnd"]))
            break
    if quarter is None:
        return []
    while count > 0 and quarter[0] <= date <= quarter[1]:
        day = diary.get_day(date)
        for i, subject in day.subjects.items():
            for mark in subject.marks:
                marks.append({"subject": subject.name, "mark": mark, "date": date_to_str(date), "lesson": i})
                count -= 1
                if count <= 0:
                    return marks
        date -= td(days=1)
    return marks


def get_session_cookie(session: requests.Session) -> Optional[str]:
    """
    Возвращает сессионное куки для быстрого восстановления сессии

    :param session: Сессия пользователя
    :return: Сессионный куки, либо None, если произошла ошибка
    """
    cookie = next((i for i in session.cookies if i.name == 'X1_SSO'), None)
    return cookie.value if cookie else None


def get_periods(json, is_quarters=False):
    """
    Возвращает учебные периоды.

    :param json: Ответ от сервера, возвращаемый get_raw_diary
    :param is_quarters: Возвращать все периоды или только четверти
    :return: Учебные периоды в формате [{'schoolEduPeriodGuid': '...', 'eduPeriodGuid': '...',
        'parentEduPeriodGuid': '...', 'name': '...', 'dateBegin': '...', 'dateEnd': '...'}, ...]
    """
    edu_periods = json["data"]["edu_periods"]
    if not is_quarters:
        return edu_periods
    quarters = []
    parent = None
    for i in edu_periods:
        if i["name"] == "По четвертям":
            parent = i["eduPeriodGuid"]
    for i in edu_periods:
        if i["parentEduPeriodGuid"] == parent:
            quarters.append(i)
    return quarters
