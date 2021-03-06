# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-06 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('responsitory', '0012_auto_20180705_0005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billinfo',
            old_name='time',
            new_name='submit_time',
        ),
        migrations.AddField(
            model_name='billinfo',
            name='evaluate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='billinfo',
            name='handler_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='处理时间'),
        ),
        migrations.AlterField(
            model_name='billinfo',
            name='handler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='handlers', to='responsitory.UsrInfo', verbose_name='处理者'),
        ),
        migrations.AlterField(
            model_name='billinfo',
            name='submitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submiters', to='responsitory.UsrInfo', verbose_name='用户'),
        ),
    ]
