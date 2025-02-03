from django.shortcuts import render
from django.db.models import Count
from polls.models import Poll
from comments.models import Comment

def home(request):
    recent_polls = Poll.objects.order_by('-created_at')[:6]
    recent_comments = Comment.objects.select_related('poll').order_by('-created_at')[:5]

    trending_polls = Poll.objects.annotate(
        vote_count=Count('votes'),
        comment_count=Count('comments'),
        total_interactions=Count('votes') + Count('comments')
    ).filter(total_interactions__gte=5).order_by('-total_interactions')

    return render(request, "home.html", {
        "recent_polls": recent_polls,
        "recent_comments": recent_comments,
        "trending_polls": trending_polls,
    })