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
    inlet_press=0.
    shear_int=0.
    
    image = ''

    #these flag variables are used to identify if the solution has run or not
    flag = ''
    flag2=''
        return render_template('inputpage.html',
                           Flag = 0,
                           SolveStatus='Solved',
                           output_image_url=image,
                           L2=my_boundary,
                           t2=my_growth,
                           E21=my_cores,
                           E22=my_flow,
                           c21=my_meshsize,
                           Flag2=flag2,
                           ip=inlet_press,
                           ws=shear_int,
                           C1=out_len,
                           C11=in1_len,
                           C111=in2_len,
                           C1111=imp_rad)
