from flask.ext.login import current_user
from datetime import datetime

from app.data import db
from helpers import send_email

TICKET_STATUS_OPEN = 1
TICKET_STATUS_CLOSED = 0

class Ticket(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.SmallInteger, default=TICKET_STATUS_OPEN)
	created_on = db.Column(db.DateTime, default=db.func.now())
	closed_on = db.Column(db.DateTime)
	new_course_name = db.Column(db.String(500))

	new_course_uni_id = db.Column(db.Integer, db.ForeignKey('uni.id'))
	review_id = db.Column(db.Integer, db.ForeignKey('review.id'))

	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #admin
	user = db.relationship('User', backref=db.backref('tickets', lazy='dynamic'))

	def __init__(self):
		send_email()

	def __repr__(self):
		return '<Ticket %r>' % (self.id)

	def close(self):
		self.status = TICKET_STATUS_CLOSED
		self.user_id = current_user.id
		self.closed_on = datetime.now()
