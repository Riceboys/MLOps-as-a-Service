import sys
sys.path.append("../anacostia-client")
import os

from api import AnacostiaPipeline
from client import AnacostiaExecutor
import schedule

from typing import Callable


pipeline = AnacostiaPipeline()

@pipeline.train("training started", "trainind ended", "OKBLUE")
def train_model():
    print("training model now")
    return None

@pipeline.prepare_data("started preparing data", "finished preparing data", "OKGREEN")
def prepare_data():
    print("preparing data now")
    return None


if __name__ == "__main__":
    #AnacostiaExecutor(host_inbound_port=8000, host_outbound_port=12345)
    pipeline.run()

    #cron_string = "* * * * *"

    #trigger_training(count_files_in_dir, "./data", 0)

