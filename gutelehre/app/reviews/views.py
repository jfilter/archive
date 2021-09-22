from flask import Blueprint, flash, redirect, render_template, request, url_for, make_response, abort
from sqlalchemy import desc

from app.data import db
from forms import ReviewForm
from models import Review, Uni, Course, Semester, STATUS_VISIBLE
from app.tickets.models import Ticket

reviews = Blueprint('reviews', __name__)

### SCHREIBEN

@reviews.route('/Bewerten/', methods=('GET', 'POST'))
def writing_choose_uni():
	if request.method == 'GET': # i post to this, if i want to reset cookie
		uni_id = request.cookies.get('uni_id')
		if uni_id:
			return redirect('/Bewerten/' + uni_id + '/')
	unis = Uni.query.order_by(Uni.name).all()
	title = "Lehrveranstaltung Bewerten"
	return render_template('reviews/writing/choose_uni.html', unis=unis, title=title)


@reviews.route('/Bewerten/<int:uni_id>/', methods=('GET', 'POST'))
def writing_choose_course(uni_id):
	uni = Uni.query.get_or_404(uni_id)
	courses = Course.query.filter(Course.uni_id == uni_id).order_by(Course.name)
	title = uni.name + ' - Lehrveranstaltung Bewerten'
	resp = make_response(render_template('reviews/writing/choose_course.html', uni=uni, courses=courses, title=title))

	request_uni_id = request.cookies.get('uni_id')
	if not request_uni_id == uni_id:
		resp.set_cookie('uni_id', str(uni_id), expires=2000000000)
	return resp


@reviews.route('/Bewerten/<int:uni_id>/<int:course_id>', methods=('GET', 'POST'))
def writing_review(uni_id, course_id):
	form = ReviewForm()
	form.semester.choices = [(s.name, s.name) for s in Semester.query.order_by(Semester.id)]

	if form.validate_on_submit():
		review = Review()
		form.populate_obj(review)
		review.ip_adress = request.remote_addr #set ip from request
		review.rating = int(review.rating) # cast, because it was a string

		# Don't create relationship, because course does not exist yet!
		# We will create on later, when we are going to review the review. (hihi)
		if course_id != 0:
			review.course_id = course_id
		db.session.add(review)
		db.session.commit()

		ticket = Ticket()
		ticket.review_id = review.id

		#only set the name in the ticket if we really want to create a new course
		if course_id == 0: 
			ticket.new_course_name = request.args.get('new_course')

		ticket.new_course_uni_id = str(uni_id)
		db.session.add(ticket)
		db.session.commit()
		return render_template('reviews/writing/review_success.html') #to new post

	uni = Uni.query.get(uni_id)
	# create a dummy course, if the course doesn't exist yet. we will create a course later
	if course_id == 0:
		course = Course()
		course.name = request.args.get('new_course')
		if course.name == None or course.name == "":
			return redirect("/")
		course.id = 0
	else:
		course = Course.query.get(course_id)

	title = uni.name + " - Lehrveranstaltung Bewerten"
	return render_template('reviews/writing/review.html', form=form, course=course, uni=uni, title=title)


### LESEN


@reviews.route('/Bewertungen/', methods=('GET', 'POST'))
def reading_choose_uni():
	if request.method == 'GET': # i post to this, if i want to reset cookie
		uni_id = request.cookies.get('uni_id')
		if uni_id:
			return redirect('/Bewertungen/' + uni_id + '/')
	unis = Uni.query.order_by(Uni.name).all()
	title = "Lehrveranstaltungm Bewertung"
	return render_template('reviews/reading/choose_uni.html', unis=unis, title=title)


@reviews.route('/Bewertungen/<int:uni_id>/', methods=('GET', 'POST'))
def reading_choose_course(uni_id):
	uni = Uni.query.get_or_404(uni_id)
	courses = Course.query.filter(Course.uni_id == uni_id).order_by(Course.name).all()
	title = uni.name + " - Lehrveranstaltung Bewertung"
	resp = make_response(render_template('reviews/reading/choose_course.html', uni=uni, courses=courses, title=title))

	request_uni_id = request.cookies.get('uni_id')
	if not request_uni_id == uni_id:
		resp.set_cookie('uni_id', str(uni_id), expires=2000000000)
	return resp


@reviews.route('/Bewertungen/<int:uni_id>/<int:course_id>/', methods=('GET', 'POST'))
def reading_choose_review(uni_id, course_id):

	uni = Uni.query.get_or_404(uni_id)
	course = Course.query.get_or_404(course_id)
	if course.uni_id != uni.id:
		abort(404)

	reviews = Review.query.filter(Review.course_id == course_id, Review.status == STATUS_VISIBLE).order_by(desc(Review.created_on)).all()
	title = course.name + ' - ' +uni.name + " - Lehrveranstaltung Bewertung"
	return render_template('reviews/reading/choose_review.html', uni=uni, course=course, reviews=reviews, title=title)


@reviews.route('/Bewertungen/<int:uni_id>/<int:course_id>/<int:review_id>', methods=('GET', 'POST'))
def reading_show_review(uni_id, course_id, review_id):
	uni = Uni.query.get_or_404(uni_id)
	course = Course.query.get_or_404(course_id)
	review = Review.query.get_or_404(review_id)
	if review.status != STATUS_VISIBLE or review.course_id != course.id or course.uni_id != uni.id:
		abort(404)

	review.count_views += 1
	db.session.commit()

	title = course.name + ' - ' +uni.name + " - Lehrveranstaltung Bewertung"
	return render_template('reviews/reading/show_review.html', uni=uni, course=course, review=review, title=title)
