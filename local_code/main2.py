from flask import Flask, request

app = Flask(__name__)

@app.route("/prepare-data", methods=["POST"])
def func():
    print("it's working.")
    return "works"

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)