# Generated by Django 2.1.2 on 2018-11-29 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0032_auto_20181129_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteini',
            name='slug',
            field=models.SlugField(default='', help_text='How it appears in URL', max_length=32, verbose_name='Slug'),
        ),
    ]
