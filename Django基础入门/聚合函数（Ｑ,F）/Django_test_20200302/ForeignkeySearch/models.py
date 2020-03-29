from django.db import models

# Create your models here.
class Classroom(models.Model):
    c_name = models.CharField(max_length=20,db_column="classroom_name")

class Student(models.Model):
    s_name = models.CharField(max_length=20,db_column="student_name")
    s_classroom = models.ForeignKey(Classroom)

class Food_lover(models.Model):
    f_name = models.CharField(max_length=20)
    f_Eat = models.IntegerField()

class Do_T_Or_F(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(True_or_false=False)
    def create_obj(self,Do=False):
        a = self.model()
        a.True_or_false = Do
        return a

class TrueOrFalse(models.Model):
    True_or_false = models.BooleanField(default=False)
    objects = Do_T_Or_F()
