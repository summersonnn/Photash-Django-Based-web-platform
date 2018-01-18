from django.http import Http404
from photo.api.serializers import PhotoSerializer
from photo.models import Photo
from reportedPhotos.models import ReportedPhotos
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from .serializers import ReportedPhotosSerializer

class ReportPhotoAPIView(APIView):
    serializer_class = ReportedPhotosSerializer
    queryset = Photo.objects.all()
    http_method_names = [u'get', ]
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, id, format=None):
        try:
            if ReportedPhotos.objects.filter(photoid=id).count() != 0:
                report = ReportedPhotos.objects.get(photoid=id)
            else:
                report = ReportedPhotos(photoid=id)



            report.howmany_reports += 1
            report.save()

        except Exception as error:
            return Response({'error': error})

        return Response({'success': 'success'})










