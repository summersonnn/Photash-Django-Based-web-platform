from django import forms
from photo.models import *
from captcha.fields import ReCaptchaField


class PhotoForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Photo
        fields = [
            'photoItself'
        ]
