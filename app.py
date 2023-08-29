from flask import Flask
import os
import paramiko

app = Flask(__name__)

@app.route('/')
def launch_fluent():
    vm_ip_address = '13.68.168.34'
    username = 'pavan'
    password = 'Cadfemindia@2023'
    ansys_fluent_path = r'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v231\\fluent\\ntbin\\win64'
    python_executable = r'C:\Users\pavan\AppData\Local\Programs\Python\Python311\python.exe'  # Python executable path
    command_to_execute = f'"{python_executable}" -c "from ansys.fluent.core import launch_fluent;import ansys.fluent.core as pyfluent;pyfluent.launch_fluent(precision=\'double\', processor_count=4, mode=\'meshing\', show_gui=False)"'

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        # Execute the Fluent launch command on remote VM
        env={'AWP_ROOT231': r'C:\Program Files\ANSYS Inc\ANSYS Student\v231'}
        command_with_path = f'setx PATH "%PATH%;{ansys_fluent_path}" && {command_to_execute}'
        stdin, stdout, stderr = ssh_client.exec_command(command_with_path, environment=env)

        # Capture and process output
        output = stdout.read().decode()
        error = stderr.read().decode()

        paramiko.util.log_to_file('sssh.log')
        ssh_client.close()

        return f"<pre>Output: {output}\nError: {error}</pre>"
    except Exception as e:
        app.logger.error(f'Error occurred: {e}')
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True)
