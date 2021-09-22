from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_required, login_user, logout_user

from app.data import db
from forms import LoginForm, RegistrationForm
from models import User

users = Blueprint('users', __name__)


@users.route('/login/', methods=('GET', 'POST'))
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if not form.user.is_active():
			flash("Der Account ist nicht aktiv.")
			return redirect ('/')
		login_user(form.user)
		flash("Erfolgreich eingeloggt.")
		return redirect('/')
	return render_template('users/login.html', form=form)


@users.route('/register/', methods=('GET', 'POST'))
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User()
		form.populate_obj(user)
		user.hash_password()
		db.session.add(user)
		db.session.commit()
		# login_user(user)
		flash("Erfolgreich registriert.")
		return redirect('/')
	return render_template('users/register.html', form=form)


@users.route('/logout/')
@login_required
def logout():
	logout_user()
	flash("Erfolgreich ausgeloggt.")
	return redirect('/')