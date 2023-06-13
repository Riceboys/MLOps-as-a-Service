import os
import sys
sys.path.append("..")
from anacostia_client import scheduler, lock

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger
from collections.abc import Callable
from multiprocessing import Process


class AnacostiaBaseTrigger:
    colors = {
        "HEADER": "\033[95m",
        "OKBLUE": "\033[94m",
        "OKCYAN": "\033[96m",
        "OKGREEN": "\033[92m",
        "WARNING": "\033[93m",
        "FAIL": "\033[91m",
        "ENDC": "\033[0m"
    }

    def __init__(
            self, 
            trigger_name: str,  
            stages: list[str] | str = "all",
            trigger_schedule: BaseTrigger = IntervalTrigger(seconds=1),
            trigger_function: Callable[..., bool] = None,
            action_functions: list[Callable[..., any]] = None,
            task_description: str = None
        ) -> None:
        
        self.trigger_name = trigger_name
        self.trigger_schedule = trigger_schedule
        self.trigger_result = False
        self.trigger_function = trigger_function
        self.action_functions = action_functions
        self.task_description = task_description

        scheduler.add_job(self.wrapper, self.trigger_schedule, id=self.trigger_name)
        print(f"Trigger {self.trigger_name} is running")
    
    def wrapper(self):
        with lock:
            if self.trigger_function is not None:
                self.trigger_result = self.trigger_function()
            else:
                self.trigger_result = True

    def run(self):
        try:
            while True:
                with lock:
                    if self.trigger_result:
                        # we're pausing the trigger to allow the action functions to run
                        self.trigger_result = False
                        scheduler.pause_job(self.trigger_name)

                        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
                        print(
                            "{}{} started...{}".format(
                                self.colors["OKGREEN"],
                                self.task_description,
                                self.colors["ENDC"]
                            )
                        )

                        for func in self.action_functions:
                            func()
                        
                        print(
                            "{}{} ended...{}".format(
                                self.colors["OKGREEN"],
                                self.task_description,
                                self.colors["ENDC"]
                            )
                        )

                        # once action functions are done, we're resuming the trigger running as scheduled
                        scheduler.resume_job(self.trigger_name)
                        
        except (KeyboardInterrupt):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            user_input = input("\nAre you sure you want to stop the trigger? (y/n): ")
            if user_input == "y":
                user_input = input("Do you want to stop all pipeline steps? (y/n): ")
                if user_input == "y":
                    scheduler.remove_job(self.trigger_name)
                    scheduler.shutdown()
                    print(f"\nTrigger {self.trigger_name} stopped")
                    sys.exit(0)
                else:
                    pass
        except (SystemExit):
            scheduler.remove_job(self.trigger_name)
            scheduler.shutdown()
            print(f"\nTrigger {self.trigger_name} stopped")
            sys.exit(0)

    def __call__(self):
        proc = Process(target=self.run, daemon=True)
        proc.start()

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
    scheduler.start()
    train_trigger.run()