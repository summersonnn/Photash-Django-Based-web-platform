from django import template
from reportedPhotos.models import ReportedPhotos
register = template.Library()

@register.filter
def checkandincrease(photoid):
    if ReportedPhotos.objects.filter(photoid=photoid).count() != 0:
        report = ReportedPhotos.objects.get(photoid=photoid)
    else:
        report = ReportedPhotos(photoid=photoid)


    report.howmany_reports += 1
    report.save()
    return True