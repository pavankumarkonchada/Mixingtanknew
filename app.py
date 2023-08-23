#importing web application related modules
#import flask
from flask import Flask, render_template, request,jsonify
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import sys
import os
import subprocess
import logging
import requests
import socket
from requests.auth import HTTPBasicAuth
import paramiko
#import azure.functions as func
#import logging
print("Current working directory:", os.getcwd())

log_file_path = os.path.join(os.getcwd(), 'app.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO)


# Add the 'lib' folder to the Python path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
sys.path.append(lib_path)
subfolder_path = os.path.join(lib_path, 'pymapdl')
sys.path.append(subfolder_path)

from lib.constants import *
import lib.pymapdl.remote_bimetallic

app = Flask(__name__)
app.config["DEBUG"] = True
cwd = os.getcwd()
app.config["ALLOWED_EXT_GEOM"]=["STP","STL","SCDOC","X_T","STEP"]


def geomext(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_EXT_GEOM"]:
        return True
    else:
        return False

def pyFluent(boundary,growth,cores,flow,mesh,files,wd,out,in1,in2,imp):  
    print("entering the function")
    lib.pymapdl.remote_bimetallic.solve_mix(boundary,growth,cores,flow,mesh,files,wd,out,in1,in2,imp)





    
    # Download files from Blob Storage and transfer to VM
    


@app.route("/", methods=['POST'])

#def index():
    #vm_ip = "20.163.248.81:3389"  # Replace with the actual IP address of your Azure VM
    #response = ping_vm(vm_ip)
   
    #return render_template('index.html', response=response)

def process_file():
    try:
        # Read user input from the HTML form
        input_value = 1.2
        
        # Read the file from the GitHub repository
        github_file_url = 'https://github.com/pavankumarkonchada/Mixingtanknew/blob/main/lib/pymapdl/mixing_tank_pyfluent.py'
        response = requests.get(github_file_url)
        github_file_content = response.text
        
        # Modify the content based on user input
        modified_content = github_file_content.replace('max_size',str(input_value))
        print("Runninga adfajspdfj kajsfpaksdjf")
        # Send the modified content to the VM through API
        vm_api_url = 'http://20.163.248.81:3389/api/endpoint'
        vm_api_data = {'content': modified_content}
        response = requests.post(vm_api_url, json=vm_api_data)
        
        return jsonify({"status": "success", "message": "File modified and sent to VM successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
         

if __name__ == '__main__':   
    app.run(host='0.0.0.0',debug=True)    
