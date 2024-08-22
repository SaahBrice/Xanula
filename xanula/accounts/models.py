from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def has_active_subscription(self):
        return self.subscriptions.filter(
            is_active=True,
            end_date__gt=timezone.now()
        ).exists()



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def has_active_subscription(user):
        return user.subscriptions.filter(
            is_active=True,
            end_date__gt=timezone.now()
        ).exists()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()