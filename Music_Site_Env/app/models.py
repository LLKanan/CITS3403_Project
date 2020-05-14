from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
	user_id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(128), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	results = db.relationship('Results', backref = 'user', lazy= 'dynamic')
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	def get_id(self):
		return self.user_id
	def __repr__(self):
		return '<User {}>'.format(self.username)

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key = True) 
    quiz_name = db.Column(db.String(128), index = True)
    quiz_image = db.Column(db.String(256), index = True)
    hidden = db.Column(db.Boolean)
    question = db.relationship('Question', backref = 'quiz', lazy = 'dynamic')
    results = db.relationship('Results', backref = 'quiz', lazy = 'dynamic')
    def __repr__(self):
        return '<Quiz {}>'.format(self.quiz_name)

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key = True, index = True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    youtube_id = db.Column(db.String(256)) 
    duration = db.Column(db.Integer)
    correct_answer = db.Column(db.String(256))
    option_1 = db.Column(db.String(256))
    option_2 = db.Column(db.String(256))
    option_3 = db.Column(db.String(256))
    start_time = db.Column(db.Integer)
    results = db.relationship('Results', backref = 'question', lazy= 'dynamic')
    def __repr__(self):
        return '<Question {}'.format(self.correct_answer)

class Results(db.Model):
    result_id = db.Column(db.Integer, primary_key = True, index= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    user_answer = db.Column(db.String(256))
    correct = db.Column(db.Boolean)
    def __repr__(self):
        return '<Results {}'.format(self.correct)

class finalResults(db.Model):
	final_result_id = db.Column(db.Integer, primary_key = True, index = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
	total_correct = db.Column(db.Integer)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
