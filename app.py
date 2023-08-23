from flask import Flask, request, jsonify
import paramiko
import requests
import base64

app = Flask(__name__)



# Azure VM details
azure_vm_ip = "20.163.248.81"
azure_vm_username = "pavan"
azure_vm_password = "Cadfemindia@2023"

@app.route("/transfer", methods=["GET"])
def transfer_file():
    try:
        # Download the file from GitHub
        #headers = {"Authorization": f"Bearer {github_pat}"}
        github_api_url = f"https://raw.githubusercontent.com/pavankumarkonchada/Mixingtanknew/main/lib/pymapdl/mixing_tank_pyfluent.py"
        response = requests.get(github_api_url)
        content = response.json()
        print("it is getting the github file")
        file_content = content["content"]
        #file_content_decoded = file_content.encode("utf-8")
        file_content_decoded = file_content#base64.b64decode(file_content_decoded)

        # Establish SSH connection to Azure VM
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(azure_vm_ip, username=azure_vm_username, password=azure_vm_password)

        # Transfer the file to Azure VM using SCP
        with ssh_client.open_sftp() as sftp:
            remote_path = "C:/check/destination.py"
            with sftp.file(remote_path, "wb") as remote_file:
                remote_file.write(file_content_decoded)

        ssh_client.close()

        return jsonify({"message": "File transferred successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
