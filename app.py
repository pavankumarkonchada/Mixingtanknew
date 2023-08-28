from flask import Flask, request, render_template
import paramiko
import os
app = Flask(__name__)

@app.route('/')
def copy_file():
    source_file_path = 'lib/pymapdl/mixing_tank_pyfluent.py'  # Adjust this path
    destination_path = '/home/mixing/mixing_tank_pyfluent1.py'    # Adjust this path
    vm_ip_address = '52.249.184.159'
    username = 'pavan'
    password = 'Cadfemindia@2023'
    private_key_path = 'lib/id_rsa'
    input_str1='C:\Check\geom1.scdoc'
    input_str3='1.2'
    #try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(vm_ip_address, username=username, password=password)
    file=file=open(source_file_path, 'rt')
    current_content=file.read()
    updated_content = current_content.replace('import_filename', input_str1).replace('max_size', input_str3)
    file.close()
    file=open(source_file_path,'wt')
    file.write(updated_content)
    file.close()
    # SCP the file
    sftp = ssh_client.open_sftp()
    sftp.put(source_file_path, destination_path)
    #with ssh_client.open_sftp() as sftp:
    #    sftp.put(source_file_path,destination_path)
    name_of_file="filename.txt"
    path_to_file=os.path.join('/home/mixing/',name_of_file)
    cmd=f"touch {path_to_file}"
    stdin, stdout, stderr =ssh_client.exec_command("touch filename.txt")
    print(cmd)
    print(stdout)
    ssh_client.close()
    return "<h1 style='color:red'>command executed</h1>"
    #except Exception as e:
        # Log the exception for troubleshooting
    #    app.logger.error(f'Error occurred: {e}')
    #    return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True)
