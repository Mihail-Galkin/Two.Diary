from flask import Blueprint

bp = Blueprint('schedule', __name__)

from app.schedule import routes