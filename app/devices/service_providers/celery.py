from celery import Celery
from devices.config.config import Config

celery_app = Celery("worker", broker=Config.AMQP_URI)

celery_app.conf.task_routes = {"devices.celery_tasks.tasks.*": "rule_executor"}
