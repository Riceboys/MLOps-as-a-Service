import socket


HOST = '192.168.0.172'  # Replace with the server's IP address or domain name
PORT = 12345                  # Replace with the port the server is listening on


if __name__ == "__main__":

    # Establish a connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # Send a command to the server
        command = "Do something"
        client_socket.sendall(command.encode())

        # Receive a response (optional)
        response = client_socket.recv(1024).decode()
        print("Server response:", response)
        print("hello")