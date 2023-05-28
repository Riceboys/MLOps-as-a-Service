import requests
import socket
import schedule
import os


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
            print('Train command sent successfully')
        else:
            print('Failed to send train command')
    
    def prepare_data(self):
        end_point = "prepare-data"
        external_server_url = f'http://{self.HOST}:{self.PORT}/{end_point}' 

        command = 'prepare data for training'
        response = requests.post(external_server_url, data=command)

        if response.status_code == 200:
            print('Prepare data command sent successfully')
        else:
            print('Failed to send prepare-date command')
    
    def run(self):
        self.prepare_data()
        self.train()
    

if __name__ == "__main__":

    HOST_IP = os.getenv("HOST")
    PORT = os.getenv("PORT")

    executor = Executor(
        HOST=HOST_IP,
        PORT=PORT,
    )

    executor.run()
