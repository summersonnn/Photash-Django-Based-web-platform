from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from star_ratings.models import *
# from photo.models import *
from django.db.models import Sum
from math import sqrt
from django.db.models import Max
# from photo.models import *


# Create your models here.
class Contest(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Contest id')
    contest_name = models.CharField(max_length=50, unique=True, blank=False, verbose_name='Contest Name')
    contest_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name='photo? video?')
    start_date = models.DateTimeField(blank=False, verbose_name='Start Date')
    end_date = models.DateTimeField(blank=False, verbose_name='End Date')
    tag = models.CharField(max_length=30, blank=False, verbose_name='Contest Tag')
    min_must_votes = models.IntegerField(blank=False, default=10, verbose_name='Minimum number of votes a contender must provide')              #Yani o contest içinde en az bu sayı defa oy vermeli. Vermezse kendi gönderdiği fotoğraf geçerli olmayacak.
    min_avg = models.FloatField(blank=False, default=4.00, verbose_name='Min average of given points a contender must provide')       #Yani o contest içinde verdiği oyların ortalaması en az bu kadar olmalı. Bu sayede herkese 1 vermesini önlüyoruz.
    min_stddev = models.FloatField(blank=False, default=2.00, verbose_name='User should not vote with repeated scores')
    max_photos_per_Reguser = models.IntegerField(blank=False, default=5, verbose_name='Max photos per free user')
    max_photos_per_Preuser = models.IntegerField(blank=False, default=20, verbose_name='Max photos per Premium user')
    prize_distributions = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.contest_name)

    def get_absolute_url(self):
        return reverse('contest:detail', kwargs={'slug': self.slug})


class Contender(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Username", related_name="contender")
    contest = models.ForeignKey('Contest', verbose_name='Contest id', on_delete=models.CASCADE, related_name="contenders")
    final_ranking = models.IntegerField(blank=False, default=1, verbose_name='Final ranking')
    prize_earned = models.TextField(blank=True)
    achievement_earned = models.TextField(blank=True)

    class Meta:
            unique_together = (("user", "contest"),)

    def __str__(self):
        return self.user.username

    def get_number_of_photos_uploaded(self):
        Photo = apps.get_model('photo.Photo')
        return Photo.objects.filter(ownername=self.user, contest=self.contest).count()

    @staticmethod
    def get_stddev(data, vote_count, vote_average):  # POSTGRESQL'e geçtikten sonra django stddev api'ını kullaibiliriz
        if vote_count < 2:
            return 0

        return sqrt(sum((x.score - vote_average) ** 2 for x in data) / (vote_count-1))

    def get_vote_count_avg_stddev(self):
        votes = self.user.votes.filter(rating__photos__contest=self.contest)
        vote_count = votes.count()

        if vote_count == 0:
            return 0, 0.0, 0.0

        vote_sum = votes.aggregate(Sum('score'))['score__sum']
        vote_average = float(vote_sum) / vote_count

        return votes.count(), vote_average, Contender.get_stddev(votes, vote_count, vote_average)

    def check_conditions_for_rankings(self):
        vote_count, vote_average, vote_stddev = self.get_vote_count_avg_stddev()

        # criterias
        count_criteria = True
        avg_criteria = True
        stddev_criteria = True

        output_string = ""

        # count_criteria
        if vote_count < self.contest.min_must_votes:
            count_criteria = False
            output_string += "count_criteria\n"

        # avg_criteria
        if vote_average < self.contest.min_avg:
            avg_criteria = False
            output_string += "avg_criteria\n"

        # stddev_criteria
        if vote_stddev < self.contest.min_stddev:
            stddev_criteria = False
            output_string += "stddev_criteria\n"

        if count_criteria and avg_criteria and stddev_criteria:
            return True
        else:
            print(self.user.username, "did not satisfy the following condition(s)")
            print(output_string)
            return False




