# Generated by Django 2.1.5 on 2019-01-27 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freetvandradio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_agent',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='user_agent',
            name='string',
            field=models.CharField(max_length=512, verbose_name='String'),
        ),
    ]
