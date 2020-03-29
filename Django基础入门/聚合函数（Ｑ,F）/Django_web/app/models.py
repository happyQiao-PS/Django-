from django.db import models

# Create your models here.
class myManager(models.Manager):
    def create_Grade(self,name="hello"):
        obj = self.model()
        obj.g_name = name
        return obj
    def create_Student(self,name="hello",fk=1):
        obj = self.model()
        obj.s_name = name
        obj.fk = fk
        return obj

class Grade(models.Model):
    g_name = models.CharField(max_length=16)
    object = myManager()

class Student(models.Model):
    s_name = models.CharField(max_length=16)
    s_fk = models.ForeignKey(Grade)
    object = myManager()