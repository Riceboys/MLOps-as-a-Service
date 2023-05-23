import requests

ip_address = "192.168.0.172"
port = "12345"
end_point = "receive-command"
external_server_url = f'http://{ip_address}:{port}/{end_point}'  

command = 'Do something'

response = requests.post(external_server_url, data=command)

if response.status_code == 200:
    print('Command sent successfully')
else:
    print('Failed to send command')
