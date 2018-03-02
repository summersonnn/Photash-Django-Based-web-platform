from rest_framework import serializers
from contest.models import Contest, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class ContestSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    class Meta:
        model = Contest
        fields = ('__all__')

