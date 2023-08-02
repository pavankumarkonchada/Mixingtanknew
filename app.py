#importing web application related modules
#import flask
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inputpage.html', title='My Flask App')
