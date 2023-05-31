import requests
import os
from flask import Flask


app = Flask(__name__)
port = 8000
ip_address = "0.0.0.0"

@app.route("/prepare", methods=["POST"])
def prepare_data():
    send()
    return "/prepare-data executed sucessfully"

def send():
    end_point = "prepare-data"
    # 10.151.207.219 is the elastic IP address of the flask app running on the host machine
    # port 8080 is the port the flask app running on the host machine is running on
    external_server_url = f"http://10.151.207.219:8080/{end_point}" 

    command = 'prepare data for training'
    response = requests.post(external_server_url, data=command)

    if response.status_code == 200:
        print('Prepare data command sent successfully')
    else:
        print('Failed to send prepare-date command')


if __name__ == "__main__":
    # we can trigger the pipeline by running curl -X POST http://0.0.0.0:8000/prepare 
    # since this flask app is running on port 8000 in the container and the container is listening to port 8000 on the host machine.
    # look at the docker-compose.yml file, we map ports 8080:8080 and 8000:8000
    app.run(ip_address, port)