# -*- coding: utf8 -*-
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from application import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(100))
    login_time = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def get_by_id(self, id):
        return self.query.filter_by(id=id).first()

    @staticmethod
    def add(user):
        db.session.add(user)
        return session_commit()

    def update(self, id, login_time):
        self.query.filter_by(id=id).update({Users.login_time: login_time})
        return session_commit()

    @staticmethod
    def check_password(hash, password):
        return check_password_hash(hash, password)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return str(e)
