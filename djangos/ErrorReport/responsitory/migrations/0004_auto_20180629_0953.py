# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-29 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responsitory', '0003_articleinfo_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleinfo',
            name='index_kind',
            field=models.IntegerField(choices=[(1, '技术'), (2, '新闻'), (3, '其他')], default=2, verbose_name='总分类'),
        ),
        migrations.AlterField(
            model_name='bloginfo',
            name='surfix',
            field=models.CharField(max_length=10, unique=True, verbose_name='后缀'),
        ),
    ]