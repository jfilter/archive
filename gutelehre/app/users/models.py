from flask.ext.login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from app.data import db

USER_RANK_DISABLED = -1
USER_RANK_USER = 0
USER_RANK_MOD = 1
USER_RANK_ADMIN = 2

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(70))
  rank = db.Column(db.SmallInteger, default=USER_RANK_DISABLED)

  # tickets = db.relationship('Ticket', backref='User',
  #                               lazy='dynamic')

  def __repr__(self):
    return '<User %r>' % (self.id)

  def hash_password(self):
    self.password = generate_password_hash(self.password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def is_active(self):
    return self.rank > USER_RANK_DISABLED

  def is_mod(self):
    return self.rank == USER_RANK_MOD

  def is_admin(self):
    return self.rank == USER_RANK_ADMIN
