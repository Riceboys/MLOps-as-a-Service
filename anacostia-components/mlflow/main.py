from flask import Flask, request, jsonify
import mlflow
from mlflow import MlflowException


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
                "experiment_id": experiment_id,
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

@app.route("/delete-experiment", methods=["POST"])
def delete_experiment():
    if request.is_json:
        try:
            params = request.get_json()

            experiment_id = params.get("experiment_id")

            mlflow.delete_experiment(experiment_id)

            response_data = {
                "message": "Experiment deleted successfully.",
                "experiment_id": experiment_id
            }

            response = jsonify(response_data)
            response.status_code = 200

            return response

        except MlflowException as error:
            response_data = {
                "message": "Experiment deletion failed.",
                "error": str(error)
            }

            response = jsonify(response_data)
            response.status_code = 400
            
            return response

        except Exception as e:
            print(str(e))

            response_data = {
                "message": "Experiment deletion failed.",
                "error": str(e)
            }

            response = jsonify(response_data)
            response.status_code = 500
            
            return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
