from django.db import models
from photo.models import Photo

# Create your models here.
class ReportedPhotos(models.Model):
    #id = models.IntegerField(primary_key = True, verbose_name= "Report id")
    #photoid = models.IntegerField(verbose_name="Reported photo id")
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, null=True)
    howmany_reports = models.IntegerField(blank = False, default = 0, verbose_name="How many time reported?")
    isOpen = models.BooleanField(blank = False, default = True, verbose_name="Is the report is open?")
    isHandled = models.BooleanField(blank = False, default = False, verbose_name="Have any admins took a look at it?")
    isDeleted = models.BooleanField(blank = False, default = False, verbose_name="Is the reported photo deleted?")
