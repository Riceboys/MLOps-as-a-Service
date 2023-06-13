from flask import request, Flask
import requests


app = Flask(__name__)

@app.route("/prepare-data", methods=["POST"])
def prepare_data():
    print("printing data")
    return "/prepare-data executed sucessfully"

if __name__ == "__main__":
    end_point = "prepare"
    ip_address = "127.0.0.1"
    port = 8080

    """
    alias = "anacostia_anacostia-executor"
    port = 8080
    end_point = "prepare"
    ip_address = "127.0.0.1"
    external_server_url = f"http://{ip_address}:{port}/{end_point}" 

    command = 'prepare data for training'
    response = requests.post(external_server_url, data=command)

    if response.status_code == 200:
        print('Prepare data command sent successfully')
    else:
        print('Failed to send prepare-data command')
    """
    
    app.run(ip_address, port)
