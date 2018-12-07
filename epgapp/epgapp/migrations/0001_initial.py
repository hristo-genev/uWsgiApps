# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-12 15:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name of channel')),
                ('xmltv_id', models.CharField(max_length=32, verbose_name='Channel id in XMLTV')),
                ('enabled', models.BooleanField(default=False)),
                ('update', models.CharField(blank=True, choices=[('', ''), ('i', 'i - Incremental'), ('l', 'l - Light'), ('s', 's - Smart'), ('f', 'f - Forced')], default='', max_length=1)),
                ('offset', models.IntegerField(default=0)),
                ('include', models.CharField(blank=True, max_length=256)),
                ('exclude', models.CharField(blank=True, max_length=256)),
                ('period', models.CharField(blank=True, max_length=16)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='epgapp.Channel', verbose_name='Timeshift of')),
            ],
        ),
        migrations.CreateModel(
            name='Epg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.CharField(max_length=20)),
                ('stop', models.CharField(max_length=20)),
                ('program', models.TextField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epgapp.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='Grabbers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.CharField(blank=True, max_length=32)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epgapp.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='epg.xml', max_length=256, verbose_name='Output file path')),
                ('update', models.CharField(blank=True, choices=[('', ''), ('i', 'i - Incremental'), ('l', 'l - Light'), ('s', 's - Smart'), ('f', 'f - Forced')], default='', max_length=1, verbose_name='Update type')),
                ('logging', models.BooleanField(default=True, verbose_name='Enabled logging')),
                ('timespan', models.IntegerField(default=0, verbose_name='Days to grab')),
                ('hours', models.CharField(blank=True, max_length=5)),
                ('keeppastdays', models.IntegerField(default=0)),
                ('skip', models.CharField(default='noskip', max_length=10)),
                ('mode', models.CharField(default='n', max_length=48)),
                ('postprocess_grab', models.BooleanField(default=True)),
                ('postprocess_run', models.BooleanField(default=False)),
                ('postprocess_name', models.CharField(choices=[('mdb', 'mdb'), ('rex', 'rex')], default='mdb', max_length=3)),
                ('max_retries', models.IntegerField(default=6)),
                ('retry_timeout', models.IntegerField(default=10)),
                ('channeldelay', models.IntegerField(default=0)),
                ('indexdelay', models.IntegerField(default=0)),
                ('showdelay', models.IntegerField(default=0)),
                ('proxy_server', models.CharField(blank=True, default='', max_length=256)),
                ('proxy_user', models.CharField(blank=True, default='', max_length=16)),
                ('proxy_password', models.CharField(blank=True, default='', max_length=16)),
                ('useragent', models.CharField(blank=True, max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Siteini',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name of siteini file')),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='grabbers',
            name='siteini',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epgapp.Siteini'),
        ),
        migrations.AddField(
            model_name='channel',
            name='siteinis',
            field=models.ManyToManyField(through='epgapp.Grabbers', to='epgapp.Siteini'),
        ),
    ]
