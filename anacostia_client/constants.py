from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.base import BaseJobStore
from threading import Lock


scheduler = BackgroundScheduler(
    job_defaults={"max_instances": 4},
    #executors={"default": ProcessPoolExecutor(4)}
)

lock = Lock()

colors = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m"
}
