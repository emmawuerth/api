# Generated by Django 3.1.14 on 2023-01-17 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_queue', '0004_auto_20220615_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='last_run',
            field=models.DateField(blank=True, null=True),
        ),
    ]