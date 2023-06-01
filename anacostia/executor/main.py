import requests
import os
from flask import Flask


class Executor:

    def __init__(self, HOST, PORT, schedule=None) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.schedule = schedule
    
    def train(self):
        end_point = "train"
        external_server_url = f'http://{self.HOST}:{self.PORT}/{end_point}' 

        # we're not really doing anything with the command
        command = 'train model'
        response = requests.post(external_server_url, data=command)

        if response.status_code == 200:
            return 'Train command sent successfully\n'
        else:
            return 'Failed to send train command\n'
    
    def prepare_data(self):
        end_point = "prepare-data"
        external_server_url = f'http://{self.HOST}:{self.PORT}/{end_point}' 

        command = 'prepare data for training'
        response = requests.post(external_server_url, data=command)

        if response.status_code == 200:
            return 'Prepare data command sent successfully\n'
        else:
            return 'Failed to send prepare-date command\n'
    
    def run_all(self):
        self.prepare_data()
        self.train()
        return "all steps executed successfully\n"


if __name__ == "__main__":

    HOST_IP = os.getenv("HOST")
    INBOUND_PORT = os.getenv("IN_PORT")
    OUTBOUND_PORT = os.getenv("OUT_PORT")

    print(HOST_IP)
    print(INBOUND_PORT)
    print(OUTBOUND_PORT)
    
    executor = Executor(
        HOST=HOST_IP,
        PORT=OUTBOUND_PORT,
    )

    app = Flask(__name__)

    app.add_url_rule("/execute-prepare", view_func=executor.prepare_data, methods=["POST"])
    app.add_url_rule("/execute-train", view_func=executor.train, methods=["POST"])
    app.add_url_rule("/execute-all", view_func=executor.run_all, methods=["POST"])

    app.run(host='0.0.0.0', port=INBOUND_PORT)
