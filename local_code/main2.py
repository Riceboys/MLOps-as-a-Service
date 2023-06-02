import socket
import os

class AnacostiaSocket:
    def __init__(self) -> None:
        self.connection = None
        self.functions = []
    
        self.socket_path = "/tmp/anacostia_socket.sock"
        if os.path.exists(self.socket_path) == True:
            os.remove(self.socket_path)
        print("Server listening on", self.socket_path)

    def train_handler(self, expected_message):
        def decorator(func):
            def wrapper():
                data = self.connection.recv(1024)
                if data.decode() == expected_message:
                    response = func()
                self.connection.sendall(response.encode())
                self.connection.close()
            return wrapper
        return decorator
    

ana_sock = AnacostiaSocket()

@ana_sock.train_handler("train1")
def start_processing():
    print("Processing started")
    return "signal received"

if __name__ == "__main__":
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(ana_sock.socket_path)
        server_socket.listen(1)

        while True:
            connection, _ = server_socket.accept()
            start_processing()

"""
def message_handler(expected_message):
    def decorator(func):
        def wrapper(connection):
            data = connection.recv(1024)
            if data.decode() == expected_message:
                response = func()
            connection.sendall(response.encode())
            connection.close()
        return wrapper
    return decorator

@message_handler("start")
def start_processing():
    print("Processing started")
    return "signal received"

socket_path = "/tmp/anacostia_socket.sock"
if os.path.exists(socket_path) == True:
    os.remove(socket_path)

server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_socket.bind(socket_path)
server_socket.listen(1)

print("Server listening on", socket_path)

while True:
    connection, _ = server_socket.accept()
    start_processing(connection)
"""
