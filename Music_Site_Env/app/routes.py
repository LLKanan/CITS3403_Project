from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateQuizForm, CreateQuestionForm, QuestionForm
from app.models import User,Quiz,Question,Results,finalResults
from flask_login import login_required, current_user, login_user, logout_user
import random

@app.route('/')
@app.route('/index')
@login_required
#Default Home page
def index():
	#Redirect if admin
	if current_user.get_id() == 0:
			return redirect(url_for('admin_home'))
	return render_template('index.html', title = 'Home')

#Login Page
@app.route('/login', methods = ['GET', 'POST'])
def login():
	#Redirect to home page if user is already logged in 
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	#Redirect to previous page if available otherwise home page on successful login
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		if current_user.get_id() == 0:
			return redirect(url_for('admin_home'))
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html', title = 'Sign in', form = form)

#Logout redirects to home page and logs user out
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

#Registration page
@app.route('/register',methods=['GET', 'POST'])
def register():
	#If user is logged in redirect to home page
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	#If registration form is valid flash message and redirect to login page
	if form.validate_on_submit():
		user = User(username=str(form.username.data).strip(), email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Congratulations, you're now a registered user!")
		return redirect(url_for('login'))
	return render_template('register.html', title='Registration page', form = form)

#Avaialble Quizzes page
@app.route('/view_quizzes',methods=['GET', 'POST'])
@login_required
def view_quizzes():
	results = db.session.execute('Select * from Quiz where hidden == 0').fetchall()
	user_id = current_user.get_id()
	completed_list = (db.session.execute("Select * from final_results where user_id = " + str(user_id))).fetchall()
	temp_list = []
	#Only display quizzes that the user hasn't obtained a final result for
	for completed in completed_list:
		temp_list.append(int(completed[2]))
	counter = 0
	while counter < len(results):
		if int(results[counter][0]) in temp_list:
			print("pop")
			results.pop(counter)
			counter -= 1
		counter += 1
	return render_template('./view_quizzes.html',title='View Quizzes',results = results)

#Function to update/add an answer to a question to the result database
def submit_answer(quiz_id,question_list,user_answer,current_question):
	check = (db.session.execute('Select * from final_results where quiz_id == ' + str(quiz_id) + ' and user_id == '+ str(current_user.get_id()))).first()
	#Check that the user hasn't already completed the quiz and is cheating
	if check == None:
		result = Results.query.filter_by(question_id = question_list[current_question][0]).filter_by(user_id = current_user.get_id()).first()
		#Check to see if we're updating an existing answer
		if result != None:
			result.user_answer = user_answer
			if(user_answer == question_list[current_question][4]):
				result.correct = True
			else:
				result.correct = False
		#Otherwise create a new "result"
		else:
			result = Results(user_id = current_user.get_id(), quiz_id = quiz_id,question_id = question_list[current_question][0], user_answer = user_answer, correct = (True if (user_answer == question_list[current_question][4]) else False))
			db.session.add(result)	
		db.session.commit()

#Question page
@app.route('/start_quiz/<int:quiz_id>/<current_question>',methods=['GET', 'POST'])
@login_required
def start_quiz(quiz_id,current_question):
	form = QuestionForm()
	current_question = int(current_question)
	question_list = (db.session.execute('Select * from Question where quiz_id ==' + str(quiz_id) + " ORDER BY question_id")).fetchall()
	quiz_name = (db.session.execute('Select * from Quiz where quiz_id ==' + str(quiz_id))).first()	
	temp_list = question_list[current_question][4:8]
	user_id = str(current_user.get_id())
	saved_answers = (db.session.execute('Select * from results where question_id == ' + str(question_list[current_question][0]) + ' and user_id == ' + user_id)).first()
	option_list = []
	random_int = random.randrange(0,4)
	#Load the previous answer if it exists and randomise the other answers order
	if saved_answers == None:
		option_list.append((None,"Select Answer"))
		for counter in range(len(temp_list)):
			option = temp_list[((random_int + counter) % 4)]
			option_list.append((option,option))
	#Otherwise create a list of answers and randomise order
	else:
		option_list.append((saved_answers[4],saved_answers[4]))	
		for counter in range(len(temp_list)):
			option = temp_list[((random_int + counter) % 4)]
			if option == saved_answers[4]:
				continue
			option_list.append((option,option))
	form.set_options(option_list)
	#If user submits a valid answer load next question
	if form.validate_on_submit():
		submit_answer(quiz_id,question_list,form.answer.data,current_question)
		if form.submit_answer.data:
			if current_question + 1 < len(question_list):
				return redirect(url_for('start_quiz',quiz_id = quiz_id, current_question = current_question + 1))
			else:
				return redirect(url_for('quiz_results',quiz_id = quiz_id))
	return render_template('./question_page.html', title = quiz_name[1], question_list = question_list,current_question = current_question, quiz_name = quiz_name[1], form = form, quiz_id = quiz_id)

#Function to submit a user's final results for a quiz
def submit_final_results(quiz_id,user_id,correct_counter):
	check = (db.session.execute('Select * from final_results where quiz_id == ' + str(quiz_id) + ' and user_id == '+ str(user_id))).first()
	#Check to ensure that the user isn't cheating and reattempting a quiz they've already completed
	if check == None:
		#print("new result",str(quiz_id))
		finalResult = finalResults(user_id = user_id,quiz_id = quiz_id,total_correct = correct_counter)
		db.session.add(finalResult)
		db.session.commit()	

#Results page after a user completes a quiz
#Shows correct answer, user's answers and whether they got them correct/wrong
@app.route('/quiz_results/<quiz_id>',methods = ['GET','POST'])
@login_required
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
	if int(quiz_id) != 0:
		submit_final_results(quiz_id,user_id,correct_counter)
	return render_template("./quiz_results.html",results = results, correct_counter = correct_counter, total = total,quiz_info = quiz_info)

#Results page that lists all the quizzes a user has attempted
#Redirects to admin/view_answers to show user's results
@app.route('/my_results')
@login_required
def my_results():
	user_id = current_user.get_id()
	#listQuizzes = db.session.execute('Select * from Quiz').fetchall()
	listResults = (db.session.execute('Select * from final_results where user_id == ' + str(user_id))).fetchall()
	userResults = []
	for result in listResults:
		temp = []
		quiz_info = (db.session.execute('Select * from Quiz where quiz_id == ' + str(result[2]))).first()
		temp.append(result[2])#Quiz id
		temp.append(quiz_info[1])#Quiz name
		temp.append(quiz_info[2])#Quiz image
		temp.append(result[3])#Number correct
		userResults.append(temp)
	return render_template('./my_results.html',title= "My Results",results = userResults)

#-----------------------------------------------------------------------------------------------------
#--------------------------------------------ADMIN PAGES----------------------------------------------
#-----------------------------------------------------------------------------------------------------
#Admin home page
@app.route('/admin/home')
def admin_home():
	#Ensure that only admin has access
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	return render_template('./admin/home.html', title = 'Admin HomePage')

#Admin manage users page
#Shows all users and gives option to remove user
@app.route('/admin/manage_users',methods=['GET', 'POST'])
def manage_users():
	#Ensure that only admin has access
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	results = db.session.execute('Select * from user where user_id != 0')
	return render_template('./admin/manage_users.html',title='Manage Users',results = results)

#Function to remove user redirects to manage users page
@app.route('/admin/manage_users/remove/<int:user_id>')
def remove_user(user_id):
	#Ensure that only admin can access this function
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	#Ensure that we don't remove the admin
	if user_id == 0:
		flash('Cannot Remove Admin, redirecting to userlist')
		return redirect(url_for('manage_users'))
	#Check is user exists if it does remove them
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

#Admin manage quizzes page
#Allows an admin to hide/remove a quiz
@app.route('/admin/manage_quizzes',methods=['GET', 'POST'])
def manage_quizzes():
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	results = db.session.execute('Select * from Quiz')
	return render_template('./admin/manage_quizzes.html',title='Manage Quizzes',results = results)

#Hide quiz function
#Allows admin to hide a quiz redirects to updated quiz page
@app.route('/admin/manage_quizzes/hide/<int:quiz_id>')
def hide_quiz(quiz_id):
	#Ensure that only admin has acces to this page
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	#Check to ensure that the quiz exists
	query = 'Select * from quiz where quiz_id == ' + str(quiz_id)
	temp_quiz = db.session.execute(query)
	if temp_quiz:
		quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
		#Swaps hidden value to opposite value
		if(quiz.hidden == 1):
			check = Quiz.query.filter_by(quiz_name = quiz.quiz_name).filter_by(hidden = False).first()
			#Check to make sure we make sure another quiz with the same name isn't already visible
			if check != None:
				flash("ERROR: Quiz_ID #{quiz_id} can't be toggled visible as there is another quiz with the same name that is currently visible".format(quiz_id = quiz_id))
				return redirect(url_for('manage_quizzes'))
			quiz.hidden = 0
		else:
			quiz.hidden = 1
			flash("Quiz_ID #{quiz_id} was succesfully hidden".format(quiz_id = quiz_id))
		db.session.commit()
		return redirect(url_for('manage_quizzes'))
	else:
		flash("Error couldn't find #{quiz_id}, redirecting to quiz list".format(quiz_id = quiz_id))
		return redirect(url_for('manage_quizzes'))

#Remove quiz function
#Redirects to quiz page
@app.route('/admin/remove_quizzes/hide/<int:quiz_id>')
def remove_quiz(quiz_id):
	#Ensure that only admin has access to this function
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	#Ensure that the quiz exists
	query = 'Select * from quiz where quiz_id == ' + str(quiz_id)
	temp_quiz = db.session.execute(query)
	if temp_quiz:
		#Remove all questions related to quiz
		while Question.query.filter_by(quiz_id = quiz_id).first() != None:
			db.session.delete(Question.query.filter_by(quiz_id = quiz_id).first())
			db.session.commit()
		#Remove all results related to quiz
		while Results.query.filter_by(quiz_id = quiz_id).first() != None:
			db.session.delete(Results.query.filter_by(quiz_id = quiz_id).first())
			db.session.commit()
		#Remove all finalised results related to quiz
		while finalResults.query.filter_by(quiz_id = quiz_id).first() != None:
			db.session.delete(finalResults.query.filter_by(quiz_id = quiz_id).first())
			db.session.commit()
		#Remove quiz
		while Quiz.query.filter_by(quiz_id = quiz_id).first() != None:
			db.session.delete(Quiz.query.filter_by(quiz_id = quiz_id).first())
			db.session.commit()
		flash("Quiz_ID #{quiz_id} was succesfully removed".format(quiz_id = quiz_id))
		return redirect(url_for('manage_quizzes'))
	else:
		flash("Error couldn't find #{quiz_id}, redirecting to quiz list".format(quiz_id = quiz_id))
		return redirect(url_for('manage_quizzes'))

#Admin create quiz page
@app.route('/admin/create_quiz',methods=['GET', 'POST'])
def create_quiz():
	#Ensures that only admin has access to this page
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	form = CreateQuizForm()
	#If all values valid, create new quiz and redirect to question creation process
	if form.validate_on_submit():
		quiz = Quiz(quiz_name = str(form.name.data).strip(),quiz_image = form.image.data, hidden = 1)
		db.session.add(quiz)
		db.session.commit()
		#Placeholder for linking to creating questions in a quiz
		#flash("Congratulations, you've successfully added a quiz!")
		return redirect(url_for('create_question',quiz_id = quiz.quiz_id))
	return render_template('./admin/create_quiz.html',title = 'Create new Quiz',form = form)

#Admin Create question page
@app.route('/admin/create_quiz/<int:quiz_id>',methods=['GET', 'POST'])
def create_question(quiz_id):
	#Ensures that only an admin has access to this page
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	form = CreateQuestionForm()
	#If the values are valid creates a question
	if form.validate_on_submit():
		youtube_id = str(form.youtube_link.data[17:]).strip()
		question = Question(quiz_id = quiz_id, youtube_id = youtube_id, start_time = form.start_time.data, duration = form.duration.data, correct_answer = form.correct_answer.data, option_1 = form.option_1.data, option_2 = form.option_2.data, option_3 = form.option_3.data)
		db.session.add(question)
		db.session.commit()
		flash("Successfully added question")
		return redirect(url_for('create_question',quiz_id = quiz_id))
	return render_template('./admin/create_question.html',form = form, quiz_id = quiz_id)

#Admin finalise quiz page
#When a quiz is finalised admin is redirected to this page to view the completed quiz
@app.route('/admin/review_quiz/<int:quiz_id>')
def finalise_quiz(quiz_id):
	#Ensure that only admin has access to this page
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	quiz_info = Quiz.query.filter_by(quiz_id = quiz_id).first()
	quiz_info.hidden = 0
	db.session.commit()
	quiz_info = db.session.execute('Select * from Quiz where quiz_id == ' + str(quiz_id)).first()
	results = db.session.execute('Select * from Question where quiz_id == ' + str(quiz_id))
	return render_template('./admin/view_questions.html',title= str(quiz_id) + ' Questions',quiz_info = quiz_info,results = results)

#Admin manage answers page
#Allows admin to view all user's answers
#Lists them all as quizzes first
#After selecting a quiz we can view all the user's who've attempted this quiz
@app.route('/admin/manage_answers')
def manage_answers():
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	listQuizzes = db.session.execute('Select * from Quiz')
	return render_template('./admin/manage_answers.html',title='Manage Quizzes',results = listQuizzes)

#Admin manage answers page
#Allows admin to view all user's answers
#This page in particular allows us to view all the user's who've attempted this specific quiz_id and their final scores.
#From here we can select a user to view each of their answers to each question
@app.route('/admin/manage_answers/<quiz_id>')
def manage_answer_quiz(quiz_id):
	if current_user.get_id() != 0:
		flash("You don't have access to this page")
		return redirect(url_for('index'))
	quizName = db.session.execute('Select * from Quiz where quiz_id == ' + str(quiz_id)).first()
	listResults = (db.session.execute('Select * from final_results where quiz_id == ' + str(quiz_id))).fetchall()
	results = []
	for result in listResults:
		temp = []
		user_id = result[1]
		userName = (db.session.execute('Select * from user where user_id == ' + str(user_id))).first()
		mark = result[3]
		temp.append(user_id)
		temp.append(userName[1])
		temp.append(mark)
		results.append(temp)
	return render_template('./admin/user_results.html',title = str(quizName[1]) + ' Results', results = results,quiz_id = quiz_id)

#Admin manage answers page
#This page displays all the user's answers based on the quiz and user_id selected earlier
@app.route('/admin/<quiz_id>/<user_id>')
def view_answers(quiz_id,user_id):
	if current_user.get_id() != 0 :
		if (int(current_user.get_id()) != int(user_id)):
			print(user_id,current_user.get_id())
			flash("You don't have access to this page")
			return redirect(url_for('index'))
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
	return render_template("./admin/user_answers.html",results = results, correct_counter = correct_counter, total = total,quiz_info = quiz_info)

