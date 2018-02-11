from __future__ import division, unicode_literals
from decimal import Decimal
from warnings import warn
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count, Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from model_utils.models import TimeStampedModel
from . import app_settings
from django.apps import apps


def _clean_user(user):
    if not app_settings.STAR_RATINGS_ANONYMOUS:
        if not user:
            raise ValueError(_("User is mandatory. Enable 'STAR_RATINGS_ANONYMOUS' for anonymous ratings."))
        return user
    return None


class RatingManager(models.Manager):
    def for_instance(self, instance):
        if isinstance(instance, Rating):
            raise TypeError("Rating manager 'for_instance' expects model to be rated, not Rating model.")
        ct = ContentType.objects.get_for_model(instance)
        ratings, created = self.get_or_create(content_type=ct, object_id=instance.pk)
        return ratings

    def ratings_for_instance(self, instance):
        warn("RatingManager method 'ratings_for_instance' has been renamed to 'for_instance'. Please change uses of 'Rating.objects.ratings_for_instance' to 'Rating.objects.for_instance' in your code.", DeprecationWarning)
        return self.for_instance(instance)

    def rate(self, instance, score, user=None, ip=None):
        if isinstance(instance, Rating):
            raise TypeError("Rating manager 'rate' expects model to be rated, not Rating model.")
        ct = ContentType.objects.get_for_model(instance)
        user = _clean_user(user)
        existing_rating = UserRating.objects.for_instance_by_user(instance, user)

        if existing_rating:
            if not app_settings.STAR_RATINGS_RERATE:
                raise ValidationError(_('Already rated.'))
            existing_rating.score = score
            existing_rating.save()
            return existing_rating.rating
        else:
            # Oylanan fotoğrafın sahibinin profil bilgisini çekip bazı özelliklerini updateledik.
            Profile = apps.get_model('user.Profile')
            profile = Profile.objects.get(user=instance.ownername)
            total_Points = profile.voted_x_times * profile.all_time_average
            total_Points += int(score)
            profile.voted_x_times += 1
            profile.all_time_average = total_Points / profile.voted_x_times
            profile.save()

            rating, created = self.get_or_create(content_type=ct, object_id=instance.pk)
            return UserRating.objects.create(user=user, score=score, rating=rating, ip=ip).rating


@python_2_unicode_compatible
class Rating(models.Model):
    """
    Attaches Rating models and running counts to the model being rated via a generic relation.
    """
    total = models.PositiveIntegerField(default=0)
    count = models.PositiveIntegerField(default=0)
    average = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.0))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    objects = RatingManager()

    class Meta:
        unique_together = ['content_type', 'object_id']

    @property
    def percentage(self):
        return (self.average / app_settings.STAR_RATINGS_RANGE) * 100

    def to_dict(self):
        return {
            'count': self.count,
            'total': self.total,
            'average': self.average,
            'percentage': self.percentage,
        }

    def __str__(self):
        return '{}'.format(self.content_object)

    def calculate(self):
        """
        Recalculate the totals, and save.
        """
        aggregates = self.user_ratings.aggregate(total=Sum('score'), average=Avg('score'), count=Count('score'))
        self.count = aggregates.get('count') or 0
        self.total = aggregates.get('total') or 0
        self.average = aggregates.get('average') or 0.0
        self.save()


class UserRatingManager(models.Manager):
    def for_instance_by_user(self, instance, user=None):
        ct = ContentType.objects.get_for_model(instance)
        user = _clean_user(user)

        if user:
            return self.filter(rating__content_type=ct, rating__object_id=instance.pk, user=user).first()
        else:
            return None

    def has_rated(self, instance, user=None):
        if isinstance(instance, Rating):
            raise TypeError("UserRating manager 'has_rated' expects model to be rated, not UserRating model.")

        rating = self.for_instance_by_user(instance, user=user)
        return rating is not None

    def bulk_create(self, objs, batch_size=None):
        objs = super(UserRatingManager, self).bulk_create(objs, batch_size=batch_size)
        for rating in set(o.rating for o in objs):
            rating.calculate()
        return objs


@python_2_unicode_compatible
class UserRating(TimeStampedModel):
    """
    An individual rating of a user against a model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='votes')
    ip = models.GenericIPAddressField(blank=True, null=True)
    score = models.PositiveSmallIntegerField()
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='user_ratings')

    objects = UserRatingManager()

    class Meta:
        unique_together = ['user', 'rating']

    def __str__(self):
        if not app_settings.STAR_RATINGS_ANONYMOUS:
            return '{} rating {} for {}'.format(self.user, self.score, self.rating.content_object)
        return '{} rating {} for {}'.format(self.ip, self.score, self.rating.content_object)

    @property
    def percentage(self):
        return (self.score / app_settings.STAR_RATINGS_RANGE) * 100
