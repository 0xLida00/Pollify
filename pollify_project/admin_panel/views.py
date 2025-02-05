from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from polls.models import Poll
from comments.models import Comment
from users.models import User
from .models import ActivityLog

@staff_member_required
def dashboard(request):
    """Admin dashboard view."""
    user_count = User.objects.count()
    poll_count = Poll.objects.count()
    comment_count = Comment.objects.count()

    # Fetch and categorize logs by type (for better display)
    activity_logs = ActivityLog.objects.order_by('-timestamp')[:20]

    context = {
        'user_count': user_count,
        'poll_count': poll_count,
        'comment_count': comment_count,
        'recent_activity': activity_logs,
    }

    return render(request, 'admin_panel/dashboard.html', context)