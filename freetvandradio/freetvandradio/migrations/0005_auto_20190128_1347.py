# Generated by Django 2.1.5 on 2019-01-28 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freetvandradio', '0004_auto_20190127_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='page_url',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Page url'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='player_url',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Player url'),
        ),
    ]