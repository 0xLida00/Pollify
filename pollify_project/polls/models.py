from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse


class Poll(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="polls")
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    category = models.CharField(
        max_length=50,
        choices=[
            ("Technology", "Technology"),
            ("Sports", "Sports"),
            ("Entertainment", "Entertainment"),
            ("Science", "Science"),
            ("Health", "Health"),
            ("Education", "Education"),
            ("Business", "Business"),
            ("Politics", "Politics"),
            ("Environment", "Environment"),
            ("Travel", "Travel"),
            ("Food", "Food"),
            ("Fashion", "Fashion"),
            ("Art", "Art"),
            ("History", "History"),
            ("Culture", "Culture"),
            ("Literature", "Literature"),
            ("Philosophy", "Philosophy"),
            ("Religion", "Religion"),
            ("Personal Development", "Personal Development"),
            ("Gaming", "Gaming"),
            ("Startups", "Startups"),
            ("Economics", "Economics"),
            ("Fitness", "Fitness"),
            ("Relationships", "Relationships"),
            ("Parenting", "Parenting"),
            ("DIY & Crafts", "DIY & Crafts"),
            ("Movies", "Movies"),
            ("TV Shows", "TV Shows"),
            ("Music", "Music"),
            ("Cryptocurrency", "Cryptocurrency"),
            ("AI & Machine Learning", "AI & Machine Learning"),
            ("Astronomy", "Astronomy"),
            ("Automobiles", "Automobiles"),
            ("Mental Health", "Mental Health"),
            ("Volunteerism", "Volunteerism"),
            ("Career Development", "Career Development"),
            ("Hobbies", "Hobbies"),
            ("Pets & Animals", "Pets & Animals"),
            ("Other", "Other"),
        ],
        default="Other",
    )

    def __str__(self):
        return self.question

    def has_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    def get_absolute_url(self):
        return reverse('poll_detail', kwargs={'pk': self.pk})


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)
    votes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "voter")  # Prevent double voting