from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Contest(models.Model):
    id = models.IntegerField(primary_key = True, verbose_name = 'Contest id')
    contest_name = models.CharField(max_length = 50, unique = True, blank = False, verbose_name = 'Contest Name')
    start_date = models.DateTimeField(blank = False, verbose_name = 'Start Date')
    end_date = models.DateTimeField(blank = False, verbose_name = 'End Date')
    tag = models.CharField(max_length = 30, blank = False, verbose_name = 'Contest Tag')
    min_must_votes = models.IntegerField(blank = False, default = 10, verbose_name = 'Minimum number of votes a contender must provide')              #Yani o contest içinde en az bu sayı defa oy vermeli. Vermezse kendi gönderdiği fotoğraf geçerli olmayacak.
    min_total_points_given = models.FloatField(blank = False, default = 4.00, verbose_name = 'Min average of given points a contender must provide')       #Yani o contest içinde verdiği oyların ortalaması en az bu kadar olmalı. Bu sayede herkese 1 vermesini önlüyoruz.
    max_photos_per_Reguser = models.IntegerField(blank = False, default = 5, verbose_name = 'Max photos per free user')
    max_photos_per_Preuser = models.IntegerField(blank=False, default=20, verbose_name = 'Max photos per Premium user')
    prize_distributions = models.TextField(blank = True)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return str(self.contest_name)

    def get_absolute_url(self):
        return reverse('contest:detail', kwargs={'slug': self.slug})

class Contender(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Username")
    contest = models.ForeignKey('Contest', verbose_name = 'Contest id', on_delete = models.CASCADE)
    howmany_voted = models.IntegerField(blank = False, default = 0, verbose_name = 'Number of photos that is voted by the contender')
    total_points_given = models.IntegerField(blank = False, default = 0, verbose_name = 'Number of points that is distributed by the contender')
    howmany_photos_owned = models.IntegerField(blank = False, default = 0, verbose_name = 'Photos that is sent to pool by the contender')
    final_ranking = models.IntegerField(blank = False, default = 1, verbose_name = 'Final ranking')
    prize_earned = models.TextField(blank = True)
    achievement_earned = models.TextField(blank = True)

    class Meta:
            unique_together = (("user","contest"),)

    def __str__(self):
        return self.user.username







