from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Photo, Rating

# Register your models here.
class RatingInline(GenericTabularInline):
    model = Rating


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'contest', 'ownername']
    list_display_links = ['id']
    list_filter = ['contest']
    search_fields = ['ownername']
    inlines = [
        RatingInline,
    ]

    class Meta:
        model = Photo

admin.site.register(Photo, PhotoAdmin)
