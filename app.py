from flask import Flask, jsonify
import pywinrm

app = Flask(__name__)

# Azure VM details
azure_vm_ip = '20.163.248.81'
azure_vm_username = 'pavan'
azure_vm_password = 'Cadfemindia@2023'

# WinRM connection
session = pywinrm.Session(
    azure_vm_ip,
    auth=(azure_vm_username, azure_vm_password),
    transport='ntlm',  # You can use 'basic' or 'ntlm' here
    server_cert_validation='ignore'  # Ignore SSL certificate validation
)

@app.route("/")
def open_notepad():
    # Trigger the remote command to open Notepad
    command = "notepad.exe"
    result = run_remote_command(command)
    
    return jsonify({"result": result})

def run_remote_command(command):
    try:
        # Establish WinRM session
        shell_id = session.protocol.open_shell()
        
        # Run command in the shell
        command_id = session.protocol.run_command(shell_id, command, [])
        
        # Get command output
        output = session.protocol.get_command_output(shell_id, command_id)
        
        # Close the shell
        session.protocol.cleanup_command(shell_id, command_id)
        session.protocol.close_shell(shell_id)
        
        return output.std_out.decode()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
