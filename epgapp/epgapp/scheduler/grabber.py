from datetime import datetime
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

def grag():
  logger.debug("grab() executed" + datetime.now())

def start():
  scheduler = BackgroundScheduler()
  scheduler.add_job(grab, 'interval', minutes=1)
  scheduler.start()
  logger.debug("start() executed")
