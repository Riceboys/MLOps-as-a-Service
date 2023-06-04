from flask import Flask
import os

app = Flask(__name__)

@app.route('/outbound', methods=["POST"])
def hello():
    return 'Hello, World!\n'

if __name__ == '__main__':
    outbound_socket_path = 'unix:///tmp/anacostia-executor-outbound.sock'
    
    if os.path.exists(outbound_socket_path):
        os.remove(outbound_socket_path)

    # Bind the Flask app to the Unix socket
    app.run(host=outbound_socket_path, port=9000)
