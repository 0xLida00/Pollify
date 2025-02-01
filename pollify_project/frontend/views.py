from django.shortcuts import render
from polls.models import Poll
from comments.models import Comment

def home(request):
    recent_polls = Poll.objects.order_by('-created_at')[:5]  # Get the 5 most recent polls
    recent_comments = Comment.objects.select_related('poll', 'author').order_by('-created_at')[:5]  # Recent 5 comments

    context = {
        'recent_polls': recent_polls,
        'recent_comments': recent_comments,
    }
    return render(request, 'frontend/home.html', context)