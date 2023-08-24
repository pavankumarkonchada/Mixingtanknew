from flask import Flask, request, jsonify
import paramiko
import requests
import base64
from flask import Flask, jsonify
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

@app.route('/')
def execute_command():
    # Get the VM details from the request
    vm_ip ='20.163.248.81'
    vm_username = 'pavan'
    vm_password = 'Cadfemindia@2023'

    # Command to open Notepad
    command = 'notepad.exe'

    try:
        # Create an SSH client instance
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the VM using username and password
        ssh_client.connect(vm_ip, username=vm_username, password=vm_password)

        # Execute the command
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Close the SSH connection
        ssh_client.close()

        return jsonify({'message': 'Command executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
