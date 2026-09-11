from celery import Celery
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Task definitions
from app.tasks import post_tasks, content_tasks, analytics_tasks

@celery.task
def test_task():
    return "Celery is working!"
