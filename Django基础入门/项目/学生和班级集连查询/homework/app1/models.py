from django.db import models


# Create your models here.


class Grade(models.Model):
    g_name = models.CharField(max_length=16)


class Student(models.Model):
    s_name = models.CharField(max_length=16)
    s_sex = models.CharField(max_length=4, default="男")
    s_age = models.IntegerField(default=18)
    s_hobby = models.CharField(max_length=16)
    s_grade = models.ForeignKey(Grade)
