# Generated by Django 2.1.5 on 2019-01-27 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': ' Categories',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disabled', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name of channel')),
                ('logo', models.CharField(max_length=1024, verbose_name='Channel logo')),
                ('epg_id', models.CharField(max_length=64, verbose_name='Channel id in XMLTV')),
                ('slug', models.SlugField(help_text='Name in URL', max_length=64, unique=True, verbose_name='Slug')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ordering', models.IntegerField(default=999)),
                ('category', models.ManyToManyField(blank=True, default='', to='freetvandradio.Category')),
            ],
            options={
                'verbose_name_plural': '    Channels',
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream_url', models.CharField(max_length=1024, verbose_name='Stream url')),
                ('page_url', models.CharField(max_length=1024, verbose_name='Page url')),
                ('player_url', models.CharField(max_length=1024, verbose_name='Player url')),
                ('comment', models.CharField(max_length=1024, verbose_name='Comments')),
                ('preferred', models.IntegerField(verbose_name='Preference number')),
                ('disabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freetvandradio.Channel')),
            ],
            options={
                'verbose_name_plural': '  Streams',
            },
        ),
        migrations.CreateModel(
            name='User_Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name of channel')),
                ('string', models.CharField(max_length=32, verbose_name='Name of channel')),
            ],
            options={
                'verbose_name_plural': 'User Agents',
            },
        ),
        migrations.AddField(
            model_name='stream',
            name='user_agent_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freetvandradio.User_Agent'),
        ),
    ]
