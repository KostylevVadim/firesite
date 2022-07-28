from django.db import models

# Create your models here.
class Fire(models.Model):
    _id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    type_id = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    class Meta:
        verbose_name_plural = "fires"
    def __str__(self):
        return self.name