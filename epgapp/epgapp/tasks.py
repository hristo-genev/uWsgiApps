
import datetime
import logging
import celery
#from celery.schedules import crontab
import requests
from epgapp.models import Scheduler

logger = logging.getLogger(__name__)

@celery.decorators.periodic_task(run_every=celery.schedules.crontab(minute="*")) #minute=30, hour=2)) # run every day at 2:30

def runAllGrabbers():
  logger.debug('Starting scheduled task.')
  logger.debug(datetime.datetime.now + ': Running all grabbers')
  #r = requests.get('http://epgapp.kodibg.org/run/all/1')
  #logger.debug(r.text)
  id = Scheduler.objects.first().id
  logger.debug('id: %s' % id)
