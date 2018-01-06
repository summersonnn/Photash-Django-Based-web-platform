from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username")
    location = models.CharField(max_length=30, blank=True, verbose_name="Location")
    email_verified = models.BooleanField(blank = False, default = False, verbose_name = 'E-mail verification')
    achievements = models.TextField(blank = True)
    aboutme = models.TextField(blank = True)
    is_premium = models.BooleanField(blank = False, default = False, verbose_name = 'Premium status')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()