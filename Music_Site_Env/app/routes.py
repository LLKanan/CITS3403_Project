from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateQuizForm, CreateQuestionForm, QuestionForm
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

@login_required
@app.route('/view_quizzes',methods=['GET', 'POST'])
def view_quizzes():
	results = db.session.execute('Select * from Quiz where removed == 0')
	return render_template('./view_quizzes.html',title='View Quizzes',results = results)

def submit_answer(quiz_id,question_list,user_answer,current_question):
	result = Results(user_id = current_user.get_id(), quiz_id = quiz_id,question_id = question_list[current_question][0], user_answer = user_answer, correct = (True if (user_answer == question_list[current_question][4]) else False))
	db.session.add(result)
	db.session.commit()

@login_required
@app.route('/start_quiz/<int:quiz_id>/<current_question>',methods=['GET', 'POST'])
def start_quiz(quiz_id,current_question):
	form = QuestionForm()
	current_question = int(current_question)
	question_list = (db.session.execute('Select * from Question where quiz_id ==' + str(quiz_id) + " ORDER BY question_id")).fetchall()
	quiz_name = (db.session.execute('Select * from Quiz where quiz_id ==' + str(quiz_id))).first()	
	temp_list = question_list[current_question][4:]
	option_list = []
	for option in temp_list:
		option_list.append((option,option))
	form.set_options(option_list)
	if form.validate_on_submit():
		submit_answer(quiz_id,question_list,form.answer.data,current_question)
		if current_question + 1 < len(question_list):
			return redirect(url_for('start_quiz',quiz_id = quiz_id, current_question = current_question + 1))
		else:
			return redirect(url_for('quiz_results',quiz_id = quiz_id))
	return render_template('./question_page.html', title = quiz_name[1], question_list = question_list,current_question = current_question, quiz_name = quiz_name[1], form = form)


@login_required
@app.route('/quiz_results/<quiz_id>')
def quiz_results(quiz_id):
	user_id = current_user.get_id()
	list_questions = db.session.execute('Select * from Question where quiz_id ==' + str(quiz_id) + " ORDER BY question_id").fetchall()
	results = []
	correct_counter = 0
	total = 0
	for question in list_questions:
		temp = []
		question_id = question[0]
		correct_answer = question[4]
		user_answer = db.session.execute('Select * From Results where user_id == ' + str(user_id) + " and question_id == " + str(question_id) + " order by result_id DESC").first()
		temp.append(total + 1)
		temp.append(correct_answer)
		temp.append(user_answer[4])
		if user_answer[5] == 1:
			temp.append("Correct")
			correct_counter += 1
		if user_answer[5] == 0:
			temp.append("Incorrect")
		total += 1
		results.append(temp)
	quiz_info = (db.session.execute('Select * from Quiz where quiz_id == ' + str(quiz_id))).first()
	return render_template("./quiz_results.html",results = results, correct_counter = correct_counter, total = total,quiz_info = quiz_info)

#-----------------------------------------------------------------------------------------------------
#--------------------------------------------ADMIN PAGES----------------------------------------------
#-----------------------------------------------------------------------------------------------------
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
		temp_link = "https://www.youtube.com/embed/" + ((str(form.youtube_link.data[17:])).strip()) + "?start=" + ((str(form.start_time.data)).strip())
		question = Question(quiz_id = quiz_id, youtube_link = temp_link, duration = form.duration.data, correct_answer = form.correct_answer.data, option_1 = form.option_1.data, option_2 = form.option_2.data, option_3 = form.option_3.data)
		db.session.add(question)
		db.session.commit()
		if form.add_question.data:
			flash("Successfully added question")
			return redirect(url_for('create_question',quiz_id = quiz_id))
		elif form.finalise.data:
			return redirect(url_for('finalise_quiz',quiz_id = quiz_id))
	return render_template('./admin/create_question.html',form = form)

@app.route('/admin/review_quiz/<int:quiz_id>')
def finalise_quiz(quiz_id):
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	quiz_info = db.session.execute('Select * from Quiz where quiz_id == ' + str(quiz_id))
	results = db.session.execute('Select * from Question where quiz_id == ' + str(quiz_id))
	return render_template('./admin/view_questions.html',title= str(quiz_id) + ' Questions',quiz_info = quiz_info,results = results)
	
