# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-04 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20170922_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='payed_paid_pilgy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='payed_paid_pilgy'),
        ),
        migrations.AddField(
            model_name='payments',
            name='payed_paid_subs',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='payed_paid_subs'),
        ),
        migrations.AddField(
            model_name='payments',
            name='payed_paid_user',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='payed_paid_user'),
        ),
    ]
