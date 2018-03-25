from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'contest', 'ownername']
    list_display_links = ['id']
    list_filter = ['contest']
    search_fields = ['ownername']

    class Meta:
        model = Photo

admin.site.register(Photo, PhotoAdmin)
