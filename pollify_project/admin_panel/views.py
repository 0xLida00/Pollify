from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from polls.models import Poll
from comments.models import Comment
from users.models import User
from .models import ActivityLog

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user, login_url='/login/')
def dashboard(request):
    """Admin dashboard view with recent activity logs paginated."""
    user_count = User.objects.count()
    poll_count = Poll.objects.count()
    comment_count = Comment.objects.count()

    # Apply filtering by user (if filter is passed)
    filter_user_id = request.GET.get('user')
    if filter_user_id:
        activity_logs = ActivityLog.objects.filter(user_id=filter_user_id).order_by('-timestamp')
    else:
        activity_logs = ActivityLog.objects.order_by('-timestamp')

    # Paginate logs - 20 per page
    paginator = Paginator(activity_logs, 20)
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