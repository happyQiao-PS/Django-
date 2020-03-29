from django.db import models

# Create your models here.

class grade(models.Model):
    g_name = models.CharField(max_length=16)


class student(models.Model):
    s_name = models.CharField(max_length=16)
    s_grade = models.ForeignKey(grade)