#importing web application related modules
#import flask
from flask import Flask, render_template, request
import lib.pymapdl.remote_bimetallic
from lib.constants import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inputpage.html', title='My Flask App')
