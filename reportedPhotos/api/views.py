from django.http import Http404
from django.shortcuts import get_object_or_404
from photo.api.serializers import PhotoSerializer
from photo.models import Photo
from reportedPhotos.models import ReportedPhotos
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from .serializers import ReportedPhotosSerializer
from reportedPhotos.models import ReportedPhotos

class ReportPhotoAPIView(APIView):
    serializer_class = ReportedPhotosSerializer
    queryset = Photo.objects.all()
    http_method_names = [u'get', ]
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, id, format=None):
        try:
            photo = Photo.objects.get(id=id) # check if photo exists
            try:
                report = ReportedPhotos.objects.get(photo=photo)
                if report in request.user.profile.reported_photos.all():
                    return Response({'error': 'You have already reported this photo.'}, status=HTTP_403_FORBIDDEN)
            except ReportedPhotos.DoesNotExist:
                report = ReportedPhotos(photo=photo)

            report.howmany_reports += 1
            report.save()

            if not request.user.profile.reported_photos:
                request.user.profile.reported_photos.add(ReportedPhotos.objects.get_or_create(photoid=0))

            request.user.profile.reported_photos.add(report)

        except Exception as error:
            return Response({'error': str(error)}, status=HTTP_403_FORBIDDEN)

        return Response({'success': 'Success!'})


















