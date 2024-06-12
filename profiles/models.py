from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"

    )
    image = ImageField(upload_to="profiles")
    name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, null=True)

    
    

    def __str__(self):
        return self.user.username
#Number of follower    
def follower_count(self):
        return self.followers.count()
#Number of authors user is following
def follows_count(self):
        return self.following.count()

User.add_to_class("follower_count", follower_count)
User.add_to_class("follows_count", follows_count)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Create or update a new Profile() object when a Django User is created
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
