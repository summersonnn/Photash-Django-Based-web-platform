from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Contest, Contender
from photo.models import Photo
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib import messages
from .forms import PhotoForm


def contest_index(request):
    contest_list = Contest.objects.all()

    query = request.GET.get("q")
    if query:
        # Sadece contest_name ile kalmayıp başka fieldlar içinde arama yapmasını sağlayabiliriz.
        # Detay: https://www.youtube.com/watch?v=eyAIAZr5Q3w
        contest_list = contest_list.filter(contest_name__icontains=query)

    # Show 5 contacts per page
    paginator = Paginator(contest_list, 5)

    page = request.GET.get('page')
    try:
        contests = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contests = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contests = paginator.page(paginator.num_pages)

    context = {
        'contests': contests,
    }

    return render(request, "contest/index.html", context)


def contest_detail(request, slug):
    # request.POST.get('slug')
    contest = get_object_or_404(Contest, slug=slug)
    user = request.user

    context = {
        'contest': contest,
    }

    if user.is_authenticated:
        context['vote_count'], context['vote_avg'], context['vote_stddev'] \
            = user.get_vote_count_avg_stddev_for_contest(contest)
        try:  # if there is not any Contender object, get() will raise an exception
            contender = Contender.objects.get(user=request.user, contest=contest)
            # context['contender'] = contender
            context['num_of_uploaded_photos'] = contender.get_number_of_photos_uploaded()
            # context['is_uploaded'] = 1  # True
        except Contender.DoesNotExist:
            context['num_of_uploaded_photos'] = 0
            # context['is_uploaded'] = 0  # False

    return render(request, "contest/detail.html", context)


def photo_upload(request, slug):
    # Fotoğrafın hangi contest'in pool'una gideceği bilgisini çektik.
    # Bu bilgi contest detail'indeki Join Contest butonu ile verilmişti.
    contest_record = Contest.objects.get(slug=slug)
    if not request.user.is_authenticated:
        return Http404()  # Http404 yerine bir message ile signup sayfasına yönlendirilmeli

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():  # valid captcha
            photo = form.save(commit=False)
            photo.contest = contest_record
            photo.ownername = request.user
            photo.save()

            # User'ın o conteste yükleyeceği İlk fotoğraf ise böyle contender objesi yoktur, o objeyi oluşturalım.
            if not Contender.objects.filter(user=request.user, contest=contest_record).exists():
                contender = Contender(user=request.user, contest=contest_record)
                contender.save()

            # Mesaj ve redirection işlemleri
            messages.success(request, 'You have succesfully sent a photo to photo pool')
            return HttpResponseRedirect(contest_record.get_absolute_url())

        else:  # user entered an invalid captcha
            messages.error(request, 'Invalid input for reCaptcha. Please make sure you enter the correct letters')
            return HttpResponseRedirect(request.path_info)  # redirect to the same page

    else:  # GET
        try:  # if there is not any Contender object, get() will raise an exception
            the_contender = Contender.objects.get(user=request.user, contest=contest_record)

            if the_contender.get_number_of_photos_uploaded() < contest_record.max_photos_per_Reguser:
                form = PhotoForm()
                context = {
                    'form': form,
                }
                return render(request, 'photo/form.html', context)
            else:
                return render(request, 'contest/maxreached.html')

        except Contender.DoesNotExist:
            form = PhotoForm()
            context = {
                'form': form,
            }

            return render(request, 'photo/form.html', context)


def contest_photopool(request, slug):
    # O contest'e ait fotoğrafları contestid'sinden tanıyıp, ayrıştırıp öyle veriyoruz photo/index.html dosyasına.
    contest = Contest.objects.get(slug=slug)
    photos = Photo.objects.filter(contest=contest)
    user = request.user

    # display the photos that are not voted nor uploaded by the user
    if user.is_authenticated:  # and user.votes:
        already_voted_instances = [user_rating.rating.content_object for user_rating in user.votes.all() if user_rating.rating.content_object.contest == contest]
                                  # and not user_rating.rating.content_object.ownername == user]

        # voted_instances_ids = user.votes.

        # not_voted_nor_owned_instances = photos.exclude(ratings=user).exclude(ownername=user)

        query_set = []
        for query in photos:
            if query not in already_voted_instances and query.ownername != user:
                query_set.append(query)

        context = {
            'photos': query_set[:5],
            'contest': contest,
        }
    else:
        context = {
            'photos': photos[:5],
            'contest': contest,
        }
    return render(request, "contest/photopool.html", context)


def contest_delete(request, id):
    contest = get_object_or_404(Contest, id=id)
    contest.delete()
    return redirect("contest:index")


def contest_rankings(request, slug):
    contest = get_object_or_404(Contest, slug=slug)

    if timezone.now() < contest.end_date:  # if contest is still in progress
        context = {
            'thecontest': contest
        }
        return render(request, "contest/contest_still_in_progress.html", context)

    contenders = Contender.objects.filter(contest=contest)
    excluded_contender_ids = []

    for contender in contenders:
        if not contender.check_conditions_for_rankings():
            excluded_contender_ids.append(contender.id)
            # print("excluded", contender.user.username)

    photos = Photo.objects\
        .filter(contest=contest)\
        .filter(ratings__isnull=False)\
        .exclude(ownername__contender__id__in=excluded_contender_ids)\
        .order_by('-ratings__average')

    # Show 20 photos per page
    paginator = Paginator(photos, 5)

    page = request.GET.get('page')
    try:
        paginated_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_photos = paginator.page(paginator.num_pages)

    context = {
        'photos': paginated_photos,
    }

    return render(request, "contest/rankings.html", context)

