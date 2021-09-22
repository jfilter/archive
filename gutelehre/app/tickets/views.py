from flask.ext.login import current_user
from flask import Flask
from flask.ext.admin import BaseView, expose

from models import Ticket, TICKET_STATUS_OPEN
from app.reviews.models import Review, Course
from app.data import db

class TicketsView(BaseView):
	
	def is_accessible(self):
		return current_user.is_authenticated() and (current_user.is_mod() or current_user.is_admin())

	@expose('/')
	def index(self):
		tickets = Ticket.query.with_entities(Ticket.id, Ticket.created_on, Ticket.new_course_name, Review.title, Review.teacher, Review.teacher, Review.rating, Review.content).filter(Ticket.status == TICKET_STATUS_OPEN).join(Review).limit(100).all()

		return self.render('admin/tickets.html', tickets=tickets)

	@expose('/approve/<int:ticket_id>/', methods=('GET', 'POST'))
	def approve_ticket(self, ticket_id):
		ticket = Ticket.query.get(ticket_id)
		review = Review.query.get(ticket.review_id)

		new_course_name = ticket.new_course_name
		new_course_uni_id = ticket.new_course_uni_id
		if new_course_name:
			old_course = Course.query.filter(Course.uni_id == new_course_uni_id, Course.name == new_course_name).first()
			if old_course:
				review.course_id = old_course.id
				review.approve() # approve here beauce of session
				ticket.close()	# approve here beauce of session
				db.session.commit()
			else:
				# create new Course at save to DB
				course = Course()
				course.name = new_course_name
				course.uni_id = new_course_uni_id
				course.ip_adress = review.ip_adress
				db.session.add(course)
				review.approve() # approve here beauce of session
				ticket.close()	# approve here beauce of session
				db.session.commit()

				# set ID to review of new course
				review.course_id = course.id
				db.session.commit()
		else:
			# just close ticket and approve post
			review.approve()
			ticket.close()
			db.session.commit()


		return self.render('admin/tickets_approved.html')