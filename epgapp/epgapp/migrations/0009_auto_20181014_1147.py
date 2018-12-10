# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0008_auto_20181014_1017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='broadcaster',
            options={'ordering': ['-name'], 'verbose_name_plural': 'Broadcasters'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': ' Categories'},
        ),
        migrations.AlterModelOptions(
            name='channel',
            options={'ordering': ['-name'], 'verbose_name_plural': '    Channels'},
        ),
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Configurations', 'verbose_name_plural': 'WebGrab Settings'},
        ),
        migrations.AlterModelOptions(
            name='siteini',
            options={'ordering': ['-name'], 'verbose_name_plural': '  Siteinis'},
        ),
        migrations.AddField(
            model_name='settings',
            name='name',
            field=models.CharField(default='Linux', max_length=256, verbose_name='Configuration name'),
        ),
    ]