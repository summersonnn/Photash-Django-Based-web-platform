from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import PhotoSerializer
from rest_framework.response import Response
from photo.models import Photo
from contest.models import Contest

class PhotoListAPIView(ListAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    paginate_by = 4

    def get_queryset(self):
        slug=self.kwargs["contest"]
        print("abs:", slug)

        contest = Contest.objects.get(slug=slug)
        queryset = self.queryset.filter(contest=contest)

        user_voted = [user_rating.rating.content_object for user_rating in self.request.user.userrating_set.all() if user_rating.rating.content_object.contest == contest]
        print("voted:", user_voted)
        Queryset = []

        for query in queryset:
            if query not in user_voted:
                Queryset.append(query)


        return Queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




