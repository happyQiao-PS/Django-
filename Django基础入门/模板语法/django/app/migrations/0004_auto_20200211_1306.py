# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-02-11 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200211_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='c_goods',
            field=models.ManyToManyField(null=True, to='app.Goods'),
        ),
    ]
