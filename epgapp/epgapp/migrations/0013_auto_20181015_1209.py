# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-15 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0012_auto_20181014_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.RemoveField(
            model_name='grabbingscheduler',
            name='config_dir',
        ),
        migrations.RemoveField(
            model_name='grabbingscheduler',
            name='report_dir',
        ),
        migrations.RemoveField(
            model_name='grabbingscheduler',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='grabbingscheduler',
            name='temp_dir',
        ),
        migrations.RemoveField(
            model_name='grabbingscheduler',
            name='webgrab_dir',
        ),
        migrations.AlterField(
            model_name='grabbingscheduler',
            name='instances',
            field=models.IntegerField(default=1, help_text='The maximum number of WebGrab processes running at the same time', verbose_name='Number of processes'),
        ),
        migrations.AlterField(
            model_name='grabbingscheduler',
            name='timeout',
            field=models.IntegerField(default=40, help_text='Minutes to wait before killing the WebGrab process', verbose_name='Process timeout'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='channeldelay',
            field=models.IntegerField(default=0, help_text='Delay between grabbing of subsequent channels', verbose_name='Channel delay'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='filename',
            field=models.CharField(default='epg.xml', help_text='Name of the xtml file that will be generated', max_length=32, verbose_name='Output file name'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='hours',
            field=models.CharField(blank=True, help_text='HH:mm time which will reduce the grab to only the one show (per day)', max_length=5, verbose_name='One show hour (debug)'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='indexdelay',
            field=models.IntegerField(default=0, help_text='Delay between grabbing of index pages', verbose_name='Index delay'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='keeppastdays',
            field=models.IntegerField(blank=True, help_text='Retain the epg of a number of past days', verbose_name='Keep last N days'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='logging',
            field=models.BooleanField(default=True, help_text='Change Webgrab logging behavior', verbose_name='Enable logging'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='max_retries',
            field=models.IntegerField(default=6, help_text='Number of times the engine will retry to capture a page', verbose_name='Max retries'),
        ),
        migrations.RemoveField(
            model_name='settings',
            name='mode',
        ),
        migrations.AlterField(
            model_name='settings',
            name='name',
            field=models.CharField(help_text='Name of the current configuration set to distinguish between multiple configurations', max_length=256, verbose_name='Configuration name'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='postprocess_grab',
            field=models.BooleanField(default=True, help_text='Specifies if the EPG grabbing is run first', verbose_name='Grab'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='postprocess_name',
            field=models.CharField(choices=[('mdb', 'mdb'), ('rex', 'rex')], default='mdb', help_text='The name of the process to run. "mdb" or "rex"', max_length=3, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='postprocess_run',
            field=models.BooleanField(default=False, help_text='Specifies if a post process is run', verbose_name='Run'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='proxy_password',
            field=models.CharField(blank=True, default='', help_text='The password needed by the proxy', max_length=16),
        ),
        migrations.AlterField(
            model_name='settings',
            name='proxy_server',
            field=models.CharField(blank=True, default='', help_text='Proxy server address:port or "automatic" ', max_length=256),
        ),
        migrations.AlterField(
            model_name='settings',
            name='proxy_user',
            field=models.CharField(blank=True, default='', help_text='The user name needed by the proxy', max_length=16),
        ),
        migrations.AlterField(
            model_name='settings',
            name='retry_timeout',
            field=models.IntegerField(default=10, help_text='Delay between retries', verbose_name='Time between retries'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='showdelay',
            field=models.IntegerField(default=0, help_text='Delay between grabbing of detail show pages', verbose_name='Show delay'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='skip',
            field=models.CharField(default='noskip', help_text='Available values: H,m or noskip', max_length=10),
        ),
        migrations.AlterField(
            model_name='settings',
            name='timespan',
            field=models.IntegerField(default=0, help_text='The first is the number of days (including today) to download, note that 0 is today.', verbose_name='Days to grab'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='update',
            field=models.CharField(blank=True, choices=[('', ''), ('i', 'i - Incremental'), ('l', 'l - Light'), ('s', 's - Smart'), ('f', 'f - Forced')], default='', help_text='Global update behaviour. Leave empty so evey channels uses its own update value', max_length=1, verbose_name='Update type'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='useragent',
            field=models.CharField(blank=True, help_text="Add any user-agent or just 'random' and the program will generate a random string", max_length=512),
        ),
        migrations.AddField(
            model_name='settings',
            name='mode',
            field=models.ManyToManyField(default='', help_text='Available values: debug, measure, nomark, verify, wget', to='epgapp.Modes'),
        ),
    ]
