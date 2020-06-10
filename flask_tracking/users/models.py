from passlib.hash import sha256_crypt
import random

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from flask_tracking.data import CRUDMixin, db
from flask_tracking.tracking.models import Site, Visit



class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(120))
    _clear_pw = db.Column(db.String(120))
    _salt = db.Column(db.String(120))
    sites = db.relationship('Site', backref='owner', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, pw_input):
        rounds = current_app.config.get("HASH_ROUNDS")
        self._password = sha256_crypt.hash(pw_input, rounds=rounds)
        self._clear_pw = pw_input
        if self._salt is None:
            self._salt = random.random()

    def is_valid_password(self, pw):
        return sha256_crypt.verify(pw, self._password)

    def __repr__(self):
        return f'<User #{self.id}>'
