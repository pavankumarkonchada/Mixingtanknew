import os

import shutil
import paramiko
import subprocess

# code works by creating a copy of all the pre-existing script files present in their respective places and replaces the user input variables in the required places,
# this is then transfered to the remote machine and the files are executed in the remote location
# following this the result is stored in the form of contours and a text file
# These are then transfered to the local machine and then integrated into the web app

def solve_mix(boundarylayers_auto,growthrate_auto,noofcores_auto,waterflowrate_auto,meshsize_auto,my_wdirnew,wd,out_len,in1_len,in2_len,imp_rad):
    # variables required for the simulation are obtained from app.py
    boundarylayers_auto=boundarylayers_auto
    growthrate_auto=growthrate_auto
    noofcores_auto=noofcores_auto
    waterflowrate_auto=waterflowrate_auto
    meshsize_auto=meshsize_auto
    my_wdirnew= my_wdirnew
    imp_rad=imp_rad
    out_len=out_len
    in1_len=in1_len
    in2_len=in2_len

    #The remote file path where the geometry file should be transfered is defined
    #The path C:\check\geom.scodoc must me replaced in the place of filename in scapceclaim script
    #remote_file_path_goem is needed to define where input geometry must be transferred to in the remote machine
    #remote_file_path_goem2 is needed to replace "filename" with a raw string defining the location from where the spaceclaim script must read the geometry in the remote machine
    remote_file_path_geom = r'C:\check\geom.scdoc'
    remote_file_path_geom2 = "r"+'"'+r'C:\check\geom.scdoc'+'"'

    #The geometry file is saved in this location after the modifications have been done as per the spaceclaim script
    geom_dst2="r"+'"'+r"C:\check\geom1.scdoc"+'"'



    #making a copy and replacing variables with values given by user in pyfluent file
    original = r'O:\Mixing_tank_py_web_app\lib\pymapdl\mixing_tank_pyfluent.py'
    target = r'O:\Mixing_tank_py_web_app\lib\pymapdl\mixing_tank_pyfluent1.py'
    #shutil simply makes a copy at the target location
    shutil.copyfile(original, target)

    file_path= r"O:\Mixing_tank_py_web_app\lib\pymapdl\mixing_tank_pyfluent1.py"
    #the places where the text on the pyfluent file needs to be swapped out with user input is stored in dictionaries
    variable_values={'max_size':float(meshsize_auto),'growth_rate_bl':float(growthrate_auto),'in_vel':float(waterflowrate_auto)}
    variable_str={'import_filename':geom_dst2}
    variable_int={'total_no_of_layers':int(boundarylayers_auto),'process_count':int(noofcores_auto)}
    #The pyfluent file is opened in read mode 
    file=open(file_path, 'rt')
    #the contents of the pyfluent file are stored in the variable file_contents
    file_contents=file.read()
    #the text which needs to be swapped out in the pyfluent file is swapped
    for variable,value in variable_values.items():
        file_contents = file_contents.replace(variable, str(value))

    for variable,value in variable_int.items():
        file_contents = file_contents.replace(variable, str(value))


    for variable,value in variable_str.items():
        file_contents = file_contents.replace(variable,str(value))
    #file opened in read mode is closed
    file.close()
    #the file is opened in write mode
    file=open(file_path, 'wt')
    #the modified contects stored in the variable file_contents is written to the file
    file.write(file_contents)
    #file opened in write mode is closed
    file.close()
    #end of block


    #making a copy and replacing variables with values given by user in correcting spaceclaim script
    original_sc = r'O:\Mixing_tank_py_web_app\spaceclaim_script1.py'
    target_sc = r'O:\Mixing_tank_py_web_app\spaceclaim_script2.py'
    #shutil simply makes a copy at the target location
    shutil.copyfile(original_sc, target_sc)

    file_path_sc= r"O:\Mixing_tank_py_web_app\spaceclaim_script2.py"
    #the places where the text on the spaceclaim script needs to be swapped out with user input is stored in dictionaries
    variable_string={'filename':remote_file_path_geom2, 'dest':geom_dst2}
    variable_number={'outlet_length':out_len,'inlet2_length':in2_len,'inlet1_length':in1_len,'Impeller_radius':imp_rad}
    #The pyfluent file is opened in read mode 
    file_sc=open(file_path_sc, 'rt')
    #the contents of the spaceclaim script are stored in the variable file_contents_sc
    file_contents_sc=file_sc.read()
    #the text which needs to be swapped out in the spaceclaim script is swapped
    for variable,value in variable_string.items():
        file_contents_sc = file_contents_sc.replace(variable, str(value))

    for variable,value in variable_number.items():
        file_contents_sc = file_contents_sc.replace(variable, str(value))
    #file opened in read mode is closed
    file_sc.close()
    #the file is opened in write mode
    file_sc=open(file_path_sc, 'wt')
    #the modified contects stored in the variable file_contents_sc is written to the file
    file_sc.write(file_contents_sc)
    #file opened in write mode is closed
    file_sc.close()
    #end of block


    #making a copy and replacing variables with values given by user in correcting runwb file
    original_runwb = r'O:\Mixing_tank_py_web_app\run_wb1.py'
    target_runwb = r'O:\Mixing_tank_py_web_app\run_wb2.py'
    #shutil simply makes a copy at the target location
    shutil.copyfile(original_runwb, target_runwb)

    file_path_runwb= r"O:\Mixing_tank_py_web_app\run_wb2.py"
    remote_file_path_runwb="r"+'"'+r"C:\check\fluent_meshing.wbjn"+'"'
    #the places where the text on the workbench journal needs to be swapped out with user input is stored in dictionaries
    variable_runwb={'journal_loc':remote_file_path_runwb}
    #The workbench journal is opened in read mode 
    file_runwb=open(file_path_runwb, 'rt')
    #the contents of the spaceclaim script are stored in the variable file_contents_runwb
    file_contents_runwb=file_runwb.read()
    #the text which needs to be swapped out in the workbench journal is swapped
    for variable,value in variable_runwb.items():
        file_contents_runwb = file_contents_runwb.replace(variable, str(value))
    #file opened in read mode is closed
    file_runwb.close()
    #the file is opened in write mode
    file_runwb=open(file_path_runwb, 'wt')
    #the modified contects stored in the variable file_contents_runwb is written to the file
    file_runwb.write(file_contents_runwb)
    #file opened in write mode is closed
    file_runwb.close()
    #end of block

    # remote server details
    remote_host = '192.168.12.228'  #need to change as per the target system
    remote_username = 'hrithik'     #remote machine username
    remote_password = 'Cadfem@2022' #remote machine password
    # Specify the local path, path where pyfluent file will be saved in remote machine
    local_file_path = r'O:\Mixing_tank_py_web_app\lib\pymapdl\mixing_tank_pyfluent1.py'
    remote_file_path = r'C:\check\mixing_tank_pyfluent.py'
    #specifying the local path,  path where runwb file will be saved in remote machine
    local_file_path_runwb = r'O:\Mixing_tank_py_web_app\run_wb2.py'
    remote_file_path_runwb = r'C:\check\run_wb.py'
    #specifying the local path, path where journal file will be saved in remote machine
    local_file_path_jou = r'O:\Mixing_tank_py_web_app\fluent_meshing.wbjn'
    remote_file_path_jou = r'C:\check\fluent_meshing.wbjn'
    #specifying the local path, path where spaceclaim script will be saved in remote machine
    local_file_path_scscript = r'O:\Mixing_tank_py_web_app\spaceclaim_script2.py'
    remote_file_path_scscript = r'C:\check\spaceclaim_script.py'


    #Specifying the file path of geometry on the local file path (folder name given by user)
    local_file_path_geom = my_wdirnew

    # Create an SSH client and connect to the remote server
    ssh = paramiko.SSHClient()
    paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_host, username=remote_username, password=remote_password)

    # Transfer the local Python file,geometry file,workbench journal file, spaceclaim script to the remote server using sftp
    #sftp channel is opened
    sftp = ssh.open_sftp()
    sftp.put(local_file_path, remote_file_path)
    sftp.put(local_file_path_geom, remote_file_path_geom)
    sftp.put(local_file_path_runwb, remote_file_path_runwb)
    sftp.put(local_file_path_jou, remote_file_path_jou)
    sftp.put(local_file_path_scscript, remote_file_path_scscript)
    
    #Copying cxlayout file to local machine C-Drive to make fluent workspace window to hide console,
    #the cxlayout file is stored in C under username folder everytime one uses fluent. It stores information regarding the workspace layout
    #This is needed as fluent changes to tab switching layout by default when using pyfluent and default workspace layout must be enforced each time
    #this will be tricky during remote execution, where we do not know the username in the target_layout, will have to give a predetermined username and use sftp.put()
    original_layout = r'O:\Mixing_tank_py_web_app\fluent_layout\Default\.cxlayout.ini'
    target_layout = r'C:\Users\hrithik\.cxlayout.ini'
    shutil.copyfile(original_layout, target_layout)

    #printing to confirm if code is being read
    print("Files have been copied successfully")
    
    #command to execute Workbench journal to change the geometry and save it
    workbench_path=r"C:\Program Files\ANSYS Inc\v222\Framework\bin\Win64\RunWB2.exe"
    wb_journal_path=r'C:\check\fluent_meshing.wbjn'
    
    #The command to run the workbench journal is defined as a shell command and run using subprocess.call()
    command = f'"{workbench_path}" -B -R "{wb_journal_path}"'
    #subprocess.call() is used instead of subprocess.Popen() as the former waits for the command to finish executing before moving on to the next line while the latter doesn't    
    subprocess.call(command, shell=True)
   
    #if the geometry is present in the required location, the pyfluent code is run
    if os.path.exists(r"C:\check\geom1.scdoc"):
        #commands to change working directory and run the pyfluent code are written as shell commands and executed using subprocess.call()
        command = r"cd C:\check&&python C:\check\mixing_tank_pyfluent.py" 
        #subprocess.call() is used instead of subprocess.Popen() as the former waits for the command to finish executing before moving on to the next line while the latter doesn't
        subprocess.call(command, shell=True)
    
    #The text file with results from fluent run is transfered from remote machine to local machine using sftp.get()
    remote_txt=r"C:\check\result.txt"
    local_txt=r"O:\Mixing_tank_py_web_app\myfile.txt"
    sftp.get(remote_txt, local_txt)

    #Image of pressure contour is transfered from remote machine to local machine using sftp.get()
    remote_press=r"C:\check\pressure.png"
    local_press=r"O:\Mixing_tank_py_web_app\static\pressure.png"
    sftp.get(remote_press, local_press)

    #Image of velocity plot is transfered from remote machine to local machine using sftp.get()
    remote_vel=r"C:\check\vel_plot.png"
    local_vel=r"O:\Mixing_tank_py_web_app\static\vel_plot.png"
    sftp.get(remote_vel, local_vel)

    #Image of q-criteria contour is transfered from remote machine to local machine using sftp.get()
    remote_press=r"C:\check\Q-criteria.png" 
    local_press=r"O:\Mixing_tank_py_web_app\static\Q-criteria.png"
    sftp.get(remote_press, local_press)
    #The sftp channel is closed
    sftp.close()
    #the ssh instance is closed
    ssh.close()
