from admin_panel.models import ActivityLog

def log_activity(user, action):
    """Logs an activity for a user."""
    ActivityLog.objects.create(user=user, action=action)