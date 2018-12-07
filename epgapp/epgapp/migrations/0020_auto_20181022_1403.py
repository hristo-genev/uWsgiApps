# Generated by Django 2.1.2 on 2018-10-22 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0019_auto_20181020_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='programs',
            field=models.ManyToManyField(blank=True, default='', related_name='programmes', to='epgapp.Epg'),
        ),
        migrations.AddField(
            model_name='epg',
            name='audio',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='epg',
            name='category',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='epg',
            name='credits',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='epg',
            name='date',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='epg',
            name='episode',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='epg',
            name='ori_title',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='epg',
            name='rating',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='epg',
            name='sub_title',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='epg',
            name='subtitles',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='epg',
            name='title',
            field=models.CharField(default='No title', max_length=1024),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=models.SlugField(help_text='Name in URL', max_length=32, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='epg',
            name='program',
            field=models.TextField(blank=True),
        ),
    ]
