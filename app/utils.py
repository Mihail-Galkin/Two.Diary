import time
from datetime import date as d
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Optional

from babel.dates import format_datetime

from app import db
from app.models.sessions import Session
from app.models.users import User


def get_monday(date: d):
    monday = date - td(days=date.weekday())
    return monday


def str_to_date(str_date: str) -> d:
    return dt.strptime(str_date, "%d.%m.%Y").date()


def date_to_str(date: d) -> str:
    return date.strftime("%d.%m.%Y")


def get_readable_date(date: d) -> str:
    formatted_date = format_datetime(date, "EEEE, d MMMM", locale="ru").capitalize()
    return formatted_date


def get_user(sess_cookie: str) -> Optional[User]:
    db_sess = db.session
    q = db_sess.query(Session).filter(Session.value == sess_cookie)
    if q.count() == 0:
        return None
    return q.first().user
