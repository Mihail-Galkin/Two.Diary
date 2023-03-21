import sqlalchemy
from sqlalchemy import orm

from app import db


class Session(db.Model):
    __tablename__ = 'sessions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    value = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    def __repr__(self):
        return f'<Session> {self.id} {self.value} {self.user_id}'

