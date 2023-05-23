from flask import request
from mlops_decorators import MLOpsPipeline


pipeline = MLOpsPipeline()

@pipeline.train("started training", "training ended", "OKBLUE")
def receive_command():
    print("loading data")


if __name__ == "__main__":
    #pipeline.run()
    #receive_command()
    print("done main")
