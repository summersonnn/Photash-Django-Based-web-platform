import re

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
if hasattr(settings, 'COMMON_URLS'):
    COMMON_URLS = [re.compile(url) for url in settings.COMMON_URLS]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        #Request'ın user'ı var mı diye kontrol eder.
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        print(path)

        #Şu an erişmeye çalıştığın url exempt ni değil mi? True-False
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        url_is_common = any(url.match(path) for url in COMMON_URLS)

        if path == 'user/logout/':
            logout(request)

        #Kullanıcı girişi yapıldıysa ve url muaf url'ler arasındaysa
        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)
        #Logged in - Muaf değil  veya  Logged out - Muaf  Bu durumlar istenmeyen durumlar değildir
        elif request.user.is_authenticated or url_is_exempt:
            return None
        #Logged in ve Logged out userların ortak erişebileceği urllerden ise
        elif not request.user.is_authenticated and url_is_common:
            return None
        #Logged in değil ve sadece Logged in userların ulaşabildiği bir url ise
        else:
            return redirect(settings.LOGIN_URL)


