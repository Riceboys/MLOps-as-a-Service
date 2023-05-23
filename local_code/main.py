from flask import Flask, request

app = Flask(__name__)

@app.route('/receive-command', methods=['POST'])
def receive_command():
    command = request.get_data().decode()

    # Process the received command
    # Add your logic here

    return 'Command received successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
