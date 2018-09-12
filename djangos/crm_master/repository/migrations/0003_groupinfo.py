# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-09 12:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('repository', '0002_auto_20180909_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupInfo',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
            ],
            options={
                'verbose_name_plural': '权限组',
            },
            bases=('auth.group',),
        ),
    ]