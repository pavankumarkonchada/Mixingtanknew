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
        remote_script_path = r'C:\\mixingtank_pyfluent.py'  # Path to the script on the remote VM

        # Construct the SSH command with -t flag and environment setup
        ssh_command = (
            f'setx PATH "%PATH%;{ansys_fluent_path}" && '
            f'setx AWP_ROOT231 "{ansys_fluent_path}" && '  # Set the AWP_ROOT231 variable
            f'"{python_executable}" "{remote_script_path}"'
        )

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        # Execute the SSH command in an interactive shell
        stdin, stdout, stderr = ssh_client.exec_command(f'ssh -t {username}@{vm_ip_address} "{ssh_command}"')

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
