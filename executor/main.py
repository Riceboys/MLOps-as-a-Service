import socket

# host.docker.internal DNS name only works on Docker Desktop for Mac, Docker Desktop for Windows, and Docker Toolbox.
host_ip = socket.gethostbyname('host.docker.internal')
port = 12345

# Establish a connection to the server
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host_ip, port))

        # Send a command to the server
        command = "Do something"
        client_socket.sendall(command.encode())

        # Receive a response (optional)
        response = client_socket.recv(1024).decode()
        print("Server response:", response)
        print("hello")
