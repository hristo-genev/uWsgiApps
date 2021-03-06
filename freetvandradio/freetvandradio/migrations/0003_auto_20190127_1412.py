# Generated by Django 2.1.5 on 2019-01-27 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freetvandradio', '0002_auto_20190127_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='logo',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Channel logo'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='comment',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Comments'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='preferred',
            field=models.IntegerField(blank=True, default=1, verbose_name='Preference number'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='stream_url',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Stream url'),
        ),
    ]
