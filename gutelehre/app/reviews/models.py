from app.data import db

class Uni(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), index=True, unique=True, nullable=False)
	short_name = db.Column(db.String(50), index=True, unique=True, nullable=False)
	url = db.Column(db.String(100))
	description = db.Column(db.Text)
	created_on = db.Column(db.DateTime, default=db.func.now())

	# courses = db.relationship('Course', backref='Uni',lazy='dynamic')

	def __repr__(self):
			return '<Uni %s>' % (self.name)


STATUS_HIDDEN = 0
STATUS_UNREVIEWED = 1
STATUS_VISIBLE = 2

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(500), nullable=False)
	course_type = db.Column(db.String(10))
	created_on = db.Column(db.DateTime, default=db.func.now())
	ip_adress = db.Column(db.String(40))
	status = db.Column(db.SmallInteger, default=STATUS_UNREVIEWED)

	uni_id = db.Column(db.Integer, db.ForeignKey('uni.id'))
	uni = db.relationship('Uni', backref=db.backref('courses', lazy='dynamic'))

	# reviews = db.relationship('Review', backref='Course',                            lazy='dynamic')

	def __repr__(self):
			return '<Course %r>' % (self.name)


class Review(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(500), nullable=False)
	teacher = db.Column(db.String(500))
	content = db.Column(db.Text, nullable=False)
	rating = db.Column(db.SmallInteger, nullable=False)
	semester = db.Column(db.String(10), nullable=False)
	status = db.Column(db.SmallInteger, default=STATUS_UNREVIEWED)
	ups = db.Column(db.SmallInteger, default=0)
	downs = db.Column(db.SmallInteger, default=0)
	count_views = db.Column(db.Integer, default=0)
	created_on = db.Column(db.DateTime, default=db.func.now())
	ip_adress = db.Column(db.String(40), nullable=False)

	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	course = db.relationship('Course', backref=db.backref('reviews', lazy='dynamic'))


	#tickets = db.relationship('Ticket', backref='Review',                           lazy='dynamic')

	def __repr__(self):
		return '<Review %r>' % (self.id)

	def approve(self):
		self.status = STATUS_VISIBLE

	def disapprove(self):
		self.status = STATUS_HIDDEN


class Semester(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(4), nullable=False)

	def __repr__(self):
		return '<Semester %r>' % (self.name)