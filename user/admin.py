from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
'''class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'firstname', 'lastname', 'location', 'aboutme']
    list_display_links = ['user']
    list_filter = ['location']
    search_fields = ['firstname']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)'''

