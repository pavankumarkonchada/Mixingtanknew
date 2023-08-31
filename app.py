from flask import Flask
import paramiko

app = Flask(__name__)
app.config['REQUEST_TIMEOUT'] = 300  # Set your desired timeout value in seconds

@app.route('/')
def launch_fluent():
    try:
        vm_ip_address = '192.168.12.222'
        username = 'cadfem'
        password = 'cadfem1'

        ansys_fluent_path = r'C:\Program Files\ANSYS Inc\ANSYS Student\v231\fluent\ntbin\win64'
        remote_script_path = r'C:\mixingtank_pyfluent.py'  # Path to the script on the remote VM
        
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        # Construct the Fluent command with proper quoting
        fluent_command = (f'"{ansys_fluent_path}\\fluent.exe" 3d -meshing -wait')

        # Execute the Fluent launch command on remote VM
        stdin, stdout, stderr = ssh_client.exec_command(fluent_command)

        # Capture and process output
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh_client.close()

        return f"<pre>Output: {output}\nError: {error}</pre>"
    except Exception as e:
        app.logger.error(f'Error occurred: {e}')
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
