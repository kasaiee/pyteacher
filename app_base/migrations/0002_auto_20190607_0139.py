# Generated by Django 2.2.1 on 2019-06-06 21:09

import app_base.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesession',
            name='video',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/mrz/workspace/pyteacher/media/'), upload_to=app_base.models.get_upload_path),
        ),
    ]
