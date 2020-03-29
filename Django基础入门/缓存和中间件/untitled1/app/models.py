from django.db import models

# Create your models here.
class LoadPic(models.Model):
    load_name = models.CharField(max_length=16)
    load_img = models.ImageField(upload_to="icon")