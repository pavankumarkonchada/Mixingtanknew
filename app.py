#importing web application related modules
#import flask
from flask import Flask, render_template, request
#importing file copying module
#import os as os
#numpy module

# import project specific files
import lib.pymapdl.remote_bimetallic
from lib.constants import *

#an app instance is opened using variable app
app = Flask(__name__)




#defining the app extension (This case has just '/', meaning this is the main domain)
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


    
    if request.method == 'POST' :



        #checks if the file uploaded has a valid filename,valid extension or not
        if request.files:

                print("file needs to have valid name")

            imp_rad= float(request.form.get('impellerradius'))
            
        else:
            print("method is not post")



    #sends the variables that need to be accesed by HTML code to the HTML code 'inputpage.html'
    return render_template('inputpage.html',
                           Flag = flag,
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


if __name__ == '__main__':
    app.run(host='0.0.0.0',passthrough_errors=True,use_reloader=False,port=5000)

