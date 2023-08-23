from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=['POST'])
def process_file():
    try:
        # Read user input from the HTML form
        input_value = 1.2
        
        # Read the file from the GitHub repository
        github_file_url = 'https://github.com/pavankumarkonchada/Mixingtanknew/blob/main/lib/pymapdl/mixing_tank_pyfluent.py'
        response = requests.get(github_file_url)
        github_file_content = response.text
        
        # Modify the content based on user input
        modified_content = github_file_content.replace('max_size', str(input_value))
        
        # Send the modified content to the VM through API
        vm_api_url = 'http://20.163.248.81/api/endpoint'
        vm_api_data = {'content': modified_content}
        response = requests.post(vm_api_url, json=vm_api_data)
        
        return jsonify({"status": "success", "message": "File modified and sent to VM successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':   
    app.run(host='0.0.0.0', debug=True)
