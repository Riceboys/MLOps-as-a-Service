import docker
from utils import *
import requests
import json
import os


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
                    CONTAINER_PORT:f"{self.host_port}" 
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
        else:
            print(f"Container {CONTAINER_NAME} is already running on port {self.host_port}.")

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


if __name__ == "__main__":
    component = MLflowComponent(8080, "../anacostia-components/storage")
    experiment_id = component.create_experiment("test")
    print(component.get_experiment(experiment_id))