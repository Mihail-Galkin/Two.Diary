from flask import render_template

from app.decorators import login_required
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required(recreate_diary=True)
def index(diary):
    return render_template("index.html", guids=diary.guids)
