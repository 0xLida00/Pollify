from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from polls.models import Poll, Vote
from comments.models import Comment

class FrontendTests(TestCase):
    def setUp(self):
        # Setup test users, polls, and comments
        self.client = Client()
        self.author = User.objects.create_user(username='pollauthor', password='password')
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create sample polls
        self.poll1 = Poll.objects.create(author=self.author, question='Sample Poll 1', category='Technology')
        self.poll2 = Poll.objects.create(author=self.author, question='Sample Poll 2', category='Sports')

        # Add votes to polls to simulate trending
        Vote.objects.create(poll=self.poll1, choice=self.poll1.choices.create(choice_text="Yes"), voter=self.user)
        Vote.objects.create(poll=self.poll1, choice=self.poll1.choices.create(choice_text="No"), voter=self.author)

        # Create comments
        self.comment1 = Comment.objects.create(poll=self.poll1, author=self.user, content="This is a comment on Poll 1.")
        self.comment2 = Comment.objects.create(poll=self.poll2, author=self.user, content="Another comment on Poll 2.")

    def test_home_view_status_code(self):
        """Test that the home view returns a 200 status code."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_trending_polls_display(self):
        """Test that trending polls are displayed correctly on the home page."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Sample Poll 1")
        self.assertContains(response, "2 Votes")

    def test_recent_polls_display(self):
        """Test that recent polls are displayed correctly."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Sample Poll 2")
        self.assertContains(response, "Sample Poll 1")

    def test_recent_comments_display(self):
        """Test that recent comments are displayed correctly."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, "This is a comment on Poll 1.")
        self.assertContains(response, "Another comment on Poll 2.")

    def test_empty_trending_polls(self):
        """Test that a message is displayed when there are no trending polls."""
        Poll.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertContains(response, "No trending polls at the moment.")

    def test_empty_recent_polls(self):
        """Test that a message is displayed when there are no recent polls."""
        Poll.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertContains(response, "No polls available yet.")

    def test_empty_recent_comments(self):
        """Test that a message is displayed when there are no recent comments."""
        Comment.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertContains(response, "No comments yet. Join the conversation!")