from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import ProfileSerializer #, UserSerializer
from contest.models import Tag
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

        return Response(data, status=status.HTTP_200_OK)


class UpdatePreferedTags(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        try:
            old_tags = Profile.objects.get(user=self.request.user).prefered_tags
            remove = request.data['remove']
            tag_ids = request.data['ids']
            tag_objects = [get_object_or_404(Tag, id=id) for id in tag_ids]

            if not remove:
                for tag in tag_objects:
                    if tag not in old_tags.all():
                        old_tags.add(tag)

            else:
                for tag in tag_objects:
                    if tag in old_tags.all():
                        old_tags.add(tag)

            return Response({'success': 'successfuly updated users tags.'}, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({'error': error.message}, status=status.HTTP_406_NOT_ACCEPTABLE)








