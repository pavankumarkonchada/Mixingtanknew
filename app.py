from flask import Flask, request, jsonify
import paramiko
import requests
import base64
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
#import os

app = Flask(__name__)
app.config["DEBUG"] = True



# Azure VM details
azure_vm_ip = "20.163.248.81"
azure_vm_username = "pavan"
azure_vm_password = "Cadfemindia@2023"

@app.route("/", methods=["GET"])
def transfer_file():

    subscription_id="caa619ff-3041-4ba1-a933-ee23683796f5"
    resource_group="cadfemservices"
    vm_name="cadfemvm"
    command="ipconfig"

    #authenticate using managed identity
    credentials=DefaultAzureCredential()

    #create compute management client
    compute_client=ComputeManagementClient(credentials,subscription_id)

    #executing command on VM
    result=compute_client.virtual_machines.run_command(resource_group,vm_name,{'command_id':'RunShellScript','script':[command]})

    #getting output from the command
    command_output=result.value[0].message
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
