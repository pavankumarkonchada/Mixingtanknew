from flask import Flask, request, render_template
import paramiko

app = Flask(__name__)

@app.route('/')

def copy_file():
    source_file_path = 'id_rsa'  # Adjust this path
    destination_path = '/mnt/mydisk'    # Adjust this path
    vm_ip_address = '52.249.184.159'
    username = 'pavan'
    password = 'Cadfemindia@2023'

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)
        
        # SCP the file
        with ssh_client.open_sftp() as sftp:
            sftp.put(source_file_path, destination_path)
        
        ssh_client.close()
        return 'File copied successfully!'
    except Exception as e:
        return f'Error: {e}'

if name == '__main__':
    app.run(debug=True)
