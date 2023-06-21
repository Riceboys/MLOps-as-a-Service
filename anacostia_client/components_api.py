import docker
from utils import *
import requests
import json
import os
import time
from typing import List, Dict, Any


class AnacostiaComponent(object):
    def __init__(self, host_ip: str, host_port: int, image_name: str) -> None:
        self.host_ip = host_ip
        self.host_port = host_port
        self.url = f"http://{host_ip}:{host_port}"

        self.client = docker.from_env()
        self.image_name = image_name
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


class MLflowComponent(AnacostiaComponent):
    def __init__(self, host_port: int, storage_dir: str) -> None:
        self.storage_dir = storage_dir
        super().__init__("0.0.0.0", host_port, "ghcr.io/mlflow/mlflow")
    
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


if __name__ == "__main__":
    component = MLflowComponent(8080, "../anacostia-components/storage")
    
    component.delete_tags(
        "4d6f7387b1714494913fd8fdadec4fd4",
        ["tag1", "tag2"]
    )