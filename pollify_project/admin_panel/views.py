from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from polls.models import Poll
from comments.models import Comment
from users.models import User
from .models import ActivityLog

@staff_member_required
def dashboard(request):
    """Admin dashboard view with recent activity logs paginated."""
    user_count = User.objects.count()
    poll_count = Poll.objects.count()
    comment_count = Comment.objects.count()

    activity_logs = ActivityLog.objects.order_by('-timestamp')

    # Paginate logs - 20 per page
    paginator = Paginator(activity_logs, 15)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.get_page(1)

    context = {
        'user_count': user_count,
        'poll_count': poll_count,
        'comment_count': comment_count,
        'recent_activity': page_obj,
    }

    return render(request, 'admin_panel/dashboard.html', context)