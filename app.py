#importing web application related modules
#import flask
from flask import Flask, render_template, request
import sys
import os

# Add the 'lib' folder to the Python path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
sys.path.append(lib_path)
subfolder_path = os.path.join(lib_path, 'pymapdl')
sys.path.append(subfolder_path)

from lib.constants import *


app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])

def calculator():  
    # These are the default values that are shown in the website in place of the variables to be entered
    my_file='folder'
    my_boundary = 4
    my_growth = 1.2
    my_cores = 8
    my_flow = 0.5
    my_meshsize = 0.8
    out_len = 20
    in1_len = 30
    in2_len = 30
    imp_rad = 20
    rslt_img= r"pavankumarkonchada\Mixingtanknew\static\default_img.png"
    inlet_press=0.
    shear_int=0.
    
    image = ''

    #these flag variables are used to identify if the solution has run or not
    flag = ''
    return render_template('index.html', title='My Flask App')
