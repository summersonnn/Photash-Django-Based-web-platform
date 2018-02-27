from rest_framework import serializers
from contest.models import Contest, Tag

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('__all__')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')