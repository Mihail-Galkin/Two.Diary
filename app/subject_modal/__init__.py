from flask import Blueprint

bp = Blueprint('subject_modal', __name__)

from app.subject_modal import routes