from celery.schedules import crontab

# Redis URLs
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"

# Timezone
timezone = "Asia/Kolkata"
enable_utc = False  # Set this to False to respect local timezone

# Task result config
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
result_expires = 3600  # Optional: results expire in 1 hour
task_track_started = True  # Optional: lets you see "STARTED" status

# Broker connection retry
broker_connection_retry_on_startup = True

# Scheduled Tasks (optional, good if using Celery Beat)
beat_schedule = {
    'daily-reminder': {
        'task': 'daily_reminder_googlechat',
        'schedule': crontab(hour=21, minute=0),  # 9 PM IST daily
    },
    'monthly-report': {
        'task': 'monthly_html_report',
        'schedule': crontab(day_of_month=1, hour=8, minute=0),
    }
}
