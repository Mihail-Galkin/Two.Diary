import copy
from datetime import timedelta as td

from flask import request, render_template

from app.decorators import only_ajax, login_required
from app.one_type_subjects import bp
from app.utils import str_to_date, date_to_str


@bp.route('/one-type-subjects')
@only_ajax()
@login_required()
def one_type_subjects(diary):
    # TODO: задокументировать
    on_page = 4

    subject_name = request.args.get("subject")
    delta = int(request.args.get("delta", 1))
    page = int(request.args.get("page", 0))

    period = diary.current
    day = str_to_date(request.args.get("period-day"))
    quarters = diary.quarters
    for i in quarters:
        if str_to_date(i["dateBegin"]) <= day <= str_to_date(i["dateEnd"]):
            period = i
            break

    period_begin = str_to_date(period["dateBegin"])
    period_end = str_to_date(period["dateEnd"])

    last_day = str_to_date(request.args.get("last-day", date_to_str(period_end)))
    first_day = str_to_date(request.args.get("first-day", date_to_str(period_end)))

    last_subject = int(request.args.get("last-subject", -1))
    first_subject = int(request.args.get("first-subject", 100))

    current_date = copy.copy(first_day if delta == 1 else last_day)

    subjects = []  # Subjects format: [(day, subject_index), ...]
    while period_begin <= current_date <= period_end and on_page >= 0:
        current_date -= td(days=delta)

        for i, subject in diary.get_day(current_date).subjects.items():
            if (current_date == last_day and i <= last_subject) or (current_date == first_day and i >= first_subject):
                continue
            if subject.name == subject_name:
                on_page -= 1
                subjects.append((diary.get_day(current_date), i))

                if on_page == -1:
                    break
    is_last_page = False
    is_first_page = False
    if on_page == -1:
        subjects.pop(-1)
    else:
        is_last_page = (delta == 1)
        is_first_page = (delta == -1)

    if delta == -1:
        subjects.reverse()

    return render_template("one-type-subjects.html",
                           subjects=subjects,
                           page=page + delta,
                           is_last_page=is_last_page,
                           is_first_page=is_first_page,
                           day=request.args.get("period-day"))
