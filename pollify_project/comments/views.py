from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from polls.models import Poll
from .models import Comment, CommentVote

@login_required
def add_comment(request, poll_id):
    """Add a new comment to a poll."""
    if request.method == "POST":
        poll = get_object_or_404(Poll, id=poll_id)
        content = request.POST.get("content", "").strip()  # Remove leading/trailing whitespace
        if content:  # Ensure content is not empty
            Comment.objects.create(poll=poll, author=request.user, content=content)
        return redirect("poll_detail", pk=poll_id)

from django.db import IntegrityError

@csrf_exempt
@login_required
def vote_comment(request, comment_id, vote_type):
    """Handle voting on a comment with better concurrency support."""
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    try:
        # Use `get_or_create` to handle cases where there might be a race condition
        comment_vote, created = CommentVote.objects.get_or_create(user=user, comment=comment, defaults={'vote_type': vote_type})

        if not created:
            # User has already voted; check if they are trying to change their vote
            if comment_vote.vote_type == vote_type:
                # Silently return if the same vote is submitted
                return JsonResponse({"success": True, "upvotes": comment.upvotes, "downvotes": comment.downvotes})

            # Update vote type and adjust counts
            if comment_vote.vote_type == "upvote":
                comment.upvotes -= 1
            elif comment_vote.vote_type == "downvote":
                comment.downvotes -= 1

            comment_vote.vote_type = vote_type
            comment_vote.save()
        
        # Update the new vote count
        if vote_type == "upvote":
            comment.upvotes += 1
        elif vote_type == "downvote":
            comment.downvotes += 1

        comment.save()

    except IntegrityError:
        return JsonResponse({"success": False, "message": "An error occurred. Please try again later."}, status=500)

    return JsonResponse({"success": True, "upvotes": comment.upvotes, "downvotes": comment.downvotes})