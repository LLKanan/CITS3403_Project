from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField,SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User,Quiz,Question,Results,finalResults

#Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#Registration Form
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password', message='Passwords must match, please try again')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username = str(username.data).strip()).first()
		if user is not None:
			raise ValidationError('Username is already taken, try a different Username.')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError('Email address already in use, try a different email address.')

#Quiz Creation Form
class CreateQuizForm(FlaskForm):
	name = StringField('Quiz Name', validators = [DataRequired()])
	image = StringField('Image_URL', validators = [DataRequired()])
	submit = SubmitField('Create Questions')
	
	def validate_name(self, name):
		query = Quiz.query.filter_by(quiz_name = str(name.data).strip()).filter_by(hidden = 0).first()
		if query is not None:
			raise ValidationError('Sorry this quiz name is already taken. Try a different quiz name.')

#Question Creation form
class CreateQuestionForm(FlaskForm):
	youtube_link = StringField('Youtube Video Link', validators = [DataRequired()])
	start_time = IntegerField('Video Start Time in seconds', validators = [DataRequired()])
	duration = IntegerField('Playtime in seconds', validators = [DataRequired()])
	correct_answer = StringField('Correct Option', validators = [DataRequired()])
	option_1 = StringField('Multiple Choice option 2', validators = [DataRequired()])
	option_2 = StringField('Multiple Choice option 3', validators = [DataRequired()])
	option_3 = StringField('Multiple Choice option 4', validators = [DataRequired()])
	add_question = SubmitField('Add question')

#User Question Form
class QuestionForm(FlaskForm):
	answer = SelectField("Select answer")
	submit_answer = SubmitField('Next Question')
	#previous_question = SubmitField('Previous Question')
	def set_options(self, option_list):
		self.answer.choices = option_list
	def validate_answer(self, answer):
		if answer == None:
			raise ValidationError('Failed to select answer.')

