# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-02-03 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForeignkeySearch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food_lover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=20)),
                ('f_Eat', models.IntegerField()),
            ],
        ),
    ]
