from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User,Quiz,Question,Results
from flask_login import login_required, current_user, login_user, logout_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html', title = 'Sign in', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register',methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, points=0)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Congratulations, you're now a registered user!")
		return redirect(url_for('login'))
	return render_template('register.html', title='Registration page', form = form)

@app.route('/admin/home')
def admin():
	if current_user.get_id() != 0:
		flash("You don't have access to this page!")
		return redirect(url_for('index'))
	return render_template('./admin/home.html', title='Admin Homepage')

