import socket

# Connect to the server using the same socket path
socket_path = "/tmp/anacostia_socket.sock"

client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client_socket.connect(socket_path)

message = "start1"
client_socket.sendall(message.encode())

response = client_socket.recv(1024)
print("Server response:", response.decode())

client_socket.close()
