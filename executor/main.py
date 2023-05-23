import requests
import socket

# host.docker.internal DNS name only works on Docker Desktop for Mac, Docker Desktop for Windows, and Docker Toolbox.
host_ip = socket.gethostbyname('host.docker.internal')
port = "12345"
end_point = "train"
external_server_url = f'http://{host_ip}:{port}/{end_point}'  

command = 'Do something'

response = requests.post(external_server_url, data=command)

if response.status_code == 200:
    print('Command sent successfully')
else:
    print('Failed to send command')
