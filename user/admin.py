from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'aboutme']
    list_display_links = ['user']
    list_filter = ['location']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)

