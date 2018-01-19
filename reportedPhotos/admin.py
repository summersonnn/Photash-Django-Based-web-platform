from django.contrib import admin
from .models import ReportedPhotos

# Register your models here.
class ReportedPhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'howmany_reports']
    list_display_links = ['id']

    class Meta:
        model = ReportedPhotos

admin.site.register(ReportedPhotos, ReportedPhotosAdmin)