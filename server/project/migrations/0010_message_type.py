# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20170504_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='type',
            field=models.TextField(default='message'),
            preserve_default=False,
        ),
    ]