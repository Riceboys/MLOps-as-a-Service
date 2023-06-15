from constants import scheduler, lock, colors
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger
from collections.abc import Callable


class AnacostiaBaseTrigger:

    def __init__(
            self, 
            trigger_name: str,  
            trigger_schedule: BaseTrigger = IntervalTrigger(seconds=1),
            trigger_function: Callable[..., bool] = None,
            action_functions: list[Callable[..., any]] = None,
            task_description: str = None
        ) -> None:
        
        self.trigger_name = trigger_name
        self.trigger_schedule = trigger_schedule
        self.trigger_function = trigger_function
        self.action_functions = action_functions
        self.task_description = task_description

        self.trigger_result = False
        self.action_functions_status = 0
        
        scheduler.add_job(self.wrapper, self.trigger_schedule, id=self.trigger_name)
        print(f"Trigger {self.trigger_name} is running")
    
    def wrapper(self):
        with lock:
            if self.trigger_function is not None:
                self.trigger_result = self.trigger_function()
            else:
                self.trigger_result = True

    def run(self):
        with lock:
            # if the trigger function returns True, we're executing the action functions
            if self.trigger_result:

                # we're pausing the trigger to allow the action functions to run
                self.trigger_result = False
                scheduler.pause_job(self.trigger_name)

                print(
                    "{}{} started...{}".format(
                        colors["OKGREEN"],
                        self.task_description,
                        colors["ENDC"]
                    )
                )

                # executing the action functions
                for func in self.action_functions:
                    func()
                
                print(
                    "{}{} ended...{}".format(
                        colors["OKGREEN"],
                        self.task_description,
                        colors["ENDC"]
                    )
                )

                # once action functions are done, we're resuming the trigger running as scheduled
                scheduler.resume_job(self.trigger_name)


class AnacostiaPrepTrigger:

    def __init__(
            self, 
            trigger_name: str,  
            trigger_schedule: BaseTrigger = IntervalTrigger(seconds=1),
            trigger_function: Callable[..., bool] = None,
            action_functions: list[Callable[..., any]] = None,
            task_description: str = None
        ) -> None:
        
        self.trigger_name = trigger_name
        self.trigger_schedule = trigger_schedule
        self.trigger_function = trigger_function
        self.action_functions = action_functions
        self.task_description = task_description

        self.trigger_result = False
        self.action_functions_status = 0
        
        scheduler.add_job(self.wrapper, self.trigger_schedule, id=self.trigger_name)
        print(f"Trigger {self.trigger_name} is running")
    
    def wrapper(self):
        with lock:
            if self.trigger_function is not None:
                self.trigger_result = self.trigger_function()
            else:
                self.trigger_result = True

    def run(self):
        with lock:
            # if the trigger function returns True, we're executing the action functions
            if self.trigger_result:

                # we're pausing the trigger to allow the action functions to run
                self.trigger_result = False
                scheduler.pause_job(self.trigger_name)

                print(
                    "{}{} started...{}".format(
                        colors["OKGREEN"],
                        self.task_description,
                        colors["ENDC"]
                    )
                )

                # executing the action functions
                for func in self.action_functions:
                    func()
                
                print(
                    "{}{} ended...{}".format(
                        colors["OKGREEN"],
                        self.task_description,
                        colors["ENDC"]
                    )
                )

                # once action functions are done, we're resuming the trigger running as scheduled
                scheduler.resume_job(self.trigger_name)


class AnacostiaTrainTrigger:

    def __init__(
            self, 
            trigger_name: str,  
            trigger_schedule: BaseTrigger = IntervalTrigger(seconds=1),
            trigger_function: Callable[..., bool] = None,
            action_functions: list[Callable[..., any]] = None,
            task_description: str = None
        ) -> None:
        
        self.trigger_name = trigger_name
        self.trigger_schedule = trigger_schedule
        self.trigger_function = trigger_function
        self.action_functions = action_functions
        self.task_description = task_description

        self.trigger_result = False
        self.action_functions_status = 0
        
        scheduler.add_job(self.wrapper, self.trigger_schedule, id=self.trigger_name)
        print(f"Trigger {self.trigger_name} is running")
    
    def wrapper(self):
        with lock:
            if self.trigger_function is not None:
                self.trigger_result = self.trigger_function()
            else:
                self.trigger_result = True

    def run(self):
        with lock:
            # if the trigger function returns True, we're executing the action functions
            if self.trigger_result:

                # we're pausing the trigger to allow the action functions to run
                self.trigger_result = False
                scheduler.pause_job(self.trigger_name)

                print(
                    "{}{} started...{}".format(
                        colors["OKGREEN"],
                        self.task_description,
                        colors["ENDC"]
                    )
                )

                # executing the action functions
                for func in self.action_functions:
                    func()
                
                print(
                    "{}{} ended...{}".format(
                        colors["OKGREEN"],
                        self.task_description,
                        colors["ENDC"]
                    )
                )

                # once action functions are done, we're resuming the trigger running as scheduled
                scheduler.resume_job(self.trigger_name)