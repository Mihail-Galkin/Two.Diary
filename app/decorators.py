import functools
from typing import Callable

import flask
from flask import request, abort, redirect

from app.diary_class import Diary
from app.utils import get_user


def only_ajax() -> Callable:
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
                diary = Diary(user.source_session, user.guid)
                diaries[sess_cookie] = diary
            return func(diary, *args, **kwargs)

        return wrapper

    return decorator
