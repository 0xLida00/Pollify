from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from admin_panel.utils import log_activity
from django.contrib import messages
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
            # Log the activity here
            log_activity(request.user, f"Added a comment to poll: {poll.question}")
        return redirect("poll_detail", pk=poll_id)


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

@login_required
@csrf_protect
def edit_comment(request, comment_id):
    """Edit an existing comment."""
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure only the author can edit the comment
    if comment.author != request.user:
        return HttpResponseForbidden("You do not have permission to edit this comment.")

    if request.method == "POST":
        new_content = request.POST.get("content", "").strip()
        if new_content:
            comment.content = new_content
            comment.save()
            messages.success(request, "Your comment has been updated successfully.")
            return redirect("poll_detail", pk=comment.poll.id)
        else:
            messages.error(request, "Comment content cannot be empty.")

    return render(request, "comments/edit_comment.html", {"comment": comment})

@login_required
def delete_comment(request, comment_id):
    """Delete an existing comment."""
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure only the author can delete the comment
    if comment.author != request.user:
        return HttpResponseForbidden("You do not have permission to delete this comment.")

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Your comment has been deleted successfully.")
        log_activity(request.user, "Deleted a comment")
        return redirect("poll_detail", pk=comment.poll.id)

    return render(request, "comments/delete_comment.html", {"comment": comment})