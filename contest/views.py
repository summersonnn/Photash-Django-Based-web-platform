from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Contest, Contender
from photo.models import Photo
from django.utils import timezone
from django.contrib import messages
from .forms import PhotoForm

def contest_index(request):
    context = {}
    if request.GET.get('q'):
        context['query'] = request.GET['q']
    if request.GET.get('ongoing'):
        context['ongoing'] = request.GET['ongoing']
    if request.GET.get('finished'):
        context['finished'] = request.GET['finished']
    if request.GET.get('upcoming'):
        context['upcoming'] = request.GET['upcoming']
    return render(request, "contest/index.html", context)


def contest_detail(request, slug):
    return render(request, "contest/detail.html", context={'contest': Contest.objects.get(slug=slug)})


def photo_upload(request, slug):
    # Fotoğrafın hangi contest'in pool'una gideceği bilgisini çektik.
    # Bu bilgi contest detail'indeki Join Contest butonu ile verilmişti.
    contest_record = Contest.objects.get(slug=slug)
    print("THIS PART WORKS!")

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():  # valid captcha
            photo = form.save(commit=False)
            photo.contest = contest_record
            photo.ownername = request.user
            photo.isChecked = False
            photo.isDeleted = False
            photo.save()

            # User'ın o conteste yükleyeceği İlk fotoğraf ise böyle contender objesi yoktur, o objeyi oluşturalım.
            if not Contender.objects.filter(user=request.user, contest=contest_record).exists():
                contender = Contender(user=request.user, contest=contest_record)
                contender.save()

            file = open('check.txt', 'a')
            file.write(photo.filename())
            file.write("\n")
            file.close()

            # Mesaj ve redirection işlemleri
            messages.success(request, 'You have succesfully sent a photo to photo pool')
            return HttpResponseRedirect(contest_record.get_absolute_url())

        else:  # user entered an invalid captcha
            messages.error(request, 'Invalid input for reCaptcha. Please make sure you enter the correct letters')
            return HttpResponseRedirect(request.path_info)  # redirect to the same page

    else:  # GET
        if timezone.now() > contest_record.end_date:
            return render(request, 'contest/contest_ended.html')
        try:  # if there is not any Contender object, get() will raise an exception
            the_contender = Contender.objects.get(user=request.user, contest=contest_record)

            if the_contender.get_number_of_photos_uploaded() >= contest_record.max_photos_per_Reguser:
                return render(request, 'contest/maxreached.html')
        except Contender.DoesNotExist:
            pass

        form = PhotoForm()
        context = {
            'form': form,
        }

        return render(request, 'photo/form.html', context)

def contest_photopool(request, slug):
    # O contest'e ait fotoğrafları contestid'sinden tanıyıp, ayrıştırıp öyle veriyoruz photo/index.html dosyasına.
    contest = Contest.objects.get(slug=slug)
    context = {'contest': contest}
    if request.GET.get('p'):
        query = request.GET.get('p')
        if int(query) in [photo.id for photo in Photo.objects.filter(contest=contest)]:
            context['query'] = query

    return render(request, "contest/photopool.html", context)


def contest_delete(request, id):
    contest = get_object_or_404(Contest, id=id)
    contest.delete()
    return redirect("contest:index")

def contest_rankings(request, slug):
    contest = get_object_or_404(Contest, slug=slug)

    context = {'contest': contest}

    if timezone.now() < contest.end_date:  # if contest is still in progress
        return render(request, "contest/contest_still_in_progress.html", context)

    return render(request, "contest/rankings.html", context)

