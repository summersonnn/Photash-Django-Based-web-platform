from rest_framework import serializers
from photo.models import Photo
from contest.api.serializers import ContestSerializer

class PhotoSerializer(serializers.ModelSerializer):
    contest = ContestSerializer()
    class Meta:
        model  = Photo
        fields = ('__all__')