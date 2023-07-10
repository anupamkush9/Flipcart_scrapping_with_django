import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_scrapping.settings')

app =  Celery('web_scrapping')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# app.conf.beat_schedule = {
#     'every-5-seconds': {
#         'task': "data_store.scrapper_file.scrapper", # path of the task
#         "schedule": 10,
#     }
   
# }