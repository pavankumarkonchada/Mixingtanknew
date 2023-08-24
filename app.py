from flask import Flask, jsonify
import paramiko
import requests
import io  # Import the io module
import socket
app = Flask(__name__)

# Azure VM details


def test_connection(host, port):
    try:
        socket.create_connection((host, port))
        return True
    except (ConnectionRefusedError, TimeoutError):
        return False

windows_vm_ip = "20.163.248.81"
ssh_port = 22  # SSH port
azure_vm_ip = '20.163.248.81'
azure_vm_username = 'pavan'
azure_vm_password = 'Cadfemindia@2023'

@app.route("/")
def open_notepad():
if test_connection(windows_vm_ip, ssh_port):
    print("Connection successful")
else:
    print("Connection failed")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
