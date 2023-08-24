from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def check_vm():
    vm_ip = '20.163.248.81'
    vm_port = 3389  # RDP port

    try:
        # Attempt to create a socket connection
        socket.create_connection((vm_ip, vm_port), timeout=10)
        return "VM is reachable"
    except ConnectionError:
        return "VM is not reachable"

if __name__ == '__main__':
    app.run()
