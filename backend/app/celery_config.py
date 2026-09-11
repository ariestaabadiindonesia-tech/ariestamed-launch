from celery.beat import ScheduleEntry
from celery.schedules import crontab
from app.tasks.post_tasks import process_scheduled_posts
from app.tasks.analytics_tasks import refresh_all_analytics

# Celery Beat Schedule
class Config:
    CELERY_BEAT_SCHEDULE = {
        'process-scheduled-posts': {
            'task': 'app.tasks.post_tasks.process_scheduled_posts',
            'schedule': crontab(minute='*/5'),  # Every 5 minutes
        },
        'refresh-analytics': {
            'task': 'app.tasks.analytics_tasks.refresh_all_analytics',
            'schedule': crontab(minute=0, hour='*/4'),  # Every 4 hours
        },
    }
