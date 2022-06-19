from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# When a user is create it will automatically create a profile

@receiver(post_save, sender=User) # When a user is saved then send this signal will be received by this receiver which is create_profile function
def create_profile(sender, instance, created, **kwargs):
	if created: # If the user is created
		Profile.objects.create(user=instance) # Then create a profile with instance of the newly created user

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()
	