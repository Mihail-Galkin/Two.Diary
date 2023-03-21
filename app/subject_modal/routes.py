from datetime import date as d

from flask import request, render_template

from app.decorators import only_ajax, login_required
from app.subject_modal import bp
from app.utils import date_to_str, str_to_date


@bp.route('/subject-modal')
@only_ajax()
@login_required()
def subject_modal(diary):
    date = request.args.get("date", "today")
    if date == "today":
        date = date_to_str(d.today())
    lesson = int(request.args.get("lesson"))

    day = diary.get_day(str_to_date(date))
    subject = day.subjects[lesson]
    return render_template("parts/subject-modal.html", subject=subject)
