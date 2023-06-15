from trigger import AnacostiaBaseTrigger
from client import AnacostiaComponent
from anacostia_client import scheduler
import sys


class AnacostiaPipeline(object):
    def __init__(self, components: list[AnacostiaComponent], triggers: list[AnacostiaBaseTrigger]) -> None:
        self.triggers = triggers
        self.components = components
        scheduler.start()
    
    def pause_triggers(self) -> None:
        for trigger in self.triggers:
            scheduler.pause_job(trigger.trigger_name)
            print(f"\nTrigger {trigger.trigger_name} paused")
    
    def resume_triggers(self) -> None:
        for trigger in self.triggers:
            scheduler.resume_job(trigger.trigger_name)
            print(f"\nTrigger {trigger.trigger_name} resumed")
    
    def remove_triggers(self) -> None:
        for trigger in self.triggers:
            scheduler.remove_job(trigger.trigger_name)
    
    def run(self) -> None:
        while True:
            try:
                for trigger in self.triggers:
                    trigger.run()

            except (KeyboardInterrupt):
                self.pause_triggers()

                user_input = input(f"\nAre you sure you want to stop the pipeline? (y/n): ")
                if user_input == "y":

                    user_input = input(f"Enter (1) for hard stop, enter (2) for soft stop, press Enter to abort: ")
                    if user_input == "1":

                        self.remove_triggers()
                        scheduler.shutdown()
                        sys.exit(0)

                    elif user_input == "2":
                        pass

                    else:
                        self.resume_triggers()
                        continue
                else:
                    self.resume_triggers()
                    continue

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
    train_trigger = AnacostiaBaseTrigger(
        "pipeline_trigger", 
        trigger_schedule=IntervalTrigger(seconds=3), 
        trigger_function=trigger_func,
        action_functions=[prepare_data, train_model, validate_model],
        task_description="Run training pipeline"
    )

    pipeline = AnacostiaPipeline(components=None, triggers=[train_trigger])
    pipeline.run()