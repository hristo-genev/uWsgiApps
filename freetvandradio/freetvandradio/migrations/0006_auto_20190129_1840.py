# Generated by Django 2.1.5 on 2019-01-29 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freetvandradio', '0005_auto_20190128_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stream',
            old_name='user_agent_id',
            new_name='user_agent',
        ),
    ]