import os
import sys
sys.path.append("..")
from anacostia_client import scheduler, lock

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger

class AnacostiaTrigger:
    def __init__(
            self, 
            trigger_name: str,  
            stages: list[str] | str = "all",
            trigger_schedule: BaseTrigger = IntervalTrigger(seconds=1)
        ) -> None:
        
        self.trigger_name = trigger_name
        self.trigger_schedule = trigger_schedule
        self.trigger_result = False
        scheduler.add_job(self.wrapper, self.trigger_schedule, id=self.trigger_name)

    def trigger_function(self):
        return True
    
    def wrapper(self):
        with lock:
            self.trigger_result = self.trigger_function()

    def run(self):
        try:
            while True:
                with lock:
                    if self.trigger_result:
                        print(f"{self.trigger_name} triggered")
                        self.trigger_result = False
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()


import random

def tick():
    num = random.randint(1, 10)
    if num <= 5:
        print(f"random number <= 5: {num}")
        return True
    else:
        print(f"random number > 5: {num}")
        return False

# once wrapper is put inside of a class, val is no longer global
val = False
def wrapper():
    global val
    with lock:
        val = tick()

if __name__ == '__main__':
    job1 = scheduler.add_job(wrapper, trigger=IntervalTrigger(seconds=3), id='job1')
    print(f"job_id: {job1.id}")

    # call scheduler.start() after all the triggers have been added
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            with lock:
                if val:
                    print("val is true")
                    val = False
            #time.sleep(2)

    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()