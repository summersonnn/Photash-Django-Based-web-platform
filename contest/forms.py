from django import forms
from photo.models import *
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class PhotoForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    photo_caption = forms.CharField(max_length=90, widget=forms.TextInput(attrs={'placeholder': 'Enter your caption here'}))
    class Meta:
        model = Photo
        fields = [
            'photoItself',
            'photo_caption'
        ]

