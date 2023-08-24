from flask import Flask, jsonify
import paramiko
import requests
import io  # Import the io module

app = Flask(__name__)

# Azure VM details
azure_vm_ip = '20.163.248.81'
azure_vm_username = 'pavan'
azure_vm_password = 'Cadfemindia@2023'

@app.route("/")
def open_notepad():
    try:
        private_key_url = 'https://raw.githubusercontent.com/pavankumarkonchada/Mixingtanknew/main/id_rsa'
        username = 'pavan'
        host = '20.163.248.81'

        # Fetch the private key content
        private_key_content = requests.get(private_key_url).content
        private_key_content_str = private_key_content.decode('utf-8')

        # Establish SSH connection
        private_key = paramiko.RSAKey(file_obj=io.StringIO(private_key_content_str))
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
