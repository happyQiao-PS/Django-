# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-02-03 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForeignkeySearch', '0002_food_lover'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrueOrFalse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('True_or_false', models.BooleanField(default=False)),
            ],
        ),
    ]
