from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(message="Поле пустое"), Email(message="Неверный email")], )
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле пустое")])
    submit = SubmitField('Войти')