from flask import Flask, jsonify
import paramiko
import os
import base64

app = Flask(__name__)

# Azure VM details
azure_vm_ip = '20.163.248.81'
azure_vm_username = 'pavan'
azure_vm_password = 'Cadfemindia@2023'

@app.route("/")
def open_notepad():
    try:
        # Retrieve Private Key from Environment Variable
        private_key_base64 = os.environ.get('PrivateKey')
        private_key_bytes = base64.b64decode(private_key_base64)

        # SSH Connection to Azure VM
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        private_key_obj = paramiko.RSAKey.from_private_key(private_key_bytes)
        ssh.connect(azure_vm_ip, username=azure_vm_username, pkey=private_key_obj)

        # Execute the command remotely (open Notepad)
        stdin, stdout, stderr = ssh.exec_command('notepad.exe')
        output = stdout.read().decode()

        ssh.close()

        return jsonify({"result": output})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

