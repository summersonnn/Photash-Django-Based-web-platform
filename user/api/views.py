from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.status import HTTP_200_OK
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

        return Response(data, status=HTTP_200_OK)


class UpdatePreferedTags(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_tags(self, ids):
        old_tags = Profile.objects.get(user=self.request.user).prefered_tags.all()
        queryset = [get_object_or_404(Tag, id=id) for id in ids]
        removable = False

        for tag in old_tags:
            if tag not in queryset:
                removable = False
                break

        return queryset, removable

    def post(self, request, format=None):
        '''try:
            remove = request.data['remove']
            tag_ids = request.data['ids']
            tag_objects = self.get_tags(tag_ids)

            if remove:
                pass'''

        pass



