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

        remote_script_path = "C:\\mixing_tank_pyfluent.py"

        # Read and execute each line of the script
        output_lines = []
        with open("C:\\mixing_tank_pyfluent.py", "r") as script_file:
            for line in script_file:
                # Execute the line on the remote VM
                command = f"python -c '{line.strip()}'"
                stdin, stdout, stderr = ssh_client.exec_command(command)

                exit_status = stdout.channel.recv_exit_status()
                output_lines.append(stdout.read().decode())

        # Close the SSH connection
        ssh_client.close()

        return jsonify({"status": "success", "output": output_lines})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0',Debug=True,use_reloader=False,port=5000)
