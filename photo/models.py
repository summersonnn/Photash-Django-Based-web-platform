from django.db import models
from datetime import datetime
from django.urls import reverse
from django_resized import ResizedImageField  # önceden Imagefield yerine ResizedImagefield kullanıyordum. Ama o sekılde orijinal boyutlarıyla upload etmiyordu. Degıstırdım. Kutuphanesi hala burada.
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.db.models.signals import pre_delete  #R eceive the pre_delete signal and delete the file associated with the model instance.
from django.dispatch.dispatcher import receiver
from contest.models import Contender


# Create your models here.
class Photo(models.Model):
    # Aynı fotoğraf farklı contestlerde farklı id'ye sahip olacağından tek primary key photoid (belki bunu değiştirebilirim)
    id = models.IntegerField(primary_key=True, verbose_name='Photo id')
    photoItself = models.ImageField(upload_to='photopool/', default='blog/static/manzara.jpg', verbose_name='Photo')
    ownername = models.ForeignKey('auth.User', verbose_name='Name of the owner of the photo', on_delete=models.CASCADE, related_name='photos')
    contest = models.ForeignKey('contest.Contest', verbose_name='Contest name', on_delete=models.CASCADE, related_name='photos')

    # auto_now_add=True, koymaya çalıştım fakat default istedi. default ile ikisini aynı anda koymama da izin vermedi.
    # Sadece default koyabildim.
    uploading_date = models.DateTimeField(default=datetime.now, verbose_name="Yüklenme Tarihi")
    ratings = GenericRelation(Rating, related_query_name='photos')

    # Photo.objects.filter(ratings__isnull=False).order_by('ratings__average') ile sıralama yapılıyor.

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('photo:detail', kwargs={'id': self.id})


@receiver(pre_delete, sender=Photo)
def mymodel_delete(sender, instance, **kwargs):
    instance.photoItself.delete(False)

