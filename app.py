from flask import Flask
import paramiko
#from pypsexec.client import Client
import winrm
import socket
import Xlib.support.connect as xlib_connect
import logging
import select

LOGGER = logging.getLogger(__name__)
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
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip_address, username=username, password=password)

        
        channels = {}
        poller = select.poll()
        def x11_handler(channel):
            x11_chanfd = channel.fileno()
            local_x11_socket = xlib_connect.get_socket(*local_x11_display[:3])
            local_x11_socket_fileno = local_x11_socket.fileno()
            channels[x11_chanfd] = channel, local_x11_socket
            channels[local_x11_socket_fileno] = local_x11_socket, channel
            poller.register(x11_chanfd, select.POLLIN)
            poller.register(local_x11_socket, select.POLLIN)
            LOGGER.debug('x11 channel on: %s %s', src_addr, src_port)
            transport._queue_incoming_channel(channel)
        def flush_out(session):
            while session.recv_ready():
                sys.stdout.write(session.recv(4096))
            while session.recv_stderr_ready():
                sys.stderr.write(session.recv_stderr(4096))
        # get local disply
        local_x11_display = xlib_connect.get_display(os.environ['DISPLAY'])
        # start x11 session
        transport = ssh_client.get_transport()
        session = transport.open_session()
        session.request_x11(handler=x11_handler(channel))
        session.exec_command('xterm')
        session_fileno = session.fileno()
        poller.register(session_fileno, select.POLLIN)
        # accept first remote x11 connection
        transport.accept()
        # event loop
        while not session.exit_status_ready():
            poll = poller.poll()
            # accept subsequent x11 connections if any
            if len(transport.server_accepts) > 0:
                transport.accept()
            if not poll: # this should not happen, as we don't have a timeout.
                break
            for fd, event in poll:
                if fd == session_fileno:
                    flush_out(session)
                # data either on local/remote x11 socket
                if fd in channels.keys():
                    channel, counterpart = channels[fd]
                    try:
                        # forward data between local/remote x11 socket.
                        data = channel.recv(4096)
                        counterpart.sendall(data)
                    except socket.error:
                        channel.close()
                        counterpart.close()
                        del channels[fd]
        print 'Exit status:', session.recv_exit_status()
        flush_out(session)
        session.close()



        #s = winrm.Session('13.68.168.34', auth=('pavan', 'Cadfemindia@2023'))
        #r = s.run_cmd('notepad.exe')
        
        # Construct the Fluent command with proper quoting
        fluent_command = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -File C:\run.ps1'
        #r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -File C:\run.ps1'#(f'"{ansys_fluent_path}\\fluent.exe" 3ddp -meshing -gu -ssh -wait')

        # Execute the Fluent launch command on remote VM
        stdin, stdout, stderr = ssh_client.exec_command(fluent_command)

        # Capture and process output
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh_client.close()

        
        
        #c = Client("cadfemvmwindows", username="pavan", password="Cadfemindia@2023",encrypt=False)
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
