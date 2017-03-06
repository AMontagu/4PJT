# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20170306_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='qwirkgroup',
            name='isContactGroup',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='qwirkgroup',
            name='admin',
            field=models.ManyToManyField(to='project.QwirkUser'),
        ),
    ]
