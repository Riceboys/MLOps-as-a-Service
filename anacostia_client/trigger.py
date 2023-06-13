import os
import sys
sys.path.append("..")
from anacostia_client import scheduler, lock

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger
from collections.abc import Callable


class AnacostiaTrigger:
    def __init__(
            self, 
            trigger_name: str,  
            stages: list[str] | str = "all",
            trigger_schedule: BaseTrigger = IntervalTrigger(seconds=1),
            trigger_function: Callable[..., bool] = None
        ) -> None:
        
        self.trigger_name = trigger_name
        self.trigger_schedule = trigger_schedule
        self.trigger_result = False
        self.trigger_function = trigger_function
        scheduler.add_job(self.wrapper, self.trigger_schedule, id=self.trigger_name)
        print(f"Trigger {self.trigger_name} is running")
    
    def wrapper(self):
        with lock:
            if self.trigger_function is not None:
                self.trigger_result = self.trigger_function()
            else:
                self.trigger_result = True

    def run(self):
        scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                with lock:
                    if self.trigger_result:
                        # replace the following print statement with function to trigger endpoint
                        print(f"{self.trigger_name} triggered")
                        self.trigger_result = False

        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()
            print(f"\nTrigger {self.trigger_name} stopped")


import random

def trigger_func() -> bool:
    num = random.randint(1, 10)
    if num <= 5:
        print(f"random number <= 5: {num}")
        return True
    else:
        print(f"random number > 5: {num}")
        return False

if __name__ == '__main__':
    train_trigger = AnacostiaTrigger(
        "train_trigger", 
        trigger_schedule=IntervalTrigger(seconds=3), 
        trigger_function=trigger_func
    )
    train_trigger.run()