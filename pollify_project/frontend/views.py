from django.shortcuts import render
from django.db.models import Count
from polls.models import Poll
from comments.models import Comment

def home(request):
    recent_polls = Poll.objects.order_by('-created_at')[:6]
    recent_comments = Comment.objects.select_related('poll').order_by('-created_at')[:5]

    # Ensure distinct counting of votes and comments
    trending_polls = (
        Poll.objects.annotate(
            vote_count=Count('votes', distinct=True),
            comment_count=Count('comments', distinct=True),
            total_interactions=Count('votes', distinct=True) + Count('comments', distinct=True)
        )
        .filter(total_interactions__gte=1)
        .order_by('-total_interactions')
    )

    return render(request, "home.html", {
        "recent_polls": recent_polls,
        "recent_comments": recent_comments,
        "trending_polls": trending_polls,
    })