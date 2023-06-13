import api
import client
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock

scheduler = BackgroundScheduler()
lock = Lock()

running = True