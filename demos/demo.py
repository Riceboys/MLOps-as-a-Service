import sys
sys.path.append("../anacostia_client")
from pipeline import AnacostiaPipeline
from trigger import AnacostiaBaseTrigger
from apscheduler.triggers.interval import IntervalTrigger
import random
import time

def trigger_func() -> bool:
    num = random.randint(1, 10)
    if num <= 5:
        print(f"random number <= 5: {num}")
        return True
    else:
        print(f"random number > 5: {num}")
        return False

def prepare_data():
    time.sleep(5)
    print("data preparation in progress...")

def train_model():
    time.sleep(5)
    print("model training in progress...")

def validate_model():
    time.sleep(5)
    print("model validation in progress...")

if __name__ == '__main__':
    prepare_data_trigger = AnacostiaBaseTrigger(
        "pipeline_trigger", 
        trigger_schedule=IntervalTrigger(seconds=5), 
        action_functions=[prepare_data],
        task_description="Run data preparation stage of the pipeline"
    )

    train_trigger = AnacostiaBaseTrigger(
        "train_validate_trigger", 
        trigger_schedule=IntervalTrigger(seconds=5), 
        action_functions=[train_model, validate_model],
        task_description="Run training and validation stages of the pipeline"
    )

    pipeline = AnacostiaPipeline(components=None, triggers=[prepare_data_trigger, train_trigger])
    pipeline.run()