from django.db import models

class Student(models.Model):
    s_sid = models.IntegerField(default=1)
    s_name = models.CharField(max_length=16)
    s_age = models.IntegerField(default=1)
    s_hobby =  models.CharField(max_length=48)
    
