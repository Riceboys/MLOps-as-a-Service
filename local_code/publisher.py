from flask import Flask
import os
import json
import socket


app = Flask(__name__)


def json_post_request(unix_socket_path: str, endpoint_path: str, payload_json):
    # Connect to the Unix socket
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(unix_socket_path)

        # Send the POST request headers
        headers = [
            f'POST {endpoint_path} HTTP/1.1',
            'Host: localhost',
            'Content-Type: application/json',
            f'Content-Length: {len(payload_json)}',
            'Connection: close',
            '',
            ''
        ]
        request = '\r\n'.join(headers).encode('utf-8')
        client.send(request)

        # Send the payload data
        client.send(payload_json.encode('utf-8'))

        # Receive and print the response
        response = client.recv(4096)
        print(response.decode('utf-8'))

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
        print(response.decode('utf-8'))


@app.route('/inbound', methods=["POST"])
def hello():

    outbound_socket_path = '/tmp/anacostia-executor-outbound.sock'
    json_get_request(unix_socket_path=outbound_socket_path, endpoint_path="/outbound")

    """
    payload = {'name': 'John', 'age': 30}
    payload_json = json.dumps(payload)
    
    json_post_request(
        unix_socket_path=outbound_socket_path, 
        endpoint_path="/outbound", 
        payload_json=payload_json
    )
    """

    return 'inbound relay\n'

if __name__ == '__main__':
    inbound_socket_path = 'unix:///tmp/anacostia-executor-inbound.sock'
    
    if os.path.exists(inbound_socket_path):
        os.remove(inbound_socket_path)

    # Bind the Flask app to the Unix socket
    app.run(host=inbound_socket_path)

    # command to curl endpoint:
    # curl --unix-socket /tmp/anacostia-executor-inbound.sock -X POST http://127.0.0.1/inbound