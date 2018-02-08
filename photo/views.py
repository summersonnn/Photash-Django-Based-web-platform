from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Photo
from contest.models import Contest, Contender
from django.contrib.auth.models import User
from star_ratings.models import *
from django.contrib import messages


def get_photo_rating(request, id):
    object = Photo.objects.get(id=id)
    return render(request, 'photo/ratings.html', context={"photo": object})


def photo_detail(request, id):
    return render(request, "photo/detail.html", context={})


def photo_delete(request, id):
    return HttpResponseRedirect('api/photo/{}/delete'.format(id))

def star_ratings(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'photo/star_ratings.html', context={'photo': photo})