from datetime import date as d
from datetime import timedelta as td

from flask import render_template, request

from app.decorators import only_ajax, login_required
from app.home import bp
from app.parse import get_latest_marks
from app.utils import str_to_date


@bp.route('/home')
@only_ajax()
@login_required()
def home(diary):
    latest_marks = get_latest_marks(diary, 5)
    return render_template("home.html", latest_marks=latest_marks)


@bp.route("/one-day")
@only_ajax()
@login_required()
def one_day(diary):
    date = request.args.get("date", "today")
    if date == "today":
        date = d.today()
    else:
        date = str_to_date(date)
    date += td(days=int(request.args.get("delta", 0)))
    return render_template("parts/one-day.html", day=diary.get_day(date))
