from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.db.models import Sum

from reportedPhotos.models import ReportedPhotos
from photo.models import Photo
from contest.models import Tag


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username")
    location = models.CharField(max_length=30, blank=True, verbose_name="Location")
    email_verified = models.BooleanField(blank=False, default=False, verbose_name='E-mail verification')
    achievements = models.TextField(blank=True)
    aboutme = models.TextField(blank=True)
    is_premium = models.BooleanField(blank=False, default=False, verbose_name='Premium status')
    reported_photos = models.ManyToManyField(ReportedPhotos)
    photos_will_be_shown = models.ManyToManyField(Photo, related_name='photos_will_be_shown')
    all_time_average = models.FloatField(blank=False, default=0.00, verbose_name='All Time Average')
    voted_x_times = models.IntegerField(blank=False, default=0, verbose_name='X kere oylandı (bütün fotoğrafları)')
    prefered_tags = models.ManyToManyField(Tag)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def get_vote_count_avg_stddev_for_contest(self, contest):
    Contender = apps.get_model('contest.Contender')
    votes = self.votes.filter(rating__photos__contest=contest)
    vote_count = votes.count()

    if vote_count == 0:
        return 0, 0.0, 0.0

    vote_sum = votes.aggregate(Sum('score'))['score__sum']
    vote_average = float(vote_sum) / vote_count

    return votes.count(), vote_average, Contender.get_stddev(votes, vote_count, vote_average)


User.add_to_class('get_vote_count_avg_stddev_for_contest', get_vote_count_avg_stddev_for_contest)


def get_name_or_username(self):
    if not self.first_name:
        return self.username
    elif not self.last_name:
        return self.first_name
    else:
        return self.first_name + ' ' + self.last_name


User.add_to_class('get_name_or_username', get_name_or_username)
