# -*- coding: utf-8 -*- 

from flask import render_template, request, flash, redirect, Markup
from app import application, db

@application.route('/')
@application.route('/index.html')
def index():
	title = "Lehrveranstaltung Bewertung Bewerten"
	return render_template('index.html', title=title)

@application.route('/Impressum')
def impress():
	title = unicode("Impressum",'utf-8')
	return render_template('impress.html', title=title)

@application.route('/Datenschutz')
def about_us():
	title = unicode("Datenschutzerklärung",'utf-8')
	return render_template('privacy.html', title=title)

@application.route('/Informationen')
def contac():
	return render_template('infos.html', title="Informationen")

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
