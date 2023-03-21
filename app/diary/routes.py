from datetime import date as d
from datetime import timedelta as td

from flask import request, render_template

from app.decorators import only_ajax, login_required
from app.diary import bp
from app.utils import date_to_str, str_to_date


@bp.route('/diary')
@only_ajax()
@login_required()
def diary_(diary):
    str_date = request.args.get("date", "today")
    if str_date == "today":
        str_date = date_to_str(d.today())
    date = str_to_date(str_date) + td(days=int(request.args.get("delta", 0)))
    return render_template("diary.html", week=diary.get_week(date))
