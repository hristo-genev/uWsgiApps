# Generated by Django 2.1.2 on 2018-10-26 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epgapp', '0023_auto_20181026_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postprocess',
            name='name',
        ),
        migrations.AddField(
            model_name='postprocess',
            name='type',
            field=models.CharField(choices=[('mdb', 'mdb'), ('rex', 'rex')], default='mdb', help_text='The name of the process to run. "mdb" or "rex"', max_length=3, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='postprocess',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='epgapp.Postprocess'),
        ),
    ]
