from flask import Flask, request, jsonify
import mlflow


app = Flask(__name__)

@app.route("/create-experiment", methods=["POST"])
def create_experiment():
    if request.is_json:
        try:
            params = request.get_json()

            experiment_name = params.get("name")
            tags = params.get("tags", {})

            experiment_id = mlflow.create_experiment(
                name=experiment_name, 
                tags=tags
            )

            response_data = {
                "message": "Experiment created successfully.",
                "name": experiment_name,
                "id": experiment_id,
                "tags": tags
            }

            response = jsonify(response_data)
            response.status_code = 200

            return response

        except Exception as e:
            response_data = {
                "message": "Experiment creation failed.",
                "error": str(e)
            }

            response = jsonify(response_data)
            response.status_code = 500

            return response
    else:
        return "Request was not JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)