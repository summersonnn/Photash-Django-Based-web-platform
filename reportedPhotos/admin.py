from django.contrib import admin
from .models import ReportedPhotos

# Register your models here.
class ReportedPhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'photoid', 'howmany_reports']
    list_display_links = ['id']
    list_filter = ['photoid']
    search_fields = ['photoid']

    class Meta:
        model = ReportedPhotos

admin.site.register(ReportedPhotos, ReportedPhotosAdmin)