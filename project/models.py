import os
from . import db
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
import jwt
from time import time
from sqlalchemy import or_

class User(UserMixin, db.Model):

  id = db.Column(db.Integer, primary_key = True, nullable = False)
  email = db.Column(db.String(100), unique = True, nullable = True)
  password = db.Column(db.String(100), nullable = True)
  username = db.Column(db.String(150), nullable = True)
  city = db.Column(db.String(150), nullable = True)
  country = db.Column(db.String(150), nullable = True)
  state = db.Column(db.String(150), nullable = True)
  CEP = db.Column(db.String(150), nullable = True)
  rua = db.Column(db.String(150), nullable = True)
  numero = db.Column(db.String(150), nullable = True)
  complemento = db.Column(db.String(150), nullable = True)
  CPF = db.Column(db.String(150), unique = True, nullable = True)
  PIS = db.Column(db.String(150), unique = True, nullable = True)

  def __repr__(self):
      return 'User {}'.format(self.username)

  @staticmethod
  def verify_email(email):
    user = User.query.filter_by(email=email).first()

    return user

class OAuth(OAuthConsumerMixin, db.Model):
  __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
  provider_user_id = db.Column(db.String(256), nullable = False)
  provider_user_login = db.Column(db.String(256))
  user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
  user = db.relationship(User)