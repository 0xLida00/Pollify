from django.test import TestCase
from django.contrib.auth import get_user_model
from notifications.models import Notification
from polls.models import Poll

User = get_user_model()

class NotificationTests(TestCase):
    def setUp(self):
        # Set up users and a poll for testing
        self.actor = User.objects.create_user(username='actor', password='password')
        self.recipient = User.objects.create_user(username='recipient', password='password')
        self.poll = Poll.objects.create(author=self.actor, question="Sample Poll")

    def test_notification_creation(self):
        # Create a notification with a target poll
        notification = Notification.objects.create(
            actor=self.actor,
            recipient=self.recipient,
            verb='created a poll',
            target_poll=self.poll
        )

        # Check if the notification is correctly created
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(notification.actor, self.actor)
        self.assertEqual(notification.recipient, self.recipient)
        self.assertEqual(notification.verb, 'created a poll')
        self.assertEqual(notification.target_poll, self.poll)
        self.assertFalse(notification.is_read)  # Check that the notification is unread by default

    def test_notification_without_target_poll(self):
        # Create a notification without a target poll
        notification = Notification.objects.create(
            actor=self.actor,
            recipient=self.recipient,
            verb='liked a post'
        )

        # Check if the notification is created without a target poll
        self.assertEqual(Notification.objects.count(), 1)
        self.assertIsNone(notification.target_poll)

    def test_mark_notification_as_read(self):
        # Create a notification
        notification = Notification.objects.create(
            actor=self.actor,
            recipient=self.recipient,
            verb='followed you'
        )

        # Mark the notification as read
        notification.is_read = True
        notification.save()

        # Check if the notification is marked as read
        self.assertTrue(Notification.objects.get(id=notification.id).is_read)

    def test_notification_str_representation(self):
        # Create a notification
        notification = Notification.objects.create(
            actor=self.actor,
            recipient=self.recipient,
            verb='voted on a poll',
            target_poll=self.poll
        )

        # Check the string representation of the notification
        self.assertEqual(str(notification), f"{self.actor} voted on a poll for {self.recipient}")