from rest_framework import serializers
from user.models import Profile, Notification
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'user_permissions', ]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        exclude = ['photos_will_be_shown', 'reported_photos']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('__all__')