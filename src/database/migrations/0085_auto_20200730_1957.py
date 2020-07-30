# Generated by Django 3.0.7 on 2020-07-30 19:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0084_action_deep_dive'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='communitymember',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='aboutuspagesettings',
            name='social_media_links',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='primary_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='action_category', to='database.Tag'),
        ),
        migrations.AddField(
            model_name='actionspagesettings',
            name='social_media_links',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='contactuspagesettings',
            name='social_media_links',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='donatepagesettings',
            name='social_media_links',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='goal',
            name='target_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='favicon_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favicon', to='database.Media'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='featured_events_description',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='featured_stats_description',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='show_footer_social_media',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='show_footer_subscribe',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='social_media_links',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AddField(
            model_name='impactpagesettings',
            name='social_media_links',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='image',
            field=models.ManyToManyField(related_name='team_image', to='database.Media'),
        ),
        migrations.AddField(
            model_name='team',
            name='is_closed',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Team'),
        ),
        migrations.AddField(
            model_name='team',
            name='tagline',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='team_page_options',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_video', to='database.Media'),
        ),
        migrations.AddField(
            model_name='useractionrel',
            name='carbon_impact',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='useractionrel',
            name='date_completed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepagesettings',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='homepage_images', to='database.Media'),
        ),
        migrations.AlterField(
            model_name='impactpagesettings',
            name='featured_video_link',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='VendorsPageSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=10000)),
                ('sub_title', models.CharField(blank=True, max_length=10000)),
                ('description', models.TextField(blank=True, max_length=10000)),
                ('featured_video_link', models.CharField(blank=True, max_length=100)),
                ('social_media_links', models.CharField(blank=True, max_length=10000, null=True)),
                ('more_info', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('is_template', models.BooleanField(blank=True, default=False)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Community')),
                ('images', models.ManyToManyField(blank=True, to='database.Media')),
            ],
            options={
                'verbose_name_plural': 'VendorsPageSettings',
                'db_table': 'vendors_page_settings',
            },
        ),
        migrations.CreateModel(
            name='TeamsPageSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=10000)),
                ('sub_title', models.CharField(blank=True, max_length=10000)),
                ('description', models.TextField(blank=True, max_length=10000)),
                ('featured_video_link', models.CharField(blank=True, max_length=100)),
                ('social_media_links', models.CharField(blank=True, max_length=10000, null=True)),
                ('more_info', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('is_template', models.BooleanField(blank=True, default=False)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Community')),
                ('images', models.ManyToManyField(blank=True, to='database.Media')),
            ],
            options={
                'verbose_name_plural': 'TeamsPageSettings',
                'db_table': 'teams_page_settings',
            },
        ),
    ]
