from flask import Flask, request, jsonify
import paramiko
import requests

app = Flask(__name__)



# Azure VM details
azure_vm_ip = "your_vm_ip_address"
azure_vm_username = "your_vm_username"
azure_vm_password = "your_vm_password"

@app.route("/transfer", methods=["GET"])
def process_file():
    try:
        # Read user input from the HTML form
        input_value = 1.2
        
        # Read the file from the GitHub repository
        github_file_url = 'https://github.com/pavankumarkonchada/Mixingtanknew/blob/main/lib/pymapdl/mixing_tank_pyfluent.py'
        response = requests.get(github_file_url)
        github_file_content = response.text
        
        # Modify the content based on user input
        modified_content = github_file_content.replace('max_size',str(input_value))
        print("Running adfajspdfj kajsfpaksdjf")
        # Send the modified content to the VM through API
        vm_api_url = 'http://20.163.248.81:80/api/endpoint'
        vm_api_data = {'content': modified_content}
        response = requests.post(vm_api_url, json=vm_api_data)
        
        return jsonify({"status": "success", "message": "File modified and sent to VM successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
