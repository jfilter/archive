from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from flask import Flask
from flask.ext.admin import Admin

# Create customized model view class
class AdminView(ModelView):

	def is_accessible(self):
		return current_user.is_authenticated() and current_user.is_admin()

