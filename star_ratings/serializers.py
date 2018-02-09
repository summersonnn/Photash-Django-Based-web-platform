from rest_framework import serializers
from .models import Rating, UserRating
from user.api.serializers import UserSerializer

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        #exclude = ('object_id', 'content_type')
        fields = ('__all__')


class UserRatingSerializer(serializers.ModelSerializer):
    rating = RatingSerializer()
    user = UserSerializer()
    class Meta:
        model = UserRating
        exclude = ('ip', 'id')