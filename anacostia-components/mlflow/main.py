import requests
import os
from flask import Flask, request, jsonify
import socket
import mlflow


class MLFlow:

    def __init__(self, HOST, PORT) -> None:
        self.HOST = HOST
        self.PORT = PORT
    
    def log_metrics(self):
        data = request.json  # Assuming the request body is in JSON format
        print(data)

        param1 = data.get('param1')  # Get the value of 'param1' from the JSON request body
        param2 = data.get('param2')  # Get the value of 'param2' from the JSON request body

        response_data = {
            'message': 'Request received successfully.',
            'param1': param1,
            'param2': param2
        }

        response = jsonify(response_data)
        response.status_code = 200

        return response


if __name__ == "__main__":
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    print(hostname)
    print(host_ip)

    HOST_IP = os.getenv("HOST")
    INBOUND_PORT = os.getenv("IN_PORT")
    OUTBOUND_PORT = os.getenv("OUT_PORT")
    HOST_IP = "localhost"
    INBOUND_PORT = "8000"
    OUTBOUND_PORT = "12345"

    print(HOST_IP)
    print(INBOUND_PORT)
    print(OUTBOUND_PORT)
    
    executor = MLFlow(
        HOST=HOST_IP,
        PORT=OUTBOUND_PORT,
    )

    app = Flask(__name__)

    app.add_url_rule("/log-metrics", view_func=executor.log_metrics, methods=["POST"])

    app.run(host='0.0.0.0', port=INBOUND_PORT)
