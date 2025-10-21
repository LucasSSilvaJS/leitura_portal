import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=Config.SCHEDULER_TIMEZONE)

    def start_weekly_monday_9am(self, func):
        # Monday at 9:00
        trigger = CronTrigger(day_of_week='mon', hour=9, minute=0)
        self.scheduler.add_job(func, trigger, id="monday_9am_job", replace_existing=True)
        self.scheduler.start()
        logger.info("Scheduler started: job scheduled every Monday at 9:00 (%s)", Config.SCHEDULER_TIMEZONE)

    def shutdown(self):
        self.scheduler.shutdown(wait=False)
