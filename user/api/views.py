from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .serializers import ProfileSerializer, NotificationSerializer
from contest.models import Tag
from photo.api.serializers import PhotoSerializer
from photo.models import Photo
from user.models import Profile, Notification


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


class NotificationsAPIView(APIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        get_already_ones = self.request.GET.get('already_seen')
        queryset = [query for query in user.notification_set.all() if not query.read]
        if get_already_ones == 'true':
            queryset = self.queryset

        paginator = LimitOffsetPagination()
        queryset = paginator.paginate_queryset(queryset, self.request)

        return queryset

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        msg = request.data['msg']
        user = get_object_or_404(User, id=request.data['user'])
        Notification.objects.create(msg=msg, user=user)
        return Response({'success': 'successfully created a new notification.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
def read_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    if notification.user != request.user:
        return Response({'error': 'Notification doesnt belong you.'}, status=status.HTTP_403_FORBIDDEN)

    notification.read = True
    notification.save()
    return Response({'success': 'successfully read the object.'}, status=status.HTTP_200_OK)










