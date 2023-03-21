from flask import Blueprint

bp = Blueprint('marks', __name__)

from app.marks import routes