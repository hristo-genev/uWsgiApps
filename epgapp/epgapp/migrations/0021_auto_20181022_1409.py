# Generated by Django 2.1.2 on 2018-10-22 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0020_auto_20181022_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='epg',
            old_name='program',
            new_name='desc',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='programs',
        ),
    ]
