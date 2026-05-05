"""
Celery configuration for MSU Platform.

This module configures Celery for asynchronous task processing including:
- Video transcoding
- Feed generation
- Email notifications
- Scheduled tasks (periodic cleanup, etc.)
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

# Create Celery app
app = Celery('msu_platform')

# Load configuration from Django settings (CELERY_ prefixed)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to test Celery configuration."""
    print(f'Request: {self.request!r}')


# Custom Celery Beat Schedule
app.conf.beat_schedule = {
    # Refresh user feeds every hour
    'refresh-user-feeds': {
        'task': 'apps.organizations.tasks.refresh_user_feeds',
        'schedule': 3600.0,  # 1 hour in seconds
        'options': {'expires': 3300}  # Expire if not run within 55 minutes
    },

    # Clean up old feed items daily at 2 AM
    'cleanup-old-feed-items': {
        'task': 'apps.organizations.tasks.cleanup_old_feed_items',
        'schedule': crontab(hour=2, minute=0),  # 2:00 AM daily
    },

    # Clean up failed transcoding jobs weekly
    'cleanup-failed-transcoding-jobs': {
        'task': 'apps.media.tasks.cleanup_failed_jobs',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),  # Sunday 3:00 AM
    },

    # Generate trending content daily at 1 AM
    'update-trending-content': {
        'task': 'apps.organizations.tasks.update_trending_content',
        'schedule': crontab(hour=1, minute=0),  # 1:00 AM daily
    },
}

# Task configuration
app.conf.update(
    # Task result expiration (7 days)
    result_expires=604800,

    # Task acknowledgment after task is sent
    task_acks_late=True,

    # Reject task on worker failure
    task_reject_on_worker_lost=True,

    # Prefetch multiplier (tasks to fetch at once)
    worker_prefetch_multiplier=4,

    # Task soft time limit (20 minutes)
    task_soft_time_limit=1200,

    # Task hard time limit (30 minutes)
    task_time_limit=1800,

    # Task compression
    task_compression='gzip',
    result_compression='gzip',

    # Task serialization
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',

    # Timezone
    timezone='Africa/Harare',
    enable_utc=True,
)


# Task routing (send certain tasks to specific queues)
app.conf.task_routes = {
    'apps.media.tasks.transcode_video': {'queue': 'video'},
    'apps.media.tasks.generate_thumbnail': {'queue': 'video'},
    'apps.organizations.tasks.*': {'queue': 'default'},
    'apps.core.tasks.*': {'queue': 'default'},
}


# Custom error handler
@app.task(bind=True)
def on_task_failure(self, exc, task_id, args, kwargs, einfo):
    """Handle task failure."""
    print(f'Task {task_id} failed: {exc}')
    # You can add custom error handling here (e.g., send notifications)


if __name__ == '__main__':
    app.start()
