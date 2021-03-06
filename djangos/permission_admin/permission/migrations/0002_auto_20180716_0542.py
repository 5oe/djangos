# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-16 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='age',
            field=models.IntegerField(default='13', verbose_name='年龄'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='cls',
            field=models.CharField(default='初二13班', max_length=20, verbose_name='班级'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='password',
            field=models.CharField(default='freedom', max_length=20, verbose_name='密码'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='place',
            field=models.CharField(default='广东省东莞市塘厦镇', max_length=50, verbose_name='所在地'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='school',
            field=models.CharField(default='塘厦初级中学', max_length=30, verbose_name='学校'),
        ),
    ]
