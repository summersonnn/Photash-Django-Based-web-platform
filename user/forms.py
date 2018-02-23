from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label="Username")
    password = forms.CharField(max_length=20, label="Password", widget=forms.PasswordInput)

    # Clean fonksiyonu override edildi.
    def clean(self):
        # Cleaned_data fonksiyonu girişi onayladıysa değişkenlere veri aktarır. Onaylanmazsa, boş kalır. Bu yüzden aşağıdaki if'te boş mu dolu mu diye kontrol ediyoruz.
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Incorrect username or password')
        return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=20, label="Username")
    email = forms.CharField(max_length=40, label="E-mail")
    first_name = forms.CharField(max_length=20, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    password1 = forms.CharField(max_length=20, label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
        ]


# ------------------------------------------------------------------------------------------------------


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'aboutme')
