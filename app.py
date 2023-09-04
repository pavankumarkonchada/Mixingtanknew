from flask import Flask
import paramiko
#from pypsexec.client import Client
import winrm
from pypsexec.client import Client
import wmi
from socket import*
SW_SHOWNORMAL = 1



app = Flask(__name__)
app.config['REQUEST_TIMEOUT'] = 300  # Set your desired timeout value in seconds

@app.route('/')
def launch_fluent():
    try:
        vm_ip_address = '13.68.168.34'
        username = 'pavan'
        password = 'Cadfemindia@2023'
        
        
        ansys_fluent_path = r'C:\Program Files\ANSYS Inc\ANSYS Student\v231\fluent\ntbin\win64'
        remote_script_path = r'C:\mixingtank_pyfluent.py'  # Path to the script on the remote VM
        
        ssh_client = paramiko.SSHClient()
        ssh_config=paramiko.SSHConfig()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)
        
        #s = winrm.Session('13.68.168.34', auth=('pavan', 'Cadfemindia@2023'))
        #r = s.run_cmd('notepad.exe')
        
        # Construct the Fluent command with proper quoting
        fluent_command = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -File C:\run.ps1'
        #r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -File C:\run.ps1'#(f'"{ansys_fluent_path}\\fluent.exe" 3ddp -meshing -gu -ssh -wait')

        # Execute the Fluent launch command on remote VM
        #stdin, stdout, stderr = ssh_client.exec_command(fluent_command)

        # Capture and process output
        #output = stdout.read().decode()
        #error = stderr.read().decode()

        ssh_client.close()

        connection = wmi.WMI(computer = '13.68.168.34', user = 'pavan', password = 'Cadfemindia@2023')

        process_startup = connection.Win32_ProcessStartup.new()
        process_startup.ShowWindow = SW_SHOWNORMAL
        process_id, result = connection.Win32_Process.Create(CommandLine="cmd.exe /c C:\\Users\\pavan\\testbat.bat",ProcessStartupInformation=process_startup)
        if result == 0:
          print("Process started successfully: %d" % process_id)
        else:
          raise RuntimeError
        
        #c = Client("13.68.168.34", username="pavan", password="Cadfemindia@2023",encrypt=True)
        #c.connect()
        #c.cleanup()  # this is where the magic happens
        #c.disconnect()
        #try:
        #    c.create_service()
        #    stdout, stderr, rc = c.run_executable("cmd.exe",arguments="/c echo Hello World")
        #finally:
        #    c.remove_service()
        #    c.disconnect()
            
        return f"<pre>Output: {output}\nError: {error}</pre>"
    except Exception as e:
        app.logger.error(f'Error occurred: {e}')
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
