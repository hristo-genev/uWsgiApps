# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0007_auto_20181014_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]