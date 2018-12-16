# Generated by Django 2.1.2 on 2018-12-15 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0046_siteini_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='alt_names',
        ),
        migrations.AddField(
            model_name='alternativename',
            name='channel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='epgapp.Channel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alternativename',
            name='name',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]