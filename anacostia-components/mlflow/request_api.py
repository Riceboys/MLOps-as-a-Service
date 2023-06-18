import requests
import json

def create_experiment(name: str):
    url = "http://localhost:8000/api/2.0/mlflow/experiments/create"
    parameters = {"name": name}
    response = requests.post(url, json=parameters)
    response = json.loads(response.text)
    return response["experiment_id"]

def get_experiment(experiment_id: str) -> json:
    url = "http://localhost:8000/api/2.0/mlflow/experiments/get"
    parameters = {"experiment_id": experiment_id}
    response = requests.get(url, json=parameters)
    response = json.loads(response.text)
    return response

if __name__ == "__main__":
    response = create_experiment(name="test2")
    print(get_experiment(experiment_id=response))