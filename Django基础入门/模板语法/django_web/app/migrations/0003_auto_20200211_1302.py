# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-02-11 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200211_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='c_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='goods',
            name='g_name',
            field=models.CharField(max_length=128),
        ),
    ]
