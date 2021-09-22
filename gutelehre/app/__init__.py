from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask_wtf.csrf import CsrfProtect
from flask.ext.mail import Mail

from config import *
from auth import login_manager
from admin import AdminView
from data import db
from mails import mail


application = Flask(__name__)
application.config.from_object(__name__)

db = SQLAlchemy(application)
db.init_app(application)

login_manager.init_app(application)

mail = Mail(application)


# This makes the app threadsafe. Is there a bug with flask-sqlachemy?
@application.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()



from reviews.models import *
from users.models import *
from tickets.models import *
import users.views
import reviews.views
from tickets.views import TicketsView

admin = Admin(application, "gutelehre.de")
admin.add_view(AdminView(User, db.session, category='Models'))
admin.add_view(AdminView(Uni, db.session, category='Models'))
admin.add_view(AdminView(Course, db.session, category='Models'))
admin.add_view(AdminView(Review, db.session, category='Models'))
admin.add_view(AdminView(Semester, db.session, category='Models'))
admin.add_view(AdminView(Ticket, db.session, category='Models'))

admin.add_view(TicketsView(name='Tickets'))

application.register_blueprint(users.views.users)
application.register_blueprint(reviews.views.reviews)

# if not app.debug:
import logging
from logging.handlers import SMTPHandler
mail_handler = SMTPHandler('smtp.vulpecula.uberspace.de',
                           'server-error@gutelehre.de',
                           ['tickets@gutelehre.de'], 'YourApplication Failed')
mail_handler.setLevel(logging.ERROR)
application.logger.addHandler(mail_handler)


if False:
	with application.app_context():
		db.drop_all()
		db.create_all()
		user = User()
		user.name = "Joe"
		user.email = "hi@jfilter.de"
		user.password = "lol"
		user.hash_password()
		user.rank = 2
		db.session.add(user)

		ovgu = Uni()
		ovgu.name = "Otto-von-Guericke Universitaet"
		ovgu.short_name = "OVGU"
		db.session.add(ovgu)

		hs = Uni()
		hs.name = "Hochschule Magdeburg"
		hs.short_name = "HSM"
		db.session.add(hs)

		c1 = Course()
		c1.name = "Bioinformatik"
		c1.ip_adress = "127.0.0.1"
		c1.uni_id = 1
		db.session.add(c1)

		c2 = Course()
		c2.name = "AuD"
		c2.uni_id = 1
		c2.ip_adress = "127.0.0.1"
		db.session.add(c2)

		c3 = Course()
		c3.name = "Datenbanken"
		c3.uni_id = 1
		c3.ip_adress = "127.0.0.1"
		db.session.add(c3)

		s1 = Semester()
		s1.name = "SS13"
		db.session.add(s1)

		s1 = Semester()
		s1.name = "WS13"
		db.session.add(s1)	

		s1 = Semester()
		s1.name = "SS14"
		db.session.add(s1)


		for x in range(0, 10):
			r1 = Review()
			r1.title = "Sehr super" + str(x)
			r1.rating = 4
			r1.semester = "WS13"
			r1.ip_adress = "127.0.0.1"
			r1.content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
	tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
	quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
	consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
	cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
	proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

	Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
	tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
	quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
	consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
	cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
	proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

	Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
	tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
	quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
	consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
	cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
	proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

	Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
	tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
	quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
	consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
	cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
	proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

			"""
			r1.course_id = 1
			r1.status = 2
			db.session.add(r1)

		db.session.commit()


import views
