# Generated by Django 3.0.14 on 2021-06-28 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0099_auto_20210628_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importeduser',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='database.UserProfile'),
        ),
    ]
