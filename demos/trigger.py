import time
import os
import signal
from multiprocessing import Process


running = True

class AnacostiaTrigger:
    def __init__(self, trigger_name: str, trigger_schedule: str = None) -> None:
        self.t = None
        self.trigger_name = trigger_name
        self.trigger_schedule = trigger_schedule
        
        # Register the signal handler to capture termination signals
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def trigger(self) -> bool:
        raise NotImplementedError
    
    def run(self) -> None:
        global running
        print(f"Trigger {self.trigger_name} is running")
        while running:
            if self.trigger() is True:
                print(f"Trigger {self.trigger_name} has executed")
            else:
                print(f"Trigger {self.trigger_name} has not executed")

    def stop(self, signal, frame) -> None:
        print(f"\nStopping {self.trigger_name} trigger")
    
    def __call__(self):
        self.t = Process(target=self.run, daemon=True)
        self.t.start()
        self.t.join()
        
class FolderFileCountTrigger(AnacostiaTrigger):
    def __init__(self, path: str, threshold: int = 0) -> None:
        super().__init__("Training Trigger")
        self.path = path
        self.threshold = threshold

    def trigger(self) -> bool:
        time.sleep(3)
        files = [files for root, dirs, files in os.walk(self.path)][0]
        num_files = len(files)
        return num_files > self.threshold


if __name__ == "__main__":
    file_trigger = FolderFileCountTrigger("./data", 0)
    file_trigger()
