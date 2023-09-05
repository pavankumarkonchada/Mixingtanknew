from flask import Flask
import paramiko

#an app instance is opened using variable app
app = Flask(__name__)

#open app with debugging disabled 
app.config["DEBUG"] = False

#list to define allowed geometry file extensions
app.config["ALLOWED_EXT_GEOM"]=["STP","STL","SCDOC","X_T","STEP"]

def geomext(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_EXT_GEOM"]:
        return True
    else:
        return False

@app.route('/')
def launch_fluent():
    try:
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

        #these flag variables are used to identify if the solution has run or not
        flag = ''
        flag2 = ''
        
        vm_ip_address = '13.68.168.34'
        username = 'pavan'
        password = 'Cadfemindia@2023'
        
        
        ansys_fluent_path = r'C:\Program Files\ANSYS Inc\ANSYS Student\v231\fluent\ntbin\win64'
        remote_script_path = r'C:\mixingtank_pyfluent.py'  # Path to the script on the remote VM
        source_file_path_scdocscript = 'spaceclaim_script1.py'  # Adjust this path
        destination_path_scdocscript = 'C:\\spaceclaim_script1.py'  # Adjust this path
	    source_file_path_runwb = 'run_wb1.py'  # Adjust this path
        destination_path_runwb = 'C:\\run_wb1.py'  # Adjust this path
	    source_file_path_wbjou = 'fluent_meshing.wbjn'  # Adjust this path
        destination_path_wbjou = 'C:\\fluent_meshing1.wbjn'  # Adjust this path
	    
        source_file_path_cxi = 'fluent_layout/Default/.cxlaout.ini'  # Adjust this path
        destination_path_cxi = 'C:\\Users\\hrithik\\.cxlayout.ini'  # Adjust this path


        ssh_client = paramiko.SSHClient()
        ssh_config=paramiko.SSHConfig()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)
        
        # Construct the Fluent command with proper quoting
        fluent_command = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -File C:\run.ps1'
        #r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -File C:\run.ps1'#(f'"{ansys_fluent_path}\\fluent.exe" 3ddp -meshing -gu -ssh -wait')

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
            source_file_path_goem = wkdir  # Adjust this path
            destination_path_geom = 'C:\\geom1.scdoc'  # Adjust this path
        
        with ssh_client.open_sftp() as sftp:
            sftp.put(source_file_path_pyfluent, destination_path_pyfluent)
			sftp.put(source_file_path_scdocscript, destination_scdocscript)
			sftp.put(source_file_path_runwb, destination_path_runwb)
			sftp.put(source_file_path_wbjou, destination_path_wbjou)
			sftp.put(source_file_path_goem, destination_path_goem)
            sftp.put(source_file_path_cxi, destination_path_cxi)
        
        # Execute the Fluent launch command on remote VM
        stdin, stdout, stderr = ssh_client.exec_command(fluent_command)

        # Capture and process output
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        remote_txt=r"C:\check\result.txt"
        local_txt=r"O:\Mixing_tank_py_web_app\myfile.txt"
        remote_press=r"C:\check\pressure.png"
        local_press=r"O:\Mixing_tank_py_web_app\static\pressure.png"
        remote_vel=r"C:\check\vel_plot.png"
        local_vel=r"O:\Mixing_tank_py_web_app\static\vel_plot.png"
        
        with ssh_client.open_sftp() as sftp:
            sftp.get(remote_txt, local_txt)
			sftp.get(remote_press, local_press)
			sftp.get(remote_vel, local_vel)

        
        ssh_client.close()
            
        return f"<pre>Output: {output}\nError: {error}</pre>"
    except Exception as e:
        app.logger.error(f'Error occurred: {e}')
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
