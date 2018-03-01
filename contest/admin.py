from django.contrib import admin
from .models import Contest, Contender, Tag

class ContestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("contest_name",)}
    list_display = ['id', 'contest_name', 'tag']
    list_display_links = ['contest_name']
    list_filter = ['id']
    search_fields = ['contest_name']

    class Meta:
        model = Contest

class ContenderAdmin(admin.ModelAdmin):
    list_display = ['user', 'contest']
    list_display_links = ['user']
    list_filter = ['user']
    search_fields = ['user']

    class Meta:
        model = Contender


admin.site.register(Tag)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Contender, ContenderAdmin)

