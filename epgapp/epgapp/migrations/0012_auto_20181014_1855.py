# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0011_auto_20181014_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grabbingscheduler',
            name='start',
        ),
        migrations.AddField(
            model_name='grabbingscheduler',
            name='run_interval',
            field=models.IntegerField(default=1, verbose_name='Run every N days'),
        ),
        migrations.AddField(
            model_name='grabbingscheduler',
            name='start_time',
            field=models.CharField(default='05:00', max_length=5),
        ),
        migrations.AlterField(
            model_name='grabbingscheduler',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Scheduler name'),
        ),
        migrations.AlterField(
            model_name='grabbingscheduler',
            name='settings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epgapp.Settings', verbose_name='WebGrab configuration'),
        ),
    ]
