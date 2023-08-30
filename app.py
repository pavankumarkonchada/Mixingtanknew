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
        python_executable = r'C:\\Users\\pavan\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        command_to_execute = (
            f'"{python_executable}" -c '
            '"from ansys.fluent.core import launch_fluent;'
            'import ansys.fluent.core as pyfluent;'
            'meshing=pyfluent.launch_fluent(precision=\'double\', processor_count=4, mode=\'meshing\', show_gui=False);'
            'meshing.workflow.InitializeWorkflow(WorkflowType=\'Watertight Geometry\');'
            'path=r\\"C:\\\\check\\\\geom1.scdoc\\";'
            'meshing.workflow.TaskObject[\\"Import Geometry\\"].Arguments = {"FileName": path,"LengthUnit": "mm",}"'
        )

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        # Construct the command with environment variables
        env = {'PATH': f'%PATH%;{ansys_fluent_path}', 'AWP_ROOT231': r'C:\Program Files\ANSYS Inc\ANSYS Student\v231'}
        command_with_path = f'cmd /C {command_to_execute}'
        
        # Execute the Fluent launch command on remote VM
        stdin, stdout, stderr = ssh_client.exec_command(command_with_path, environment=env)

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
