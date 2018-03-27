from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import PhotoSerializer
from rest_framework.response import Response
from photo.models import Photo
from contest.models import Contest
from django.shortcuts import get_object_or_404
from user.models import Profile

class PhotoListAPIView(ListAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    authentication_classes = (SessionAuthentication, )
    paginate_by = 4

    def get_queryset(self):
        slug = self.kwargs["slug"]

        contest = Contest.objects.get(slug=slug)
        queryset = self.queryset.filter(contest=contest)

        Queryset = []

        if self.request.user.is_authenticated:
            for query in queryset:
                if self.request.user not in query.likes.all() and query.ownername != self.request.user and self.request.user.is_authenticated:
                    Queryset.append(query)

        #Shuffling the photos so that every user will see the pool in different order
        #shuffle(Queryset)

        if self.request.GET.get('p'):
            query = self.request.GET['p']
            query = Photo.objects.get(id=query)

            if query in Queryset:
                print('Query in queryset')
            else:
                print('Query is not in queryset')
        else:
            print('There is no photo query for first pick')

        print(Queryset)

        if self.request.user.is_authenticated:
            return Queryset
        else:
            return queryset

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


#For a possible future mobile app, it is now useless.
class PhotoDetailAPIView(RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        content_type = ContentType.objects.get_for_model(Photo)
        object_id = instance.id
        rating = Rating.objects.get(content_type=content_type, object_id=object_id)
        data['rating'] = RatingSerializer(rating).data

        return Response(data, status=status.HTTP_200_OK)

'''class PhotoLikeAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        id = int(request.data['id'])
        print("xxxxx")
        print(id)
        obj = get_object_or_404(Photo, id=id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False

        if user.is_authenticated:
            if user not in obj.likes.all():
                obj.likes.add(user)
                liked = True
                updated=True
        data = {
            "updated": updated
        }
        return Response(data)'''


#For a possible future mobile app, it is now useless.
@api_view(['POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated, ))
def api_photo_delete(request, id):
    photo = get_object_or_404(Photo, id=id)
    if request.user == photo.ownername:
        photo.delete()
        return Response({'success': '{} is deleted'.format(id)}, status=status.HTTP_200_OK)

    return Response({'error': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes((SessionAuthentication,  ))
#@permission_classes((IsAuthenticated, ))
def api_increase_seen_by_one(request):
    id = int(request.data['id'])
    photo = get_object_or_404(Photo, id=id)
    if request.user not in photo.seenby.all():
        photo.seenby.add(request.user)
        photo.save()
        return Response({'success': 'Photo is seen by another person.'}, status=status.HTTP_200_OK)

    return Response({'error': 'You have already seen this photo'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@authentication_classes((SessionAuthentication,  ))
#@permission_classes((IsAuthenticated, ))
def api_increase_like_by_one(request):
    id = int(request.data['id'])
    photo = get_object_or_404(Photo, id=id)
    if request.user.is_authenticated and request.user not in photo.likes.all():
        photo.likes.add(request.user)
        photo.save()
        return Response({'success': 'Photo is liked by another person.'}, status=status.HTTP_200_OK)

    return Response({'error': 'You have already liked this photo'}, status=status.HTTP_403_FORBIDDEN)






