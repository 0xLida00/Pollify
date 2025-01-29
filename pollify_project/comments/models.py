from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    poll = models.ForeignKey("polls.Poll", on_delete=models.CASCADE, related_name="comments")  # ✅ Correct reference
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(User, through="CommentVote", related_name="comment_votes")

    def __str__(self):
        return f"{self.author.username} - {self.poll.question}"

class CommentVote(models.Model):
    """Tracks user votes on comments."""
    VOTE_CHOICES = (("upvote", "Upvote"), ("downvote", "Downvote"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("user", "comment")  # Ensure one vote per user per comment