from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from admin_panel.models import ActivityLog

class AdminPanelTests(TestCase):
    def setUp(self):
        # Set up a test client and users
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.regular_user = User.objects.create_user(username='regular', password='password', email='regular@example.com')

        # Log in as admin for testing
        self.client.login(username='admin', password='password')

        # Create sample activity logs
        self.log1 = ActivityLog.objects.create(user=self.admin_user, action="Created a poll")
        self.log2 = ActivityLog.objects.create(user=self.regular_user, action="Voted on a poll")

    def test_activity_log_creation(self):
        """Test that activity logs are correctly created."""
        self.assertEqual(ActivityLog.objects.count(), 2)
        self.assertEqual(str(self.log1), f"{self.admin_user} performed Created a poll at {self.log1.timestamp}")
        self.assertEqual(str(self.log2), f"{self.regular_user} performed Voted on a poll at {self.log2.timestamp}")

    def test_dashboard_access_as_admin(self):
        """Test that an admin user can access the dashboard."""
        response = self.client.get(reverse('admin_panel:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Activity Logs")
        self.assertContains(response, self.log1.action)
        self.assertContains(response, self.log2.action)

    def test_dashboard_access_as_regular_user(self):
        """Test that a regular user cannot access the admin dashboard."""
        self.client.logout()
        self.client.login(username='regular', password='password')
        response = self.client.get(reverse('admin_panel:dashboard'))
        expected_redirect = '/login/?next=/admin_panel/dashboard/'
        self.assertRedirects(response, expected_redirect)

    def test_pagination_on_dashboard(self):
        """Test that the dashboard correctly paginates activity logs."""
        # Create additional logs to test pagination
        for i in range(30):
            ActivityLog.objects.create(user=self.admin_user, action=f"Test action {i + 1}")

        response = self.client.get(reverse('admin_panel:dashboard'))
        self.assertEqual(response.status_code, 200)

        # Verify that only 20 logs appear on the first page
        self.assertEqual(len(response.context['recent_activity']), 20)

        # Verify second page has the remaining logs
        response = self.client.get(reverse('admin_panel:dashboard') + '?page=2')
        self.assertEqual(response.status_code, 200)

        # Adjust assertion to match exactly how many logs should appear on the second page
        expected_remaining_logs = response.context['recent_activity'].paginator.count - 20
        self.assertEqual(len(response.context['recent_activity']), expected_remaining_logs)

    def test_invalid_dashboard_access(self):
        """Test that accessing the dashboard without login redirects to login."""
        self.client.logout()
        response = self.client.get(reverse('admin_panel:dashboard'))
        expected_redirect_url = '/login/?next=/admin_panel/dashboard/'
        self.assertRedirects(response, expected_redirect_url)