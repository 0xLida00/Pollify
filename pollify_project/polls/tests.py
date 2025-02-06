from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.models import Poll, Choice, Vote
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class PollTests(TestCase):
    def setUp(self):
        # Create a user and a poll
        self.user = User.objects.create_user(username='testuser', password='password')
        self.poll = Poll.objects.create(
            author=self.user,
            question="What is your favorite programming language?",
            category="Technology"
        )
        self.choice1 = Choice.objects.create(poll=self.poll, choice_text="Python")
        self.choice2 = Choice.objects.create(poll=self.poll, choice_text="JavaScript")

    def test_poll_creation(self):
        # Test that the poll was created successfully
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(self.poll.author, self.user)
        self.assertEqual(self.poll.question, "What is your favorite programming language?")
        self.assertFalse(self.poll.has_expired())

    def test_poll_expiration(self):
        # Test poll expiration logic
        self.poll.expires_at = timezone.now() - timedelta(days=1)  # Set expiration date in the past
        self.poll.save()
        self.assertTrue(self.poll.has_expired())

    def test_choice_creation(self):
        # Test that choices are correctly created
        self.assertEqual(self.poll.choices.count(), 2)
        self.assertEqual(self.choice1.choice_text, "Python")
        self.assertEqual(self.choice2.choice_text, "JavaScript")

    def test_vote_creation(self):
        # Test voting functionality
        vote = Vote.objects.create(poll=self.poll, choice=self.choice1, voter=self.user)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(vote.poll, self.poll)
        self.assertEqual(vote.choice, self.choice1)
        self.assertEqual(vote.voter, self.user)

    def test_prevent_double_voting(self):
        # Test that a user cannot vote twice on the same poll
        Vote.objects.create(poll=self.poll, choice=self.choice1, voter=self.user)
        with self.assertRaises(Exception):  # Adjust exception based on your model's behavior
            Vote.objects.create(poll=self.poll, choice=self.choice2, voter=self.user)

    def test_poll_str_representation(self):
        # Test the string representation of a poll
        self.assertEqual(str(self.poll), "What is your favorite programming language?")

    def test_choice_str_representation(self):
        # Test the string representation of a choice
        self.assertEqual(str(self.choice1), "Python")