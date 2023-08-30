from flask import Flask
import paramiko

app = Flask(__name__)

@app.route('/')
def launch_fluent():
    try:
        vm_ip_address = '13.68.168.34'
        username = 'pavan'
        password = 'Cadfemindia@2023'
        
        ansys_install_path = r'C:\Program Files\ANSYS Inc\ANSYS Student\v231'
        python_executable = r'C:\Users\pavan\AppData\Local\Programs\Python\Python311\python.exe'
        remote_script_path = r'C:\mixingtank_pyfluent.py'  # Path to the script on the remote VM
        env={'AWP_ROOT231': r'C:\Program Files\ANSYS Inc\ANSYS Student\v231'}
        
        # Construct the command with environment variables and the actual command                                              
        command_to_execute = (
            f'setx PATH "%PATH%;{ansys_install_path}\\fluent\\ntbin\\win64" && '
            f'setx AWP_ROOT231 "{ansys_install_path}" && '
            f'ssh -t {username}@{vm_ip_address} '
            f'"{python_executable}" "{remote_script_path}"'
        )

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        # Execute the SSH command
        stdin, stdout, stderr = ssh_client.exec_command(command_to_execute, environment=env)

        # Capture and process output
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh_client.close()

        return f"<pre>Output: {output}\nError: {error}</pre>"
    except Exception as e:
        app.logger.error(f'Error occurred: {e}')
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True)
