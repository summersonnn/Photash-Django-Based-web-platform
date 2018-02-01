from django.shortcuts import render, HttpResponse

def home_view(request):
    #Dinamik template için
    '''if request.user.is_authenticated():
        context = {
            'isim': 'Kubilay',
        }
    else:
        context = {
            'isim': 'Misafir',
        }
    '''
    return render(request, 'home.html', {})


