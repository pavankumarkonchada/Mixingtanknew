from flask import Flask
import socket
import paramiko

app = Flask(__name__)

# Azure VM details
windows_vm_ip = "20.163.248.81"
ssh_port = 22  # SSH port

def test_connection(host, port):
    try:
        socket.create_connection((host, port), timeout=10)  # Added timeout for better handling
        return True
    except (ConnectionRefusedError, TimeoutError):
        return False

@app.route("/")
def open_notepad():
    if test_connection(windows_vm_ip, ssh_port):
        return "Connection successful"
    else:
        return "Connection failed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
