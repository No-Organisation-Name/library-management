from django.apps import AppConfig
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings


apip_scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

def start():
    apip_scheduler.add_jobstore(DjangoJobStore(), "default")
    apip_scheduler.start()




class MySchedulerConfig(AppConfig):
    name = 'my_scheduler'

    def ready():
        start()
