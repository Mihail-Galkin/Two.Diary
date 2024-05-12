import os

import sqlalchemy
from cryptography.fernet import Fernet
from sqlalchemy import orm

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source_session = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sessions = orm.relationship("Session", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} {self.email}'

    def set_password(self, password):
        cipher = Fernet(os.environ["PASSWORD_KEY"].encode()).encrypt(password.encode()).decode()
        self.password = cipher

    def get_password(self):
        password = Fernet(os.environ["PASSWORD_KEY"].encode()).decrypt(self.password).decode()
        return password
