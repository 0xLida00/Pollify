from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models
from PIL import Image

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        default='profile_pics/default.jpg',  # Correct default path
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize profile picture if it exists and is accessible
        if self.profile_picture and default_storage.exists(self.profile_picture.name):
            try:
                img = Image.open(self.profile_picture.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_picture.path)
            except Exception as e:
                print(f"Error processing profile picture: {e}")


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"