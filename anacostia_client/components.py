import docker
from utils import is_container_running
import requests
import os
import time
from typing import Dict, Any
from urllib.parse import urlparse


# TODO: remove this function with utils.find_available_port()
def find_available_port_flask() -> int:
    return 8001

def find_available_port_mlflow() -> int:
    return 5001

class AnacostiaComponent(object):
    def __init__(self, host_ip: str, image_name: str) -> None:
        self.host_ip = host_ip

        self.client = docker.from_env()
        self.image_name = image_name
        self.container_name = "mlflow-test"
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

    CONTAINER_NAME = "Anacostia-MLflow"
    ANACOSTIA_HOST_PORT=str(find_available_port_flask())
    MLFLOW_HOST_PORT=str(find_available_port_mlflow())
    MLFLOW_DEFAULT_ARTIFACT_ROOT="/artifacts"
    MLFLOW_BACKEND_STORE="/mlruns"

    def __init__(self, backend_store: str = None, artifacts: str = None, git_repo: str = None) -> None:

        # create volumes if the value for backend_store and artifacts are not URIs
        self.volumes = {}

        if urlparse(backend_store).scheme == "":
            if os.path.isdir(backend_store):
                self.volumes[os.path.abspath(backend_store)] = {"bind": self.MLFLOW_BACKEND_STORE, "mode": "rw"}

        if urlparse(artifacts).scheme == "":
            if os.path.isdir(artifacts):
                self.volumes[os.path.abspath(artifacts)] = {"bind": self.MLFLOW_DEFAULT_ARTIFACT_ROOT, "mode": "rw"}   

        if git_repo is not None:
            if os.path.isdir(git_repo) and git_repo.endswith(".git"):
                git_dir = os.path.abspath(git_repo)
                git_parent_dir = git_dir.replace(".git", "")
                self.volumes[git_parent_dir] = {"bind": "/client_project/", "mode": "rw"}       

        super().__init__("0.0.0.0", "mdo6180/mlflow-component:latest")

    def run_container(self) -> None:
        if is_container_running(self.CONTAINER_NAME) is False:
            print(f"Starting container {self.CONTAINER_NAME}.")

            container = self.client.containers.run(
                name=self.CONTAINER_NAME,
                image=self.image_name,
                ports={
                    5000: self.MLFLOW_HOST_PORT,        # MLflow Tracking UI, container port 5000 is mapped to host port specified by pipeline
                    8000: self.ANACOSTIA_HOST_PORT      # Anacostia API, container port 8000 is mapped to host port specified by pipeline
                },
                volumes=self.volumes,
                command="mlflow server",
                detach=True
            )

            container.exec_run("python main.py", detach=True)

            print(f"{self.CONTAINER_NAME} component is running on http://localhost:{self.ANACOSTIA_HOST_PORT}.")
            print(f"MLflow Tracking UI can be accessed at http://localhost:{self.MLFLOW_HOST_PORT}")

        else:
            print(f"{self.CONTAINER_NAME}  is already running on http://localhost:{self.ANACOSTIA_HOST_PORT}.")
            print(f"MLflow Tracking UI can be accessed at http://localhost:{self.MLFLOW_HOST_PORT}")

    def create_experiment(self, experiment_name: str, tags: Dict[str, Any] = None) -> None:
        # we have to run this inside a while loop because although the container is running, 
        # the Anacostia Flask API in the container might not be ready to accept requests
        while True:
            try:
                url = f"http://localhost:{self.ANACOSTIA_HOST_PORT}/create-experiment"

                data = {"name": experiment_name}

                if tags is not None:
                    data["tags"] = tags

                response = requests.post(url=url, json=data)
                print(response.text)
                return

            except Exception as e:
                time.sleep(0.5)


if __name__ == "__main__":
    component = MLflowComponent(
        backend_store="../anacostia-components/mlruns", 
        artifacts="../anacostia-components/mlflow",
        git_repo="../.git"
    )
    component.create_experiment(
        experiment_name="sixteenth-experiment",
        tags={"version": "v1", "priority": "P1"}
    )
