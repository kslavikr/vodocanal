# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-23 13:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_logmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='user',
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
    ]
