from flask import Flask
import paramiko

app = Flask(__name__)

@app.route('/')
def launch_fluent():
    try:
        vm_ip_address = '13.68.168.34'
        username = 'pavan'
        password = 'Cadfemindia@2023'

        ansys_fluent_path = r'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v231\\fluent\\ntbin\\win64'
        python_executable = r'C:\Users\pavan\AppData\Local\Programs\Python\Python311\python.exe'
        remote_script_path = r'C:\mixingtank_pyfluent.py'  # Path to the script on the remote VM
        command_to_execute = (
            f'setx PATH "%PATH%;{ansys_fluent_path}" && '
            f'"{python_executable}" "{remote_script_path}"'
        )
        env={'AWP_ROOT231': 'C:\Program Files\ANSYS Inc\ANSYS Student\v231'}
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        # Execute the Fluent launch command on remote VM
        stdin, stdout, stderr = ssh_client.exec_command(command_to_execute,environment=env)

        # Capture and process output
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh_client.close()

        return f"<pre>Output: {output}\nError: {error}</pre>"
    except Exception as e:
        app.logger.error(f'Error occurred: {e}')
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=49672, debug=True)
