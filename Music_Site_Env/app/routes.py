from flask import render_template
from app import app
@app.route('/')
def index():
    return "Hello world"
@app.route('/test')
def test():
    data = {}
    return render_template('sql_test_page.html',title='Test',data = data)
