import os
from urllib.parse import urlparse


# Desc: Logging and artifact storage for Anacostia
class BaseMetricsStore:
    def __init__(self, metrics_store_uri) -> None:

        parsed_uri = urlparse(metrics_store_uri)

        if parsed_uri.scheme == "file":
            self.metrics_store_dir = parsed_uri.path

            if not os.path.isdir(self.metrics_store_dir):
                raise ValueError(f"Metrics store URI {self.metrics_store_dir} is not a directory")
            else:
                os.makedirs(os.path.join(self.metrics_store_dir, "anacostia_runs"), exist_ok=True)
        
        elif parsed_uri.scheme == "":
            self.metrics_store_dir = os.path.abspath(metrics_store_uri)

            if not os.path.isdir(self.metrics_store_dir):
                raise ValueError(f"Metrics store URI {self.metrics_store_dir} is not a directory")
            else:
                os.makedirs(os.path.join(self.metrics_store_dir, "anacostia_runs"), exist_ok=True)
        
        anacostia_dir = os.path.join(self.metrics_store_dir, "anacostia_runs")
        if os.path.exists(os.path.join(anacostia_dir, "anacostia_runs.json")) is False:
            with open(os.path.join(anacostia_dir, "anacostia_runs.json"), "w") as f:
                f.write("{}")


class MLflowMetricsStore(BaseMetricsStore):
    def __init__(self, metrics_store_uri: str) -> None:
        super().__init__(metrics_store_uri)

class ArtifactsStore:
    def __init__(self, artifact_store_uri: str) -> None:
        self.artifact_store_uri = artifact_store_uri


if __name__ == "__main__":
    filestore = MLflowMetricsStore("../demos")