import sys
sys.path.append("../anacostia-client")

from api import MLOpsPipeline
import schedule


pipeline = MLOpsPipeline()

@pipeline.train("training started", "trainind ended", "OKBLUE")
def train_model():
    print("training model now")
    return None

@pipeline.prepare_data("started preparing data", "finished preparing data", "OKGREEN")
def prepare_data():
    print("preparing data now")
    return None


if __name__ == "__main__":
    cron_expr = "0/5 0 0 ? * * *"
    pipeline.run()
