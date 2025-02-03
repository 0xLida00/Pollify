from django.db.models.signals import post_save
from django.dispatch import receiver
from comments.models import Comment
from polls.models import Poll
from .models import Notification
from users.models import Follow

@receiver(post_save, sender=Poll)
def notify_new_poll(sender, instance, created, **kwargs):
    if created:
        # Notify followers of the poll author
        followers = Follow.objects.filter(followed=instance.author)
        for follower in followers:
            Notification.objects.create(
                recipient=follower.follower,
                actor=instance.author,
                verb="created a new poll",
                target_poll=instance
            )

@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, created, **kwargs):
    if created:
        # Notify poll author when someone comments on their poll
        Notification.objects.create(
            recipient=instance.poll.author,
            actor=instance.author,
            verb="commented on your poll",
            target_poll=instance.poll
        )
        
        # Notify users who follow the poll author
        followers = Follow.objects.filter(followed=instance.poll.author)
        for follower in followers:
            if follower.follower != instance.poll.author:
                Notification.objects.create(
                    recipient=follower.follower,
                    actor=instance.author,
                    verb="commented on a poll by someone you follow",
                    target_poll=instance.poll
                )