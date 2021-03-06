# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-17 11:56
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_id', models.CharField(max_length=100, verbose_name='contract id')),
                ('contract_descr', models.CharField(blank=True, max_length=100, verbose_name='contract desc')),
            ],
            options={
                'verbose_name_plural': 'Contracts Ids',
                'verbose_name': 'Contract Id',
            },
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(max_length=500, null=True, unique=True, verbose_name='Contract type name')),
            ],
            options={
                'verbose_name_plural': 'Contract Types',
                'verbose_name': 'Contract Type',
            },
        ),
        migrations.CreateModel(
            name='CountersValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_user', models.IntegerField(blank=True, null=True, verbose_name='user counter value')),
                ('value_vodocanal', models.IntegerField(blank=True, null=True, verbose_name='vodocanal counter value')),
                ('registration_time', models.DateTimeField(null=True, verbose_name='time of value registration')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.ContractId')),
            ],
            options={
                'verbose_name_plural': 'Counter values',
                'verbose_name': 'Counter value',
            },
        ),
        migrations.CreateModel(
            name='DbInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(default='', max_length=50, verbose_name='db host')),
                ('database', models.CharField(default='', max_length=50, verbose_name='db name')),
                ('user', models.CharField(default='', max_length=50, verbose_name='user name')),
                ('password', models.CharField(default='', max_length=50, verbose_name='user password')),
            ],
            options={
                'verbose_name_plural': 'Db info',
                'verbose_name': 'Db info',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(verbose_name='add time')),
                ('payed_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='payed paid')),
                ('to_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='to pay')),
            ],
            options={
                'verbose_name_plural': 'Payments',
                'verbose_name': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=500, null=True, unique=True, verbose_name='Service type name')),
                ('contract_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.ContractType')),
            ],
            options={
                'verbose_name_plural': 'Service Types',
                'verbose_name': 'Service Type',
            },
        ),
        migrations.CreateModel(
            name='UsersModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_first_last', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='user first last name')),
                ('state', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='user state')),
                ('town', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='user town')),
                ('street', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='user street')),
                ('house', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='user house')),
                ('phone', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='user phone number')),
                ('current_key', models.CharField(max_length=50, null=True, unique=True, verbose_name='current session key')),
                ('key_expire', models.DateTimeField(null=True, unique=True, verbose_name='key expire date')),
            ],
            options={
                'verbose_name_plural': 'Users Model',
                'verbose_name': 'User Model',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.UsersModel'),
        ),
        migrations.AddField(
            model_name='contractid',
            name='service',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.ServiceType'),
        ),
        migrations.AddField(
            model_name='contractid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.UsersModel'),
        ),
    ]
