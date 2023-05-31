import requests
import os
from flask import Flask


app = Flask(__name__)
port = 8080
ip_address = "0.0.0.0"

@app.route("/prepare", methods=["POST"])
def prepare_data():
    end_point = "prepare-data"
    external_server_url = f"http://0.0.0.0:8080/{end_point}" 

    command = 'prepare data for training'
    response = requests.post(external_server_url, data=command)

    if response.status_code == 200:
        print('Prepare data command sent successfully')
    else:
        print('Failed to send prepare-date command')

    return "/prepare-data executed sucessfully"

if __name__ == "__main__":
    app.run(ip_address, port)