from apscheduler.schedulers.background import BackgroundScheduler
from kink import inject


@inject
class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = list()

    def add_job(self, func, trigger, **kwargs):
        print(f"Adding job for {func.__name__}, {trigger}, {kwargs}")
        job = self.scheduler.add_job(func, trigger, **kwargs)
        self.jobs.append(job)
        return job

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()
