# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 08:36
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_qwirkuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/adrien/git/4PJT/server/../web-app/static/media/files'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='qwirkuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/adrien/git/4PJT/server/../web-app/static/media/files'), upload_to=''),
        ),
    ]
