from flask import Blueprint

bp = Blueprint('one_type_subjects', __name__)

from app.one_type_subjects import routes