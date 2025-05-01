from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


class BackgroundJobsAppConfig(AppConfig):
    name = "background_jobs_app"

    def ready(self):
        from schedule.tasks import delete_old_schedules

        scheduler = BackgroundScheduler()
        scheduler.add_job(delete_old_schedules, "interval", days=1)
        scheduler.start()

        atexit.register(lambda: scheduler.shutdown(wait=False))
