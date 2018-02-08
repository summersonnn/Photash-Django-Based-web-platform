from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view

from contest.models import Contest, Contender
from .serializers import ContestSerializer
from photo.models import Photo

from random import randint

from django.shortcuts import get_object_or_404

class ContestListAPIView(ListAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.GET.get('q'):
            query = self.request.get('q')
            queryset = self.queryset.filter(contest_name__icontains = query)

        else:
            queryset = super(ContestListAPIView, self).get_queryset()

        return queryset


class ContestDetailAPIView(RetrieveAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(ContestDetailAPIView, self).get_context_data(*args, **kwargs)
        photos = Photo.objects.filter(contest=self.get_object())
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

        if self.request.user.is_authenticated:
            context['vote_count'], context['vote_avg'], context['vote_stddev'] \
                = self.request.user.get_vote_count_avg_stddev_for_contest(contest)
            try:  # if there is not any Contender object, get() will raise an exception
                contender = Contender.objects.get(user=self.request.user, contest=self.get_object())
                # context['contender'] = contender
                context['num_of_uploaded_photos'] = contender.get_number_of_photos_uploaded()
                # context['is_uploaded'] = 1  # True
            except Contender.DoesNotExist:
                context['num_of_uploaded_photos'] = 0
                # context['is_uploaded'] = 0  # False


