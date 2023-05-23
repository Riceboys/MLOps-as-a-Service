from flask import request
from mlops_decorators import MLOpsPipeline
import socket

HOST = '0.0.0.0'  # The server's IP address (use 0.0.0.0 to listen on all available interfaces)
PORT = 12345     # The port to listen on


pipeline = MLOpsPipeline()

@pipeline.train()
def process_command(command):
    # Process the received command as needed
    # Add your logic here
    print("Received command:", command)


