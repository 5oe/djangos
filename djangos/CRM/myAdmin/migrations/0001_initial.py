# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-20 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='测试', max_length=10, verbose_name='测试标题')),
            ],
            options={
                'verbose_name_plural': '用于测试admin的表',
                'db_table': 'TestAdmin',
            },
        ),
    ]
