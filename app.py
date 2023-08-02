#importing web application related modules
#import flask
from flask import Flask, render_template, request
import sys
import os

# Add the 'lib' folder to the Python path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
sys.path.append(lib_path)
import lib.pymapdl.remote_bimetallic
from lib.constants import *


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inputpage.html', title='My Flask App')
