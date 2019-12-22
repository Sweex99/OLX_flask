from datetime import datetime
from flaskblog import db, login_manager, bcrypt
from flask_login import UserMixin
from hashlib import md5
from wtforms import BooleanField, widgets, TextAreaField

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db. Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship( 'Post', backref='author', lazy=True)
	orders = db.relationship('Order', lazy=True)
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	admin = db.Column(db.Boolean())
	notes = db.Column(db.UnicodeText)

	def __init__(self, username, email, password, notes='', admin=False):
		self.username = username
		self.email = email
		#self.password = bcrypt.generate_password_hash(password)
		self.password = password
		self.admin = admin
		self.notes = notes

	def is_admin(self):
		return self.admin

	def __repr__(self):
		return "User('{self.username}', '{self.email}', '{self.image_file}')"

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	#def set_password(self, password):
		#self.password_hash = generate_password_hash(password)

	#def check_password(self, password):
		#return check_password_hash(self.password_hash, password)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	# admin = db.Column(db.Boolean())

	def __init__(self, title, content, user_id, category_id):
		self.title = title
		self.content = content
		self.user_id = user_id
		self.category_id = category_id

	def __repr__(self):
		return "Post('{self.title}', '{self.date_posted}')"

class CKTextAreaWidget(widgets.TextArea):
	def __call__(self, field, **kwargs):
		kwargs.setdefault('class_', 'ckeditor')
		return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
	widget = CKTextAreaWidget()

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(100))
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	posts = db.relationship('Post', backref='category', lazy=True)

	def __init__(self, category_name):
		self.category_name = category_name

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	posts = db.relationship('Post', lazy=True)

	def __init__(self, user_id, post_id):
		self.user_id = user_id
		self.post_id = post_id

