import docker
from utils import *
import requests
import json
import os
import time
from typing import List


class AnacostiaComponent(object):
    def __init__(self, host_ip: str, image_name: str) -> None:
        self.host_ip = host_ip
        self.host_port = 8080
        self.url = f"http://{host_ip}:{self.host_port}"

        self.client = docker.from_env()
        self.image_name = image_name
        self.container_name = "mlflow-component"
        self.get_image()
        self.run_container()

    def get_image(self) -> None:
        try:
            self.client.images.get(self.image_name)
            print(f"Found image {self.image_name} locally.")

        except docker.errors.ImageNotFound:
            print(f"Image {self.image_name} is not available locally, pulling image {self.image_name} from Docker Hub.")
            self.client.images.pull(self.image_name)
            print(f"Done pulling image {self.image_name} from Docker Hub.")
    
    def run_container(self) -> None:
        raise NotImplementedError


# in the future, MLflowComponent will be in its own 3rd party library that is installable via pip
class MLflowComponent(AnacostiaComponent):
    def __init__(self, storage_dir: str) -> None:
        self.storage_dir = storage_dir
        super().__init__("0.0.0.0", "ghcr.io/mlflow/mlflow")
    
    def run_container(self) -> None:
        BACKEND_STORE_URI = "file:///app/storage"
        ARTIFACT_ROOT = "/app/storage" 
        CONTAINER_PORT = 5000
        CONTAINER_NAME = "mlflow-component"

        if is_container_running(CONTAINER_NAME) is False:
            print(f"Starting container {CONTAINER_NAME}.")

            self.client.containers.run(
                name=CONTAINER_NAME,
                image=self.image_name, 
                ports={
                    CONTAINER_PORT:str(self.host_port)
                },
                environment={
                    "BACKEND_STORE_URI": BACKEND_STORE_URI,
                    "ARTIFACT_ROOT": ARTIFACT_ROOT,
                },
                volumes={
                    os.path.abspath(self.storage_dir): {"bind": ARTIFACT_ROOT, "mode": "rw"}
                },
                command=f"mlflow server --backend-store-uri {BACKEND_STORE_URI} --default-artifact-root {ARTIFACT_ROOT} --host {self.host_ip} --port {CONTAINER_PORT}",
                detach=True
            )

            print(f"Container {CONTAINER_NAME} is running on port {self.host_port}.")
            print(f"MLflow Tracking UI can be accessed at http://localhost:{self.host_port}")
        else:
            print(f"Container {CONTAINER_NAME} is already running on port {self.host_port}.")
            print(f"MLflow Tracking UI can be accessed at http://localhost:{self.host_port}")

    def create_experiment(self, name: str) -> str:
        url = f"{self.url}/api/2.0/mlflow/experiments/create"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"name": name}

        response = requests.post(url, json=parameters)
        response = json.loads(response.text)
        return response["experiment_id"]

    def get_experiment(self, experiment_id: str) -> json:
        url = f"{self.url}/api/2.0/mlflow/experiments/get"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"experiment_id": experiment_id}

        response = requests.get(url, json=parameters)
        response = json.loads(response.text)
        return response

    def delete_experiment(self, experiment_id: str) -> None:
        url = f"{self.url}/api/2.0/mlflow/experiments/delete"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"experiment_id": experiment_id}

        response = requests.post(url, json=parameters)
        response = json.loads(response.text)

        if response != {}:
            print(response)
    
    def restore_experiment(self, experiment_id: str) -> None:
        url = f"{self.url}/api/2.0/mlflow/experiments/restore"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"experiment_id": experiment_id}

        response = requests.post(url, json=parameters)
        response = json.loads(response.text)

        if response != {}:
            print(response)
    
    def update_experiment(self, experiment_id: str, new_name: str) -> None:
        url = f"{self.url}/api/2.0/mlflow/experiments/update"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"experiment_id": experiment_id, "new_name": new_name}

        response = requests.post(url, json=parameters)
        response = json.loads(response.text)

        if response != {}:
            print(response)
    
    def create_run(self, experiment_id: str, run_name: str) -> str:
        url = f"{self.url}/api/2.0/mlflow/runs/create"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {
            "experiment_id": experiment_id, 
            "run_name": run_name,
            "start_time": int(time.time() * 1000)
        }

        response = requests.post(url, json=parameters)
        response = json.loads(response.text)

        run_id = response["run"]["info"]["run_id"]
        return run_id
    
    def get_run(self, run_id: str) -> json:
        url = f"{self.url}/api/2.0/mlflow/runs/get"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"run_id": run_id}

        response = requests.get(url, json=parameters)
        response = json.loads(response.text)
        return response
    
    def delete_run(self, run_id: str) -> None:
        url = f"{self.url}/api/2.0/mlflow/runs/delete"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"run_id": run_id}

        response = requests.post(url, json=parameters)
        response = json.loads(response.text)

        if response != {}:
            print(response)
    
    def restore_run(self, run_id: str) -> None:
        url = f"{self.url}/api/2.0/mlflow/runs/restore"

        # in the future, we might just want to pass in a dictionary of parameters
        parameters = {"run_id": run_id}

        response = requests.post(url, json=parameters)
        response = json.loads(response.text)

        if response != {}:
            print(response)

    def log_metrics(self, run_id: str, **kwargs) -> None:
        url = f"{self.url}/api/2.0/mlflow/runs/log-batch"

        metrics = []
        for key, value in kwargs.items():
            # TODO: possibly add support for recording step number
            metrics.append({"key": key, "value": value, "timestamp": int(time.time() * 1000)})

        payload = {
            "run_id": run_id,
            "metrics": metrics,
        }

        response = requests.post(url, json=payload)
        response = json.loads(response.text)

        if response != {}:
            print(response)
    
    def log_params(self, run_id: str, **kwargs) -> None:
        url = f"{self.url}/api/2.0/mlflow/runs/log-batch"

        params = []
        for key, value in kwargs.items():
            params.append({"key": key, "value": str(value)})

        payload = {
            "run_id": run_id,
            "params": params,
        }

        response = requests.post(url, json=payload)
        response = json.loads(response.text)

        if response != {}:
            print(response)
    
    def set_tags(self, run_id: str, **kwargs) -> None:
        url = f"{self.url}/api/2.0/mlflow/runs/log-batch"

        tags = []
        for key, value in kwargs.items():
            tags.append({"key": key, "value": str(value)})

        payload = {
            "run_id": run_id,
            "tags": tags,
        }

        response = requests.post(url, json=payload)
        response = json.loads(response.text)

        if response != {}:
            print(response)
    
    def delete_tags(self, run_id: str, tags: List[str]) -> None:
        url = f"{self.url}/api/2.0/mlflow/runs/delete-tag"

        for tag in tags:
            payload = {
                "run_id": run_id,
                "key": tag,
            }

            response = requests.post(url, json=payload)
            response = json.loads(response.text)

            if response != {}:
                print(response)

    def log_model(self, run_id: str, model_path: str, model_name: str, **kwargs) -> None:
        command = f"python /app/storage/script.py"
        mlflow_container = self.client.containers.get(self.container_name)
        exec_results = mlflow_container.exec_run(cmd=command)
        print(exec_results.output.decode("utf-8"))


from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
import pickle

if __name__ == "__main__":
    component = MLflowComponent("../anacostia-components/storage")
    
    """
    # Load the diabetes dataset.
    db = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

    # Create and train models.
    rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
    rf.fit(X_train, y_train)

    # Use the model to make predictions on the test dataset.
    predictions = rf.predict(X_test)
    print(predictions)

    # save the model in the native sklearn format
    filename = "../anacostia-components/storage/random_forest.pkl"
    pickle.dump(rf, open(filename, "wb"))

    component.set_tags(
        "4d6f7387b1714494913fd8fdadec4fd4",
        tag1="value1"
    )
    """

    component.log_model(
        "4d6f7387b1714494913fd8fdadec4fd4",
        "/app/storage/models/random_forest.pkl",
        "random_forest_v1"
    )