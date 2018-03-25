from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Photo
from contest.models import Contest, Contender
from django.contrib.auth.models import User
from django.contrib import messages


def photo_detail(request, id):
    return render(request, "photo/detail.html", context={})


def photo_delete(request, id):
    return HttpResponseRedirect('api/photo/{}/delete'.format(id))
