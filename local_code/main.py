from mlops_pipeline import MLOpsPipeline


pipeline = MLOpsPipeline()

@pipeline.train("training started", "trainind ended", "OKBLUE")
def receive_command():
    print("training model now")
    return None

if __name__ == "__main__":
    pipeline.run()