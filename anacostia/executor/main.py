import requests
import os
from flask import Flask


app = Flask(__name__)

class Executor:

    def __init__(self, HOST, PORT, schedule=None) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.schedule = schedule
    
    #@app.route("/train")
    def train(self):
        end_point = "train"
        external_server_url = f'http://{self.HOST}:{self.PORT}/{end_point}' 

        # we're not really doing anything with the command
        command = 'train model'
        response = requests.post(external_server_url, data=command)

        if response.status_code == 200:
            print('Train command sent successfully')
        else:
            print('Failed to send train command')
    
    #@app.route("/prepare-data")
    def prepare_data(self):
        end_point = "prepare-data"
        external_server_url = f'http://{self.HOST}:{self.PORT}/{end_point}' 

        command = 'prepare data for training'
        response = requests.post(external_server_url, data=command)

        if response.status_code == 200:
            print('Prepare data command sent successfully')
        else:
            print('Failed to send prepare-date command')
    
    #@app.route("/all")
    def run(self):
        self.prepare_data()
        self.train()
    
@app.route("/prepare", methods=["POST"])
def prepare_data():

    print("hello there lady")

    """
    end_point = "prepare-data"
    external_server_url = f'http://127.0.0.1:12345/{end_point}' 

    command = 'prepare data for training'
    response = requests.post(external_server_url, data=command)

    if response.status_code == 200:
        print('Prepare data command sent successfully')
    else:
        print('Failed to send prepare-date command')

    """
    return "/prepare-data executed sucessfully"

if __name__ == "__main__":

    HOST_IP = os.getenv("HOST")
    PORT = os.getenv("PORT")

    print(HOST_IP)
    print(PORT)
    
    executor = Executor(
        HOST=HOST_IP,
        PORT=PORT,
    )

    app.run(host='172.25.0.2', port=12345)
    #executor.run()
