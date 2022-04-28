import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import datetime
from datetime import timedelta, date
from apps.transaction.models import Transaction
from apps.my_scheduler.views import *

logger = logging.getLogger(__name__)


def my_job():
    saiki = datetime.datetime.now()
    print(f"-------- Saiki {saiki.strftime('%m/%d/%Y, %H:%M:%S')} ------------")
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_midnight = datetime.datetime.combine(tomorrow, datetime.datetime.min.time())
    tm = tomorrow_midnight.strftime("%Y-%m-%d %H:%M:%S")
    transactions = Transaction.objects.filter(date_return=tm, status=True)
    print(f"due data : {transactions}")
    for t in transactions:
      print(f"Name : {t.user.user.first_name} {t.user.user.last_name} --- {t.user.nik}")
      print(f"book : {t.borrows.all()}\n")



def due_date_notification():
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_midnight = datetime.datetime.combine(tomorrow, datetime.datetime.min.time())
    tm = tomorrow_midnight.strftime("%Y-%m-%d %H:%M:%S")
    transactions = Transaction.objects.filter(date_return=tm, status=True)
    print(f"------ DUE TO DATA : {transactions} --------")
    for t in transactions:
      print(f"Name : {t.user.user.first_name} {t.user.user.last_name} --- {t.user.nik}")
      print(f"book : {t.borrows.all()} \n")
      send_due_date_mail(t)

def fine_notification():
    pass

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.  
def delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)




class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # scheduler.add_job(
    #   my_job,
    #   trigger=CronTrigger(second="*/10"),  # Every 10 seconds
    #   id="sekarang",  # The `id` assigned to each job MUST be unique
    #   replace_existing=True,
    # )
    # logger.info("Added job 'my_job'.")

    scheduler.add_job(
      due_date_notification,
      trigger=CronTrigger(
        day_of_week='mon-fri', hour='23', minute='35',
      ),  # Midnight on Monday, before start of the next work week.
      id="due_date_notification",
      max_instances=1,
      replace_existing=True,
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")
    return scheduler