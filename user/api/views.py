from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from .serializers import ProfileSerializer, UserSerializer
from photo.api.serializers import PhotoSerializer
from photo.models import Photo
from user.models import Profile

class ProfileDetailAPIView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(object)
        data = serializer.data
        photos = [Photo.objects.get(id=photo.id) for photo in object.photos_will_be_shown.all()]
        if photos:
            print(photos)
            data['photos_will_be_shown'] = PhotoSerializer(photos, many=True).data

        return Response(data, status=HTTP_200_OK)


