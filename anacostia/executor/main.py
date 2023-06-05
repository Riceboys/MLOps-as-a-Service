import requests
import os
from flask import Flask
import socket


def json_get_request(unix_socket_path: str, endpoint_path: str):
    # Connect to the Unix socket
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(unix_socket_path)

        # Send the GET request headers
        headers = [
            f'GET {endpoint_path} HTTP/1.1',
            'Host: localhost',
            'Connection: close',
            '',
            ''
        ]
        request = '\r\n'.join(headers).encode('utf-8')
        client.send(request)

        # Receive and print the response
        response = client.recv(4096)
        response = response.decode('utf-8')

        # Extract the status code from the response
        status_code = response.split()[1]

        # Print the response and return the status code
        print(response)
        return status_code

class Executor:

    def __init__(self, socket_path: str, schedule: str = None) -> None:
        self.schedule = schedule
        self.socket_path = socket_path
    
    def train(self):
        #json_get_request(self.socket_path, "/train")
        return "/execute-train worked"
    
    def prepare_data(self):
        # json_get_request(self.socket_path, "/prepare-data")
        return "/execute-prepare worked"
    
    def run_all(self):
        self.prepare_data()
        self.train()
        return "all steps executed successfully\n"


if __name__ == "__main__":
    
    outbound_socket_path = '/tmp/anacostia-executor-outbound.sock'
    if os.path.exists(outbound_socket_path):
        os.remove(outbound_socket_path)

    executor = Executor(
        socket_path=outbound_socket_path
    )

    app = Flask(__name__)

    app.add_url_rule("/execute-prepare", view_func=executor.prepare_data, methods=["POST"])
    app.add_url_rule("/execute-train", view_func=executor.train, methods=["POST"])
    app.add_url_rule("/execute-all", view_func=executor.run_all, methods=["POST"])

    inbound_socket_path = 'unix:///tmp/anacostia-executor-inbound.sock'
    #inbound_socket_path = "unix:///var/run/anacostia-executor-inbound.sock"
    if os.path.exists(inbound_socket_path):
        os.remove(inbound_socket_path)

    app.run(host=inbound_socket_path)
