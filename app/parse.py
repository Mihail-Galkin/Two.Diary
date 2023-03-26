import csv
import logging
import os
from datetime import date as d
from datetime import timedelta as td
from typing import Union, Tuple, Optional

import certifi
import pandas as pd
import requests
import xlrd
from bs4 import BeautifulSoup, SoupStrainer

from app import db
from app.models.users import User
from app.useragent import get_header
from app.utils import date_to_str, str_to_date


def auth(login: str, password: str) -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.headers.update(get_header())

    url = 'https://httpbin.org/anything'
    data = {'login': login, 'password': password, "submit": "submit", "returnTo": "https://one.43edu.ru"}
    r = session.post(url, data=data, verify=False)
    print(r.json())


    return session


def get_guid(session: requests.Session) -> str:
    response = session.get("https://one.43edu.ru/edv/index/participant", verify=False)

    strainer = SoupStrainer("div", {"id": "participant"})
    soup = BeautifulSoup(response.text, 'lxml', parse_only=strainer)

    div = soup.select("div")
    guid = div[0].attrs["data-guid"]
    return guid


def get_raw_diary(session: requests.Session, guid: str, date: Union[str, d], retry=True) -> Optional[Tuple[dict, requests.Session]]:
    if isinstance(date, d):
        date = date_to_str(date)

    url = "https://one.43edu.ru/edv/index/diary/" + guid
    data = {'date': date}
    response = session.get(url, params=data, verify=False)
    json = response.json()
    if json["success"]:
        return json, session
    user = db.session.query(User).filter(User.guid == guid).first()
    if retry:
        sess = auth(user.email, user.get_password())
        cookie = get_session_cookie(sess)
        user.source_session = cookie
        db.session.commit()

        raw_diary, _ = get_raw_diary(sess, guid, date, retry=False)
        return raw_diary, sess
    logging.error(f"Ошибка при получении данных. Сообщение: {json['message']}, guid: {guid}, "
                  f"session cookies: {session.cookies}")
    return None


def get_raw_marks(session: requests.Session, guid: str, begin: str = None, end: str = None, final_grades: bool = False):
    """
    про нет в строке
    """
    if final_grades:
        url = "https://one.43edu.ru/edv/index/report/period/" + guid
        data = {}
    else:
        url = "https://one.43edu.ru/edv/index/report/marks/" + guid
        data = {"begin": begin, "end": end}
    response = session.get(url, params=data, verify=False)

    workbook = xlrd.open_workbook(file_contents=response.content, ignore_workbook_corruption=True)
    df = pd.read_excel(workbook)
    csv_data = df.to_csv(index=False)

    rows = csv.reader(csv_data.splitlines()[4:])

    return list(rows)


def get_latest_marks(diary, count: int):
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


def get_session_cookie(session: requests.Session):
    cookie = next(i for i in session.cookies if i.name == 'X1_SSO')
    return cookie.value


def get_periods(json, is_quarters=False):
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


if __name__ == "__main__":
    s = auth("galkin.mihail.11.06@yandex.ru", "***REMOVED***")

    date = d.today()
    date -= td(days=date.weekday())