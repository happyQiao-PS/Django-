from django.db import models

# Create your models here.
class HaloDjango(models.Model):
    s_name = models.CharField(max_length=20,unique=True,db_column="name")
    s_age = models.IntegerField(default=0,db_column="age",unique=True)
    s_happy = models.CharField(max_length=40,db_column="happy")
    @classmethod
    def create_obj(cls,name='halo',age=0,happy="1"):
        return cls(s_name=name,s_age=age,s_happy=happy)
    class Meta:
        db_table = "happyDjango"


