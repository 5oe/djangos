# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-03 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responsitory', '0010_articleinfo_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleinfo',
            name='read',
            field=models.IntegerField(default=0, verbose_name='阅读量'),
        ),
    ]
