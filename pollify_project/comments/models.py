from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    poll = models.ForeignKey(
        "polls.Poll",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The poll this comment belongs to."
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who created the comment.")
    content = models.TextField(help_text="Content of the comment.")
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0, help_text="Number of upvotes.")
    downvotes = models.PositiveIntegerField(default=0, help_text="Number of downvotes.")
    voters = models.ManyToManyField(User, through="CommentVote", related_name="comment_votes")

    def __str__(self):
        return f"{self.author.username} - {self.poll.question}"

    class Meta:
        ordering = ['-created_at']  # Show newest comments first


class CommentVote(models.Model):
    """Tracks user votes on comments."""
    VOTE_CHOICES = (("upvote", "Upvote"), ("downvote", "Downvote"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who voted.")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, help_text="Comment being voted on.")
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES, help_text="Type of vote.")

    class Meta:
        unique_together = ("user", "comment")
        verbose_name = "Comment Vote"
        verbose_name_plural = "Comment Votes"
        indexes = [
            models.Index(fields=['user', 'comment']),
        ]

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on comment {self.comment.id}"