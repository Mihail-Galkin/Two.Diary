from datetime import date as d
from datetime import timedelta as td

from flask import request, render_template

from app.decorators import login_required, only_ajax
from app.marks import bp
from app.parse import get_raw_marks
from app.utils import str_to_date


@bp.route('/marks')
@only_ajax()
@login_required()
def marks_(diary):
    marks = {}
    live_mode = False
    if request.args.get("selected") == "Итоговые оценки":
        raw_marks = get_raw_marks(diary.session, diary.guid, final_grades=True)
        print(raw_marks)

        for i in raw_marks:
            int_marks = list(map(int, list(filter(bool, (i[2:5])))))
            if len(int_marks) == 0:
                average = 0
            else:
                average = round(sum(int_marks) / len(int_marks), 2)
            marks[i[1]] = {"marks": int_marks, "average": average, "sum": sum(int_marks), "count": len(int_marks), "count_5": int_marks.count(5), "count_4": int_marks.count(4), "count_3": int_marks.count(3), "count_2": int_marks.count(2)}
    elif request.args.get("selected") == "Live":
        live_mode = True
        date = str_to_date(diary.current["dateBegin"])
        while date <= d.today():
            date += td(days=1)
            day = diary.get_day(date)
            for i, subject in day.subjects.items():
                for mark in subject.marks:
                    if subject.name not in marks:
                        marks[subject.name] = {"marks": []}
                    marks[subject.name]["marks"].append({"value": int(mark), "date": day.str_date, "subject_index": i})

        for subject in marks:
            summ = sum(list(map(lambda x: x["value"], marks[subject]["marks"])))
            count = len(marks[subject]["marks"])
            marks[subject]["average"] = round(summ / count, 2)
            marks[subject]["sum"] = summ
            marks[subject]["count"] = count


    # TODO abc
    # Default marks: {"Информатика": {"marks": [2, 3], "average": 2.5}, ...}
    # Live mode: {"Информатика": {"marks": [{} "average": 2.5}, ...}

    else:
        date_begin = request.args.get("begin", diary.current["dateBegin"])
        date_end = request.args.get("end", diary.current["dateEnd"])

        raw_marks = get_raw_marks(diary.session, diary.guid, date_begin, date_end)

        for i in raw_marks:
            if i[2] == "нет":
                int_marks = []
                average = 0
            else:
                int_marks = list(map(int, i[2].split(",")))
                average = round(sum(int_marks) / len(int_marks), 2)
            marks[i[1]] = {"marks": int_marks, "average": average, "sum": sum(int_marks), "count": len(int_marks), "count_5": int_marks.count(5), "count_4": int_marks.count(4), "count_3": int_marks.count(3), "count_2": int_marks.count(2)}

    return render_template("marks.html", marks=marks,
                           periods=diary.quarters + [{"name": "Итоговые оценки"}, {"name": "Live"}],
                           selected=request.args.get("selected", diary.current["name"]),
                           live_mode=live_mode)
