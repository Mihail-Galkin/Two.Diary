"""
Основной пакет приложения, реализующий работу flask web сервера.

Директории:
    forms                      содержит wtforms.
    models                     содержит модели sqlalchemy.
    templates:                 содержит шаблоны jinja.
        parts                  содержит шаблоны, являющиеся не страницей, а ее частью.
    static:                    содержит статические файлы сайта.
        images                 содержит изображения.
        scripts                содержит javascript файлы.
        styles                 содержит css стили.
    [остальные директории]     являются пакетами - маршрутизаторами

Модули:
    utils                      содержит вспомогательные функции
    useragent                  содержит генератор поддельных заголовков для запроса
    parse                      содержит набор функций для получения информации с one.43edu.ru
    extensions                 содержит инициализацию необходимых расширений flask
    diary_class                содержит классы, реализующие электронный дневник
    decorators                 содержит декораторы
    crypt                      содержит криптографические функции
"""
import logging
import os
import sys
from datetime import timedelta as td

import flask
from flask import Flask

from app.extensions import db
from config import DevelopmentConfig, ProductionConfig


def create_app():
    from app.decorators import diaries
    app = Flask(__name__)

    if os.getenv("FLASK_ENV") == "development":
        config = DevelopmentConfig
    elif os.getenv("FLASK_ENV") == "production":
        config = ProductionConfig
    else:
        logging.critical("Укажите режим запуска в FLASK_ENV (development, production)")
        sys.exit()

    app.config.from_object(config)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.diary import bp as diary_bp
    app.register_blueprint(diary_bp)

    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.marks import bp as marks_bp
    app.register_blueprint(marks_bp)

    from app.one_type_subjects import bp as ots_bp
    app.register_blueprint(ots_bp)

    from app.schedule import bp as schedule_bp
    app.register_blueprint(schedule_bp)

    from app.subject_modal import bp as modal_bp
    app.register_blueprint(modal_bp)

    @app.before_request
    def before_request():
        """ Делает сессию бесконечной """
        flask.session.permanent = True
        app.permanent_session_lifetime = td(days=365)

    with app.app_context():
        db.create_all()
        return app
