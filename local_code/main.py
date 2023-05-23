import socket

HOST = '0.0.0.0'  # The server's IP address (use 0.0.0.0 to listen on all available interfaces)
PORT = 12345     # The port to listen on

def process_command(command):
    # Process the received command as needed
    # Add your logic here
    print("Received command:", command)

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to a specific host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    # Accept incoming connections
    while True:
        client_socket, client_address = server_socket.accept()

        # Receive data from the client
        command = client_socket.recv(1024).decode()

        # Process the received command
        process_command(command)

        # Send a response (optional)
        response = "Command received successfully"
        client_socket.sendall(response.encode())

        # Close the client connection
        client_socket.close()
