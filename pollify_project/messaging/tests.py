from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from messaging.models import Message

class MessagingTests(TestCase):
    def setUp(self):
        # Setup test users and client
        self.client = Client()
        self.sender = User.objects.create_user(username='sender', password='password')
        self.recipient = User.objects.create_user(username='recipient', password='password')

        # Create a test message
        self.message = Message.objects.create(
            sender=self.sender,
            subject='Test Message',
            body='This is a test message body.'
        )
        # Add recipient to the message
        self.message.recipients.add(self.recipient)

    def test_inbox_view_status_code(self):
        """Test that the inbox view returns a 200 status code for the recipient."""
        self.client.login(username='recipient', password='password')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 200)

    def test_outbox_view_status_code(self):
        """Test that the outbox view returns a 200 status code for the sender."""
        self.client.login(username='sender', password='password')
        response = self.client.get(reverse('messaging:outbox'))
        self.assertEqual(response.status_code, 200)

    def test_inbox_message_display(self):
        """Test that the inbox view displays the correct message."""
        self.client.login(username='recipient', password='password')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertContains(response, 'Test Message')

    def test_outbox_message_display(self):
        """Test that the outbox view displays the correct message."""
        self.client.login(username='sender', password='password')
        response = self.client.get(reverse('messaging:outbox'))
        self.assertContains(response, 'Test Message')

    def test_message_detail_view(self):
        """Test that the message detail view displays the correct message content."""
        self.client.login(username='sender', password='password')
        response = self.client.get(reverse('messaging:message_detail', args=[self.message.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test message body.')

    def test_read_message_view(self):
        """Test that the read message view marks a message as read."""
        self.client.login(username='recipient', password='password')
        response = self.client.get(reverse('messaging:read_message', args=[self.message.id]))
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)
        self.assertContains(response, 'This is a test message body.')

    def test_send_message(self):
        """Test that a message can be sent through the compose view."""
        self.client.login(username='sender', password='password')
        response = self.client.post(reverse('messaging:compose_message'), {
            'recipients': [self.recipient.id],  # Send the recipients as a list
            'subject': 'New Test Message',
            'body': 'This is a new message.'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to inbox after sending

        # Verify that the message was created
        new_message = Message.objects.get(subject='New Test Message')
        self.assertEqual(new_message.sender, self.sender)
        self.assertTrue(new_message.recipients.filter(id=self.recipient.id).exists())

    def test_empty_inbox(self):
        """Test that the inbox displays a message when there are no messages."""
        Message.objects.all().delete()
        self.client.login(username='recipient', password='password')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertContains(response, 'No messages in your inbox.')