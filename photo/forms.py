from django import forms
from .models import Photo
from captcha.fields import ReCaptchaField

class PhotoForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Photo
        fields = [
            'photoItself'
        ]
