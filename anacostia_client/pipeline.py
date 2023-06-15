from trigger import AnacostiaBaseTrigger
from client import AnacostiaComponent
from constants import scheduler
import sys
import os


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
            print(f"\nTrigger {trigger.trigger_name} removed")
    
    def run(self) -> None:
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
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
                        print("\nPipeline shutdown complete")
                        sys.exit(0)

                    elif user_input == "2":
                        pass

                    else:
                        self.resume_triggers()
                        continue
                else:
                    self.resume_triggers()
                    continue

# notes:
# - pipeline should be able to run multiple triggers
# - pipeline should be able to download, set up, and run multiple components
# - pipeline should be able to run multiple triggers and components in parallel and sequence
# - when one trigger stops, the pipeline should be able to continue running other triggers
# - when one component stops, the pipeline should be able to continue running other components
# - when a trigger's action functions are running, the trigger schedule should be paused until all the action functions are finished running
# - when a trigger's action functions are running, other triggers' action functions and trigger schedule should be able to run unaffected
# - when one trigger stops, the pipeline should be able to continue running the action functions of the other triggers
