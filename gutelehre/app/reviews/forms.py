# -*- coding: latin-1 -*-

from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, ValidationError, length

from models import Review


class ReviewForm(Form):
	semester = fields.SelectField("In welchem Semester hast du die Lehrveranstaltung belegt?")	
	teacher = fields.StringField(unicode("Welche Personen waren in die Lehre involviert? (optional)", "UTF-8")
		, validators=[length(max=500)], default="z.B. Prof. Schmidt, Karl Petersen")
	rating = fields.HiddenField("Rating", validators = [InputRequired()])
	title = fields.StringField(unicode("Gib deiner Bewertungen einen aussagekräftigen Titel","UTF-8")
		, validators=[InputRequired(), length(max=500)], default="z.B. Tolle Vorlesung, noch besseres Seminar")
	content = fields.TextAreaField(unicode("""
		Bitte schreibe einen Text, um deine Bewertungen ausreichend zu begründen.
		Du kannst, zum Beispiel, folgende Fragen beantwoten:
		Was fandest du gut? Was kann noch verbessert werden?
		Was würdest du Studierenden, die sich für diese Lehrveranstaltung interessieren, empfehlen? <br>
		Bitte achte darauf, dass du die Persönlichkeitsrechte
		einzelner Personen nicht verletzt.<br>Hier findest du eine beispielhafte Gliederung, an die du dich aber nicht halten muss.
		""", "UTF-8")
		, validators=[InputRequired()], default=unicode("""Vorlesung\n\nÜbung/Seminar\n\nUnterlagen zur Lehrveranstaltung\n\nKlausur\n\nVerbessungsvorschläge\n\nEmpfehlungen für zukünftige Studierenden, die diese Veranstaltung belegen\n\n""", "UTF-8"))

# 	-vorlesung
# - übung
# - material
# - klausur
# - was sollte besser werden
