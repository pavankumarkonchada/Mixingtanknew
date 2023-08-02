#importing web application related modules
#import flask
from flask import Flask, render_template, request
#importing file copying module
#import os as os
#numpy module

# import project specific files
import lib.pymapdl.remote_bimetallic
from lib.constants import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inputpage.html', title='My Flask App')
