import socket
import os

"""
class FunctionRunner:
    def __init__(self):
        self.functions = []

    def decorator(self, expected_message):
        def inner_decorator(func):
            def wrapper(*args, **kwargs):
                data = self.receive_message()
                if data.decode() == expected_message:
                    with self.connection:
                        func(*args, **kwargs)
            self.functions.append(wrapper)
            return wrapper
        return inner_decorator

    def receive_message(self):
        # Replace this implementation with your actual message receiving logic
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        socket_path = "/tmp/anacostia_socket.sock"
        if os.path.exists(socket_path):
            os.remove(socket_path)
        server_socket.bind(socket_path)
        server_socket.listen(1)
        self.connection, _ = server_socket.accept()
        data = self.connection.recv(1024)
        return data

    def run(self):
        for func in self.functions:
            func()

# Usage example

runner = FunctionRunner()

@runner.decorator("start")
def start_processing():
    print("Processing started")

@runner.decorator("stop")
def stop_processing():
    print("Processing stopped")

runner.run()
"""


"""
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
            response = "No response"
            if data.decode() == expected_message:
                response = func()
            connection.sendall(response.encode())
            connection.close()
        return wrapper
    return decorator

@message_handler("start1")
def start1():
    print("Processing started")
    return "start signal received"

@message_handler("start2")
def start2():
    print("Processing started")
    return "start2 signal received"

socket_path = "/tmp/anacostia_socket.sock"
if os.path.exists(socket_path) == True:
    os.remove(socket_path)

server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_socket.bind(socket_path)
server_socket.listen(1)

print("Server listening on", socket_path)

while True:
    connection, _ = server_socket.accept()
    start1(connection)
    start2(connection)
