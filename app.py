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
@app.route("/")
def calculator():  
    return render_template('inputpage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',passthrough_errors=True,use_reloader=False,port=5000)
