# Generated by Django 3.2 on 2022-11-19 13:26

import common.common
from django.db import migrations, models
import web_editor.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20220728_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='css',
            field=models.FileField(blank=True, storage=web_editor.storage_backends.BuildFileStorage(), upload_to=common.common.file_upload_path),
        ),
        migrations.AlterField(
            model_name='project',
            name='html',
            field=models.FileField(blank=True, storage=web_editor.storage_backends.BuildFileStorage(), upload_to=common.common.file_upload_path),
        ),
        migrations.AlterField(
            model_name='project',
            name='js',
            field=models.FileField(blank=True, storage=web_editor.storage_backends.BuildFileStorage(), upload_to=common.common.file_upload_path),
        ),
    ]
