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

#current working direcory is stored in variable cwd
cwd = os.getcwd()

#list to define allowed geometry file extensions
app.config["ALLOWED_EXT_GEOM"]=["STP","STL","SCDOC","X_T","STEP"]

#function to check if the extension of the file uploaded is matching the allowed extensions
def geomext(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_EXT_GEOM"]:
        return True
    else:
        return False

#Function that calls the python code that is used to transfer, run the applications required to get solution
def pyFluent(boundary,growth,cores,flow,mesh,files,wd,out,in1,in2,imp):
    
    lib.pymapdl.remote_bimetallic.solve_mix(boundary,growth,cores,flow,mesh,files,wd,out,in1,in2,imp)


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


    image = ''

    #these flag variables are used to identify if the solution has run or not
    flag = ''
    flag2 = ''

    #variable declaration for variable wkdir
    wkdir= r'pavankumarkonchada\Mixingtanknew\geometry-sample\artery.scdoc'
    if request.method == 'POST' :

        #The location where the inputs have to be stored is obtained from the user, folder with same name is created
        path = os.getcwd()
        #the user input folder name is obtained using request.form
        string=request.form["folder"]
        new_wdir_path = os.path.join(path,string)
        if not os.path.exists(new_wdir_path):
            print("folder doesn't exist")
            #directory is created if not already present
            os.mkdir(new_wdir_path)
        
        #Prints the user input folder
        print(new_wdir_path)
        #prints the file name uploaded
        print(request.files)

        #checks if the file uploaded has a valid filename,valid extension or not
        if request.files:
            firstfile=request.files["geomfile"]
            print(firstfile)
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

        #calls the function which is responsible for running all the applications    
        pyFluent(my_boundary,my_growth,my_cores,my_flow,my_meshsize,wkdir,new_wdir_path,out_len,in1_len,in2_len,imp_rad)
        
        #opens the text file which contains all the outputs from the fluent run (right now it is based on the assumption that there are only 2 numerical values separated by a comma)
        #text file with result is opened in read mode
        file=open("pavankumarkonchada\Mixingtanknew\myfile.txt","r")
        #contents of the file are stored in variable post
        post=file.readline()
        postproc=[0,0]
        #the values inside the file are stored in a list variable named postproc
        postproc[0]=post.rsplit(",")[0]
        postproc[1]=post.rsplit(",")[1]
        #the result values are printed
        print(postproc[0])
        print(postproc[1])
        #file opened in read mode is closed
        file.close()
        
        #Prints RUN_COMPLETE to show that the run is complete
        print(RUN_COMPLETE)

        #the results are stored into inlet_press and sheat _int
        inlet_press=postproc[0]
        shear_int=postproc[1]
        print(shear_int)
        
        #Flag variables are updated once run is finished
        flag = 1
        flag2=1

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

#host='0.0.0.0' means that the web application is hosted on all systems in the local network
#passthrough_errors=True and use_reloader=False are very important, they are used to deactivate workzeug which looks for any changes in the code and reloads the web application
#this leads to unwanted errors when using subprocess.call() function or time.sleep() function
if __name__ == '__main__':
    app.run(host='0.0.0.0',passthrough_errors=True,use_reloader=False,port=5000)

