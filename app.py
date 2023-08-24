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
response = requests.get(f"http://{vm_ip}:3389")
if response.status_code == 200:
    print("VM is reachable")
else:
    print("VM is not reachable")

if __name__ == '__main__':
    app.run()
