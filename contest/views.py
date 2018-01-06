from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Contest, Contender
from photo.models import Photo
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

# Create your views here.
def contest_index(request):
    contest_list = Contest.objects.all()

    query = request.GET.get("q")
    if query:
        #Sadece contest_name ile kalmayıp başka fieldlar içinde arama yapmasını sağlayabiliriz. Detay: https://www.youtube.com/watch?v=eyAIAZr5Q3w
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
    #request.POST.get('slug')
    contest = get_object_or_404(Contest, slug = slug)

    context = {
        'contest': contest,
    }

    if request.user.is_authenticated:
        if Contender.objects.filter(user=request.user, contest=contest).count() > 0:
            contender = Contender.objects.get(user=request.user, contest=contest)
            context['contender'] = contender
    return render(request, "contest/detail.html", context)

def contest_delete(request, slug):
    contest = get_object_or_404(Contest, slug = slug)
    contest.delete()
    return redirect("contest:index")

def contest_rankings(request, slug):
    contest = Contest.objects.get(slug=slug)
    photo = Photo.objects.filter(contest=contest).filter(ratings__isnull=False).order_by('-ratings__average')

    context = {
        'photos': photo,
    }
    if timezone.now() > contest.end_date:
        return render(request, "contest/rankings.html", context)
    else:
        context['thecontest']=contest
        return render(request, "contest/contest_still_in_progress.html", context)
