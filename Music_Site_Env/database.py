#Initialise database
from app import db
from app.models import User,Quiz,Question,Results
admin = User(user_id = 0, username = 'admin', email = 'admin@admin.com')
admin.set_password('admin')
db.session.add(admin)
db.session.commit()
