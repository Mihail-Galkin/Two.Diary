import os

import sqlalchemy
from sqlalchemy import orm

from app import db
from app.crypt import xor


class User(db.Model):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    guid = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source_session = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sessions = orm.relationship("Session", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} {self.email} {self.guid}'

    def set_password(self, password):
        self.password = xor(password, os.getenv("PASSWORD_KEY"))

    def get_password(self):
        return xor(self.password, os.getenv("PASSWORD_KEY"))
