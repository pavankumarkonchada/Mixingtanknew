from flask import Flask, jsonify
import pywinrm
import paramiko

app = Flask(__name__)

# Azure VM details
azure_vm_ip = '20.163.248.81'
azure_vm_username = 'pavan'
azure_vm_password = 'Cadfemindia@2023'

# WinRM connection
#session = pywinrm.Session(
#    azure_vm_ip,
#    auth=(azure_vm_username, azure_vm_password),
#    transport='ntlm',  # You can use 'basic' or 'ntlm' here
#    server_cert_validation='ignore'  # Ignore SSL certificate validation
#)

@app.route("/")
def open_notepad():
    try:
        private_key_path = '/id_rsa'
        username = 'pavan'
        host = '20.163.248.81'

        # Establish SSH connection
        private_key = paramiko.RSAKey(filename=private_key_path)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, pkey=private_key)

        # Execute the command remotely (open Notepad)
        stdin, stdout, stderr = ssh_client.exec_command('notepad.exe')
        output = stdout.read().decode()

        ssh_client.close()

        return jsonify({"result": output})
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
