# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0016_auto_20181019_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='grabbers',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
