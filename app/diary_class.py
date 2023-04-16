"""
Модуль, содержащий классы, реализующие электронный дневник:
    1. Subject - урок
    2. Day - учебный день
    3. Week - неделя
    4. Diary - дневник
"""
import copy
import typing
from dataclasses import dataclass, field
from datetime import date as d
from datetime import datetime as dt
from datetime import timedelta as td

import requests
from markupsafe import Markup

from app.parse import get_raw_diary, get_periods
from app.useragent import get_header
from app.utils import get_monday, get_readable_date, date_to_str, str_to_date


@dataclass
class Subject:
    """
    Класс хранит информацию о уроке

    previous_homework format:
        {"date": "...", "homework": "..."}
    """
    index: int
    name: str
    theme: str
    homework: str
    previous_homework: dict
    teacher: str
    marks: typing.List[int]
    time_end: str
    time_begin: str


@dataclass
class Day:
    """Класс хранит информацию о уроке"""
    subjects: typing.Dict[int, Subject]
    date: d
    formatted_date: str = field(init=False)
    str_date: str = field(init=False)

    def __post_init__(self):
        self.formatted_date = get_readable_date(self.date)
        self.str_date = date_to_str(self.date)


class Week:
    """
    Класс, хранящий информацию о неделе и позволяющий получать ее день
    """

    def __init__(self, date: d, days: list[Day] = None):
        """
        Инициализация класса Week.

        :param date: Дата понедельника
        :param days: Массив с днями недели
        :raise ValueError: Длина массива не равна 7
        """
        if not days:
            days = []
            for i in range(7):
                day_date = date + td(days=i)
                days.append(Day({}, day_date))
        elif len(days) != 7:
            raise ValueError("Длина массива не равна 7")

        self.days = days
        self.date = date  # дата понедельника

    def get_day(self, date: d) -> Day:
        """
        Возвращает день по дате

        :param date: Дата дня
        :return: Day
        :raise ValueError: Данный день не принадлежит неделе
        """
        monday = get_monday(date)
        if monday != self.date:
            raise ValueError("Данный день не принадлежит неделе")
        return self.days[date.weekday()]


class Diary:
    """
    Класс дневника кэширует все недели и при обращении к дню возвращает хранящийся класс, либо получает новый с сервера
    """
    def __init__(self, session_token: str, guid: str):
        """
        Инициализация дневника:
            1. Создание сессии 43edu RESTful
            2. Получение периодов
            3. Поиск текущего периода

        :param session_token: Сессионное куки
        :param guid: guid пользователя
        """
        self.guid = guid

        self.session_token = session_token
        cookies = {'X1_SSO': session_token}

        self.session = requests.Session()
        self.session.headers.update(get_header())
        self.session.get("https://one.43edu.ru/", cookies=cookies)

        self.weeks: typing.Dict[d, Week] = {}

        raw, self.session = get_raw_diary(self.session, self.guid, get_monday(d.today()))
        self.periods = get_periods(raw)
        self.quarters = get_periods(raw, is_quarters=True)

        self.current = self.quarters[0]
        for i in sorted(self.quarters, key=lambda x: str_to_date(x["dateBegin"])):
            if d.today() >= str_to_date(i["dateBegin"]):
                self.current = copy.deepcopy(i)

    def get_day(self, date: d) -> Day:
        """
        Возвращает день по дате

        :param date: Дата
        :return: Day
        """
        monday = get_monday(date)
        return self.get_week(monday).get_day(date)

    def get_week(self, week_date: d) -> typing.Optional[Week]:
        """
        Возвращает неделю по дате дня, принадлежащего ей

        :param week_date: Дата дня, принадлежащего неделе
        :return: Week
        """
        monday = get_monday(week_date)
        if monday in self.weeks:
            return self.weeks[monday]

        raw, self.session = get_raw_diary(self.session, self.guid, monday)
        if raw is None:
            return None

        raw_week = raw["data"]["diary"]
        week = Week(monday)
        no_value = Markup('<i>Не указано</i>')
        for raw_day in raw_week:
            subjects = {}
            for raw_subject in raw_week[raw_day]:
                if raw_subject["subject"].lower().startswith("комментарий"):
                    continue
                if raw_subject["periodMark"]:
                    continue
                subject = Subject(index=int(raw_subject["lessonNumber"]),
                                  name=raw_subject["subject"],
                                  theme=(raw_subject["topic"] or no_value),
                                  homework=(raw_subject["homework"] or no_value),
                                  previous_homework=(raw_subject["previousHomework"] or no_value),
                                  teacher=raw_subject["teacher"],
                                  marks=raw_subject["marksRaw"],
                                  time_begin=raw_subject["lessonTimeBegin"],
                                  time_end=raw_subject["lessonTimeEnd"])
                subjects[int(raw_subject["lessonNumber"])] = subject
            date = dt.strptime(raw_week[raw_day][0]["date"], "%d.%m.%Y").date()
            day = Day(subjects=subjects, date=date)
            week.days[date.weekday()] = day
        self.weeks[monday] = week
        return week
