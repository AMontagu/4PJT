# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20170102_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='qwirkuser',
            name='contacts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.QwirkUser'),
        ),
    ]
