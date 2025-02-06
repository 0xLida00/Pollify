from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Follow
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        # Set up users for testing
        self.user1 = User.objects.create_user(username='user1', password='password1', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password2', email='user2@example.com')

    def test_user_creation(self):
        # Test that users are created successfully
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.email, 'user1@example.com')

    def test_user_str_representation(self):
        # Test the string representation of a user
        self.assertEqual(str(self.user1), 'user1')

    def test_profile_update(self):
        # Test updating the user's bio
        self.user1.bio = "This is a test bio."
        self.user1.save()
        updated_user = User.objects.get(username='user1')
        self.assertEqual(updated_user.bio, "This is a test bio.")

    def test_profile_picture_upload_and_resize(self):
        # Test uploading a profile picture and resizing it
        image = Image.new('RGB', (500, 500), 'blue')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)

        self.user1.profile_picture = SimpleUploadedFile('test_image.jpg', buffer.read(), content_type='image/jpeg')
        self.user1.save()

        # Check that the profile picture is saved and resized
        self.assertTrue(self.user1.profile_picture)
        self.user1.refresh_from_db()
        img = Image.open(self.user1.profile_picture.path)
        self.assertTrue(img.height <= 300 and img.width <= 300)

    def test_following_functionality(self):
        # Test following a user
        follow = Follow.objects.create(follower=self.user1, followed=self.user2)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.followed, self.user2)

    def test_unique_follow_constraint(self):
        # Test that a user cannot follow another user more than once
        Follow.objects.create(follower=self.user1, followed=self.user2)
        with self.assertRaises(Exception):  # Adjust exception based on behavior
            Follow.objects.create(follower=self.user1, followed=self.user2)

    def test_follow_str_representation(self):
        # Test the string representation of a follow instance
        follow = Follow.objects.create(follower=self.user1, followed=self.user2)
        self.assertEqual(str(follow), "user1 follows user2")