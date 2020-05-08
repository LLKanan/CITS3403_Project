from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateQuizForm, CreateQuestionForm
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
def admin_home():
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	return render_template('./admin/home.html', title = 'Admin HomePage')

@app.route('/admin/manage_users',methods=['GET', 'POST'])
def manage_users():
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	results = db.session.execute('Select * from user where user_id != 0')
	return render_template('./admin/manage_users.html',title='Manage Users',results = results)

@app.route('/admin/manage_users/remove/<int:user_id>')
def remove_user(user_id):
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	if user_id == 0:
		flash('Cannot Remove Admin, redirecting to userlist')
		return redirect(url_for('manage_users'))
	query = 'Select * from user where user_id == ' + str(user_id)
	edit_user = db.session.execute(query)
	if edit_user:
		#temp = 'Delete from user where user_id == ' + str(user_id)
		#db.session.execute(temp) 
		User.query.filter(User.user_id == user_id).delete()
		db.session.commit()
		flash("User_ID #{user_id} successfully removed".format(user_id = user_id))
		return redirect(url_for('manage_users'))
	else:
		flash("Error couldn't find #{user_id}, redirecting to user list".format(user_id = user_id))
		return redirect(url_for('manage_users'))

@app.route('/admin/manage_quizzes',methods=['GET', 'POST'])
def manage_quizzes():
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	results = db.session.execute('Select * from Quiz where removed == 0')
	return render_template('./admin/manage_quizzes.html',title='Manage Quizzes',results = results)

@app.route('/admin/manage_quizzes/remove/<int:quiz_id>')
def remove_quiz(quiz_id):
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	query = 'Select * from quiz where quiz_id == ' + str(quiz_id)
	temp_quiz = db.session.execute(query)
	if temp_quiz:
		quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
		quiz.removed = 1
		db.session.commit()
		flash("Quiz_ID #{quiz_id} successfully removed".format(quiz_id = quiz_id))
		return redirect(url_for('manage_quizzes'))
	else:
		flash("Error couldn't find #{quiz_id}, redirecting to quiz list".format(quiz_id = quiz_id))
		return redirect(url_for('manage_quizzes'))

@app.route('/admin/create_quiz',methods=['GET', 'POST'])
def create_quiz():
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	form = CreateQuizForm()
	if form.validate_on_submit():
		quiz = Quiz(quiz_name = form.name.data,quiz_image = form.image.data, removed = 0)
		db.session.add(quiz)
		db.session.commit()
		#Placeholder for linking to creating questions in a quiz
		#flash("Congratulations, you've successfully added a quiz!")
		return redirect(url_for('create_question',quiz_id = quiz.quiz_id))
	return render_template('./admin/create_quiz.html',title = 'Create new Quiz',form = form)

@app.route('/admin/create_quiz/<int:quiz_id>',methods=['GET', 'POST'])
def create_question(quiz_id):
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	form = CreateQuestionForm()
	if form.validate_on_submit():
		question = Question(quiz_id = quiz_id, youtube_link = form.youtube_link.data, duration = form.duration.data, correct_answer = form.correct_answer.data, option_1 = form.option_1.data, option_2 = form.option_2.data, option_3 = form.option_3.data)
		db.session.add(question)
		db.session.commit()
		return redirect(url_for('create_question',quiz_id = quiz_id))
	return render_template('./admin/create_question.html',form = form)

