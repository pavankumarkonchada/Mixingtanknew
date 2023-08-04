#importing web application related modules
#import flask
from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import sys
import os
import logging
import requests
from requests.auth import HTTPBasicAuth
print("Current working directory:", os.getcwd())

log_file_path = os.path.join(os.getcwd(), 'app.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

# Add the 'lib' folder to the Python path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
sys.path.append(lib_path)
subfolder_path = os.path.join(lib_path, 'pymapdl')
sys.path.append(subfolder_path)

from lib.constants import *


app = Flask(__name__)
app.config["DEBUG"] = False
cwd = os.getcwd()
app.config["ALLOWED_EXT_GEOM"]=["STP","STL","SCDOC","X_T","STEP"]
connect_str = f"DefaultEndpointsProtocol=https;AccountName=trailmixin;AccountKey=3SVrdfhrb+3zp8yJgMsvbBS7xACbuoSH/Mh+/Cz/eRUWVZH0mBYbaSMxqBfEeAcsmKbWMavId984+AStJrMV5g==;EndpointSuffix=core.windows.net" # retrieve the connection string from the environment variable
container_name = "mixstore" # container name in which images will be store in the storage account
print("Connection String:", connect_str)


blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
def retrieve_image_from_remote_server(server_ip, file_path, username, password):
    url = f"http://{server_ip}/{file_path}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), stream=True)
    return response

def geomext(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_EXT_GEOM"]:
        return True
    else:
        return False

def pyFluent(boundary,growth,cores,flow,mesh,files,wd,out,in1,in2,imp):  
    lib.pymapdl.remote_bimetallic.solve_mix(boundary,growth,cores,flow,mesh,files,wd,out,in1,in2,imp)



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
    wkdir= ''
    server_ip = "192.168.12.221"  # Replace with the IP address of the remote server
    file_path = "E:/Drp/Pressure.png"  # Replace with the actual file path on the remote server
    username = "pavan"  # Replace with the actual username for authentication
    password = "cadfem1"  # Replace with the actual password for authentication
    response = retrieve_image_from_remote_server(server_ip, file_path, username, password)
    if response.status_code == 200:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob='Pressure.png')
        blob_client.upload_blob(response.content)
        return "Image uploaded successfully."
    return "Image retrieval failed."

# Create a connection to Azure Blob Storage
    #block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)
    if request.method == 'POST' :

        #The location where the inputs have to be stored is obtained from the user, folder with same name is created
        path = os.getcwd()

        string=request.form["folder"]
        new_wdir_path = os.path.join(path,string)
        if not os.path.exists(new_wdir_path):
            print("folder doesn't exist")
            os.mkdir(new_wdir_path)
        #Prints the user input folder
        print(new_wdir_path)
        #prints the file name uploaded
        print(request.files)

        #checks if the file uploaded has a valid filename,valid extension or not
        if request.files:
            firstfile=request.files["geomfile"]
            if firstfile.filename=="":
                print("file needs to have valid name")
                return "<h1 style='color:red'>ERROR:invalid filename!</h1>"
            
            if not geomext(firstfile.filename):
                print("upload geometry file with proper extension")
                return "<h1 style='color:red'>ERROR: invalid geometry extension!</h1>"
            
            #saves the user uploaded file to the user uploaded location
            firstfile.save(os.path.join(new_wdir_path, firstfile.filename))
            wkdir=os.path.join(new_wdir_path, firstfile.filename)
            
            #All the inputs provided by the user are obtained and stored in variables
            my_boundary = float(request.form.get('boundary'))
            my_growth = float(request.form.get('growth'))
            my_cores = float(request.form.get('cores'))
            my_flow = float(request.form.get('flow'))
            my_meshsize = float(request.form.get('meshsize'))
            out_len= float(request.form.get('outlen'))
            in1_len= float(request.form.get('in1len'))
            in2_len= float(request.form.get('in2len'))
            imp_rad= float(request.form.get('impellerradius'))
            
        else:
            print("method is not post")
    
    #these flag variables are used to identify if the solution has run or not
    flag = ''
    flag2=''
    return render_template('inputpage.html',
                           Flag = 0,
                           SolveStatus='Solved',
                           L2=my_boundary,
                           t2=my_growth,
                           E21=my_cores,
                           E22=my_flow,
                           c21=my_meshsize,
                           Flag2=0,
                           ip=inlet_press,
                           ws=shear_int,
                           C1=out_len,
                           C11=in1_len,
                           C111=in2_len,
                           C1111=imp_rad)
if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True,port=8000)    
