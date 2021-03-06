# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-02-27 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_axf_foodtypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='axf_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_username', models.CharField(max_length=128)),
                ('u_email', models.CharField(max_length=48)),
                ('u_password', models.CharField(max_length=128)),
                ('u_icon', models.ImageField(upload_to='icon/%Y/%m/%d')),
                ('u_isactivate', models.BooleanField(default=False)),
                ('u_isdelete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'axf_user',
            },
        ),
    ]
