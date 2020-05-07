#Initialise database
from app import db
from app.models import User,Quiz,Question,Results
admin = User(username = 'admin', email = 'admin@admin.com', points = 0)
admin.set_password('admin')
db.session.add(admin)
db.session.commit()
