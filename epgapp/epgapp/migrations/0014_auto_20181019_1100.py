# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0013_auto_20181015_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grabbingscheduler',
            name='settings',
        ),
        migrations.AddField(
            model_name='settings',
            name='convert_times',
            field=models.BooleanField(default=True, verbose_name='Convert times to local time'),
        ),
        migrations.AddField(
            model_name='settings',
            name='instances',
            field=models.IntegerField(default=1, help_text='The maximum number of WebGrab processes running at the same time', verbose_name='Number of processes'),
        ),
        migrations.AddField(
            model_name='settings',
            name='only_title',
            field=models.BooleanField(default=True, verbose_name='Copy only title of timeshifted channels'),
        ),
        migrations.AddField(
            model_name='settings',
            name='remove_empty',
            field=models.BooleanField(default=True, verbose_name='Remove channels with no programmes'),
        ),
        migrations.AddField(
            model_name='settings',
            name='report',
            field=models.BooleanField(default=True, verbose_name='Generate report file'),
        ),
        migrations.AddField(
            model_name='settings',
            name='run_interval',
            field=models.IntegerField(default=1, verbose_name='Run every N days'),
        ),
        migrations.AddField(
            model_name='settings',
            name='start_time',
            field=models.CharField(default='05:00', max_length=5),
        ),
        migrations.AddField(
            model_name='settings',
            name='timeout',
            field=models.IntegerField(default=40, help_text='Minutes to wait before killing the WebGrab process', verbose_name='Process timeout'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='mode',
            field=models.ManyToManyField(default='', help_text='Hold the Shift key to select multiple values', to='epgapp.Modes', verbose_name='Modes'),
        ),
        migrations.DeleteModel(
            name='GrabbingScheduler',
        ),
    ]