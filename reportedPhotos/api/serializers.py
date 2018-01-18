from reportedPhotos.models import ReportedPhotos
from rest_framework import serializers

class ReportedPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedPhotos
        fields = ('__all__')

