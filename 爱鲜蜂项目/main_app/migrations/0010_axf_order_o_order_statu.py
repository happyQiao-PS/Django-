# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-04 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_axf_order_axf_ordergoods'),
    ]

    operations = [
        migrations.AddField(
            model_name='axf_order',
            name='o_order_statu',
            field=models.IntegerField(default=0),
        ),
    ]
