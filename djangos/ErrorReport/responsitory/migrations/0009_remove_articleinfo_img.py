# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-03 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('responsitory', '0008_auto_20180702_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleinfo',
            name='img',
        ),
    ]
