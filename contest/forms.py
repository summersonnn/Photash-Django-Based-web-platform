from django import forms
from photo.models import *


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = [
            'photoItself'
        ]
