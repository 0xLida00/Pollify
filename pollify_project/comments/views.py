from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from polls.models import Poll
from .models import Comment, CommentVote

def add_comment(request, poll_id):
    if request.method == "POST":
        poll = get_object_or_404(Poll, id=poll_id)
        content = request.POST.get("content")
        if content:
            Comment.objects.create(poll=poll, author=request.user, content=content)
        return redirect("poll_detail", pk=poll_id)


@csrf_exempt
@login_required
def vote_comment(request, comment_id, vote_type):
    """Handles upvoting and downvoting while preventing multiple votes per user."""
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Check if user already voted
    existing_vote = CommentVote.objects.filter(user=user, comment=comment).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            return JsonResponse({"success": False, "message": "You have already voted this way."}, status=400)
        else:
            # Remove previous vote
            if existing_vote.vote_type == "upvote":
                comment.upvotes -= 1
            else:
                comment.downvotes -= 1
            existing_vote.delete()

    # Register new vote
    CommentVote.objects.create(user=user, comment=comment, vote_type=vote_type)

    if vote_type == "upvote":
        comment.upvotes += 1
    elif vote_type == "downvote":
        comment.downvotes += 1

    comment.save()
    return JsonResponse({"success": True, "upvotes": comment.upvotes, "downvotes": comment.downvotes})