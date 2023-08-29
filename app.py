from flask import Flask
import paramiko

app = Flask(__name__)

@app.route('/')
def copy_and_open_file():
    source_file_path = 'lib/pymapdl/mixing_tank_pyfluent.py'  # Adjust this path
    destination_path = 'C:\\mixing_tank_pyfluent1.py'  # Adjust this path
    vm_ip_address = '13.68.168.34'
    username = 'pavan'
    password = 'Cadfemindia@2023'
    
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        # SCP the file
        with ssh_client.open_sftp() as sftp:
            sftp.put(source_file_path, destination_path)

        # Open the file using PowerShell
        channel = ssh_client.invoke_shell()
        command = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -File C:\run.ps1'
        channel.send(command)

        output = ""
        while True:
            if channel.recv_ready():
                output += channel.recv(1024).decode()
            if channel.exit_status_ready():
                break

        paramiko.util.log_to_file('sssh.log')
        ssh_client.close()
        
        return f"<pre>{output}</pre>"
    except Exception as e:
        # Log the exception for troubleshooting
        app.logger.error(f'Error occurred: {e}')
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True)
