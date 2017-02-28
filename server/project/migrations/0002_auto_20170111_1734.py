# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='group',
            new_name='qwirkGroup',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='qwirkUser',
        ),
        migrations.AlterField(
            model_name='qwirkgroup',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
