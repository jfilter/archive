from flask.ext.wtf import Form
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError

from models import User

class LoginForm(Form):
	email = fields.StringField(validators=[InputRequired(), Email()])
	password = fields.PasswordField(validators=[InputRequired()])

	# WTForms supports "inline" validators
	# which are methods of our `Form` subclass
	# with names in the form `validate_[fieldname]`.
	# This validator will run after all the
	# other validators have passed.
	def validate_password(form, field):
		try:
			user = User.query.filter(User.email == form.email.data).one()
		except (MultipleResultsFound, NoResultFound):
			raise ValidationError("Invalid user")
		if user is None:
			raise ValidationError("Invalid user")
		if not user.check_password(form.password.data):
			raise ValidationError("Invalid password")

		# Make the current user available
		# to calling code.
		form.user = user

class RegistrationForm(Form):
	name = fields.StringField("Name")
	email = fields.StringField("Email", validators=[InputRequired(), Email()])
	password = fields.PasswordField("Passwort", validators=[InputRequired()])

	def validate_email(form, field):
		user = User.query.filter(User.email == field.data).first()
		if user is not None:
			raise ValidationError("Deine Emailadresse wurde schon benutzt.")