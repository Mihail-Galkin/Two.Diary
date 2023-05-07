import logging
import secrets

import flask
from flask import render_template, redirect, make_response, session

from app import db
from app.forms.login import LoginForm
from app.login import bp
from app.models.sessions import Session
from app.models.users import User
from app.parse import auth, get_session_cookie, get_guid


@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = auth(form.email.data, form.password.data)
        if sess is None:
            return render_template('login.html', title='Авторизация', message="Неверный пароль", form=form)
        cookie = get_session_cookie(sess)

        db_sess = db.session
        q = db_sess.query(User).filter(User.email == form.email.data)
        if q.count() == 0:
            user = User()
            user.set_password(form.password.data)
            user.email = form.email.data
            user.guid = get_guid(sess)
            user.source_session = cookie
            db_sess.add(user)
        else:
            user = q.first()

        session = Session()
        session.value = secrets.token_hex(16)
        session.user = user

        db_sess.add(session)
        db_sess.commit()

        flask.session["session"] = session.value
        return redirect("/")
    return render_template('login.html', title='Авторизация', form=form)


@bp.route("/logout")
def logout():
    if "session" not in session.keys():
        return redirect("/")
    sess = session.pop("session")
    db_sess = db.session
    db_sess.query(Session).filter(Session.value == sess).delete()
    db_sess.commit()
    return redirect("/login")
