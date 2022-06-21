from flask import render_template
from app import app

@app.route('/')
def home():
    return "<b>There s been a change</b>"

@app.route('/template')
def template():
    return render_template('home.html')