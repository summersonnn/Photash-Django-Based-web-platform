from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm
from .models import Photo
from contest.models import Contest, Contender
from django.contrib.auth.models import User
from star_ratings.models import Rating
from django.contrib import messages

# Create your views here.
# Create your views here.
def photo_create(request, contestslug):
    # Fotoğrafın hangi contest'in pool'una gideceği bilgisini çektik. Bu bilgi contest detail'indeki Join Contest butonu ile verilmişti.
    contest_record = Contest.objects.get(slug=contestslug)
    if not request.user.is_authenticated:
        return Http404()

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit = False)
            photo.contest = contest_record
            photo.ownername = request.user
            photo.save()

            #Fotoğrafı kaydettik. Şimdi fotoğrafın sahibi(contender) için updateleri uygulayacağız.
            #İlk fotoğrafı değil ise Contender objesi daha önceden oluşmuş demektir. O halde:
            if Contender.objects.filter(user=request.user, contest=contest_record).count() != 0:
                contender = Contender.objects.get(user=request.user, contest=contest_record)
            #İlk fotoğrafı ise böyle bir obje yoktur, o objeyi oluşturalım.
            else:
                contender = Contender(user=request.user, contest=contest_record)
            contender.howmany_photos_owned += 1
            contender.save()

            #Mesaj ve redirection işlemleri
            messages.success(request, 'You have succesfully sent a photo to photo pool')
            return HttpResponseRedirect(contest_record.get_absolute_url())
    else: #GET
        #Daha önce bu contest'e upload yapmadıysa VEYA yaptıklarının sayısı max'ı geçmiyorsa, form'u gösteriyoruz.
        if  Contender.objects.filter(user=request.user, contest=contest_record).count() == 0 or Contender.objects.get(user=request.user, contest=contest_record).howmany_photos_owned < contest_record.max_photos_per_Reguser:
            form = PhotoForm()
        else:
            return render(request, 'contest/maxreached.html')

    context = {
        'form': form,
        }
    return render(request, 'photo/form.html', context)

@login_required
def get_photo_rating(request, id):
    object = Photo.objects.get(id=id)
    return render(request, 'photo/ratings.html', context={"photo": object})

def photo_index(request, contestslug):
    #O contest'e ait fotoğrafları contestid'sinden tanıyıp, ayrıştırıp öyle veriyoruz photo/index.html dosyasına.
    contestz = Contest.objects.get(slug=contestslug)
    photos = Photo.objects.filter(contest=contestz)
    context = {
        'photos': photos,
        'contest': contestz,
    }
    return render(request, "photo/index.html", context)

def photo_detail(request, id):
    photo = get_object_or_404(Photo, id = id)
    content_type = ContentType.objects.get_for_model(Photo)
    object_id = photo.id
    rating = Rating.objects.get(content_type = content_type, object_id = object_id)
    context = {
        'photo': photo,
        'rating': rating,
    }
    return render(request, "photo/detail.html", context)

def photo_delete(request, id):

    if not request.user.is_authenticated():
        return Http404()

    photo = get_object_or_404(Photo, id = id)
    photo.delete()
    return redirect("photo:index")