"""
Модуль, содержащий декораторы:
    1. only_ajax - допускает только запросы из javascript
    2. login_required - допускает к странице только авторизированных пользователей, добавляет в аргументы функции
    дневник
"""
import functools
from typing import Callable

import flask
from flask import request, abort, redirect

from app.diary_class import Diary
from app.exceptions import WrongPassword
from app.utils import get_user


def only_ajax() -> Callable:
    """
    Декоратор допускает только запросы с аргументом ajax == 1
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if int(request.args.get("ajax", "0")) != 1:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


diaries = {}


def login_required(recreate_diary: bool = False) -> Callable:
    """
    Декоратор получает информацию о пользователе при помощи сессионного куки. Если пользователь не авторизован,
    отправляет на страницу авторизации. Передает дневник в качестве дополнительного параметра

    :param recreate_diary: Нужно ли пересоздавать дневник (для обновления закэшированной информации)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sess_cookie = flask.session.get("session", "")
            user = get_user(sess_cookie)
            if user is None:
                return redirect("/login")
            if sess_cookie in diaries and not recreate_diary:
                diary = diaries[sess_cookie]
            else:
                participant = request.args.get("participant")
                # аргумент participant появляется только через js при нажатии кнопки смены ученика на сайте
                try:
                    diary = Diary(user, current_guid=participant)
                except WrongPassword:
                    return redirect("/login")
                diaries[sess_cookie] = diary
            return func(diary, *args, **kwargs)
        return wrapper
    return decorator
