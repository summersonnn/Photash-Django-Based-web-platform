from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from contest.models import Contest, Contender, Tag
from .serializers import ContestSerializer, TagSerializer
from photo.api.serializers import PhotoSerializer
from photo.models import Photo
from user.models import Profile

from django.utils import timezone

from django.shortcuts import get_object_or_404

from random import randint, shuffle, choice
import operator

def recommendation(queryset, user):
    user = Profile.objects.get(user=user)
    preferd_tags = user.prefered_tags.all()
    reordered_queryset = {}
    return_queryset = []

    for query in queryset:
        similarity = 0
        for query_tag in query.tag.all():
            if query_tag in preferd_tags:
                similarity += 1

        try:
            index = similarity / query.tag.all().count()
        except ZeroDivisionError:
            index = 0
        reordered_queryset[query] = index

    reordered_queryset = sorted(reordered_queryset.items(), key=operator.itemgetter(1))
    print(reordered_queryset)

    for query_with_index in reversed(reordered_queryset):
        return_queryset.append(query_with_index[0])

    return return_queryset


class ContestListAPIView(ListAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.GET.get('q') or self.request.GET.get('ongoing') or self.request.GET.get('finished') or self.request.GET.get('upcoming'):
            queryset = self.queryset.all()
            if self.request.GET.get('q'):
                query = self.request.GET['q']
                queryset = queryset.filter(contest_name__icontains=query)

            if self.request.GET.get('ongoing') and not self.request.GET.get('finished') and not self.request.GET.get('upcoming'):
                copy_queryset = queryset
                queryset = []
                for query in copy_queryset:
                    if not query.is_finished() == True and not query.is_finished() == None:
                        queryset.append(query)

            elif self.request.GET.get('finished') and not self.request.GET.get('ongoing') and not self.request.GET.get('upcoming'):
                copy_queryset = queryset
                queryset = []
                for query in copy_queryset:
                    if query.is_finished() == True:
                        queryset.append(query)

            elif self.request.GET.get('upcoming') and not self.request.GET.get('ongoing') and not self.request.GET.get('finished'):
                copy_queryset = queryset
                queryset = []
                for query in copy_queryset:
                    if query.is_finished() == None:
                        queryset.append(query)

        else:
            queryset = super(ContestListAPIView, self).get_queryset()

        if self.request.user.is_authenticated:
            queryset = recommendation(queryset, self.request.user)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            for x in data:
                x['photo_count'] = Photo.objects.filter(contest=Contest.objects.get(id=int(x['id']))).count()

            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for x in data:
            x['photo_count'] = Photo.objects.filter(contest=Contest.objects.get(id=int(x['id']))).count()

        return Response(data)


class ContestDetailAPIView(RetrieveAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def get_context_data(self, *args, **kwargs):
        contest = self.get_object()
        context = super(ContestDetailAPIView, self).get_context_data(*args, **kwargs)
        photos = Photo.objects.filter(contest=contest)
        count_photos = photos.count()
        if count_photos > 2:
            context['examples'] = []
            random_index = randint(0, count_photos-1)
            while True:
                random_index2 = randint(0, count_photos - 1)
                random_index3 = randint(0, count_photos - 1)
                if (random_index2 != random_index and random_index3!= random_index and random_index2 != random_index3):
                    break


            context['examples'].append(photos[random_index])
            context['examples'].append(photos[random_index2])
            context['examples'].append(photos[random_index3])


            context['photo_count'] = Photo.objects.filter(contest=contest.id).count()

        if self.request.user.is_authenticated:
            context['vote_count'], context['vote_avg'], context['vote_stddev'] = self.request.user.get_vote_count_avg_stddev_for_contest(contest)
            try:  # if there is not any Contender object, get() will raise an exception
                contender = Contender.objects.get(user=self.request.user, contest=self.get_object())
                # context['contender'] = contender
                context['num_of_uploaded_photos'] = contender.get_number_of_photos_uploaded()
                # context['is_uploaded'] = 1  # True
            except Contender.DoesNotExist:
                context['num_of_uploaded_photos'] = 0
                # context['is_uploaded'] = 0  # False
        return context


class VotersListAPIView(RetrieveAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_class = IsAuthenticated
    authentication_class = SessionAuthentication
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    '''def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if timezone.now() > instance.end_date:
            return Response({'error': 'This contest has not come to an end yet! End date is {}'.format(instance.end_date)})
        try:
            _ = Contender.objects.get(contest=instance, user=request.user)
        except Contender.DoesNotExist:
            return Response({'error': 'You are not a contender for this contest!'}, status=status.HTTP_403_FORBIDDEN)

        data = self.get_serializer(instance).data
        data['photos'] = []

        photos = Photo.objects.filter(contest=instance, ownername=request.user)

        for photo in photos:
            for rating_info in Rating.objects.filter(object_id=photo.id):
                if rating_info.content_object == photo:
                    rating = rating_info
                    break
            photo_data = PhotoSerializer(photo).data
            photo_data['rating'] = RatingSerializer(rating).data
            photo_data['voters'] = UserRatingSerializer(UserRating.objects.filter(rating=rating), many=True).data
            photo_data.pop('contest', None)
            photo_data.pop('ownername', None)
            data['photos'].append(photo_data)

        return Response(data, status=status.HTTP_200_OK)'''


class FeedAPIView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )
    http_method_names = [u'get', ]
    queryset = Contest.objects.all()
    paginate_by = 10

    def get_queryset(self):
        if self.queryset.count() < 3:
            limit = self.queryset.count()
        else:
            limit = 3

        integers = list(range(limit))
        queryset = []
        while len(integers) > 0:
            random_integer = choice(integers)
            query = self.queryset[random_integer]
            if Photo.objects.filter(contest=query).count() > 0:
                queryset.append(query)
            integers.remove(random_integer)

        return queryset

    def get(self, request, format=None):
        data = ContestSerializer(self.get_queryset(), many=True).data 

        for contest_data in data:
            contest = Contest.objects.get(id=contest_data['id'])
            photos = Photo.objects.filter(contest=contest)
            if photos.count() > 3:
                random_integer = randint(0, photos.count() - 4)
                add = 3
            else:
                random_integer = 0
                add = photos.count()

            start_index = random_integer
            finish_index = random_integer + add
            photo_data = PhotoSerializer(photos[start_index:finish_index], many=True).data

        return Response(photo_data, status=status.HTTP_200_OK)


class AskForTags(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(AskForTags, self).get_queryset()
        return queryset[:15]


class ContestRankingAPIView(ListAPIView):

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = (SessionAuthentication, )

    def get_queryset(self):
        sorted_queryset = {}

        queryset = super(ContestRankingAPIView, self).get_queryset()
        contest = get_object_or_404(Contest, slug=self.kwargs['slug'])

        contenders = Contender.objects.filter(contest=contest)
        excluded_contender_ids = []

        for contender in contenders:
            if not contender.check_conditions_for_rankings():
                excluded_contender_ids.append(contender.id)

        photos = queryset\
            .filter(contest=contest)\
            .exclude(ownername__contender__id__in=excluded_contender_ids)

        for photo in photos:
            try:
                sorted_queryset[photo] = photo.likes.all().count() / photo.seenby.all().count()
            except ZeroDivisionError:
                sorted_queryset[photo] = 0

        sorted_queryset = dict(sorted(sorted_queryset.items(), key=operator.itemgetter(1), reverse=True))

        return list(sorted_queryset.keys())

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for data in serializer.data:
                photo = Photo.objects.get(id=int(data['id']))
                percentage = photo.like_percentage
                data['like_percentage'] = percentage

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            photo = Photo.objects.get(id=int(data['id']))
            percentage = photo.like_percentage
            data['like_percentage'] = percentage

        return Response(serializer.data)


class TagDetailAPIView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        contests = [contest for contest in Contest.objects.all() if instance in contest.tag.all()]
        data['contests'] = ContestSerializer(contests, many=True).data

        return Response(data, status=status.HTTP_200_OK)




        
        

