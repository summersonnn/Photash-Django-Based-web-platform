from django.db import models
from datetime import datetime
from django.urls import reverse
#from django_resized import ResizedImageField  ----> önceden Imagefield yerine ResizedImagefield kullanıyordum. Ama o sekılde orijinal boyutlarıyla upload etmiyordu. Degıstırdım. Kutuphanesi hala burada.
from django.db.models.signals import pre_delete  #R eceive the pre_delete signal and delete the file associated with the model instance.
from django.dispatch.dispatcher import receiver
import os

def get_upload_path(instance, filename):
    return 'photopool/contest_{0}/{1}'.format(instance.contest.slug, filename)

# Create your models here.
class Photo(models.Model):
    # Aynı fotoğraf farklı contestlerde farklı id'ye sahip olacağından tek primary key photoid (belki bunu değiştirebilirim)
    id = models.IntegerField(primary_key=True, verbose_name='Photo id')
    photoItself = models.ImageField(upload_to=get_upload_path, default='blog/static/manzara.jpg', verbose_name='Photo')
    ownername = models.ForeignKey('auth.User', verbose_name='Name of the owner of the photo', on_delete=models.CASCADE, related_name='photos')
    contest = models.ForeignKey('contest.Contest', verbose_name='Contest name', on_delete=models.CASCADE, related_name='photos')
    likes = models.ManyToManyField ('auth.User', blank=True, related_name="photo_likes")
    seenby = models.ManyToManyField('auth.User', blank=True, related_name="photo_seen_by")
    uploading_date = models.DateTimeField(default=datetime.now, verbose_name="Yüklenme Tarihi")
    summary = models.TextField(max_length=48, blank=True)
    isChecked = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ("ekle_photo", "Can add new photos?"),
            ("oyla_photo", "Can vote photos?"),
        )

    def __str__(self):
        return str(self.id)

    def filename(self):
        return os.path.basename(self.photoItself.name)

    def get_absolute_url(self):
        return reverse('photo:detail', kwargs={'id': self.id})

    @property
    def like_percentage(self):
        try:
            per = self.likes.all().count()*100/self.seenby.all().count()
        except ZeroDivisionError:
            per = 0
        return per
    #If you want only 2 digits after comma, print(round(photo.like_percentage(), 2))


@receiver(pre_delete, sender=Photo)
def mymodel_delete(sender, instance, **kwargs):
    instance.photoItself.delete(False)

