# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-15 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='菜单名')),
                ('partent_menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permission.MenuInfo', verbose_name='父菜单')),
            ],
            options={
                'verbose_name_plural': '菜单表',
                'db_table': 'MenuInfo',
            },
        ),
        migrations.CreateModel(
            name='Permission2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '角色权限表',
                'db_table': 'Permission2Role',
            },
        ),
        migrations.CreateModel(
            name='PermissionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '行为权限表',
                'db_table': 'PermissionInfo',
            },
        ),
        migrations.CreateModel(
            name='RoleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='角色名')),
            ],
            options={
                'verbose_name_plural': '角色表',
                'db_table': 'RoleInfo',
            },
        ),
        migrations.CreateModel(
            name='UrlActionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, verbose_name='说明')),
                ('title', models.CharField(blank=True, max_length=20, null=True, verbose_name='get参数字符串')),
            ],
            options={
                'verbose_name_plural': '行为表',
                'db_table': 'UrlActionInfo',
            },
        ),
        migrations.CreateModel(
            name='UrlInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, verbose_name='说明')),
                ('url_name', models.CharField(max_length=225, verbose_name='url标志')),
                ('menu', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='permission.MenuInfo', verbose_name='归属菜单')),
            ],
            options={
                'verbose_name_plural': 'url表',
                'db_table': 'UrlInfo',
            },
        ),
        migrations.CreateModel(
            name='User2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.RoleInfo', verbose_name='角色')),
            ],
            options={
                'verbose_name_plural': '用户->角色表',
                'db_table': 'User2Role',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
            ],
            options={
                'verbose_name_plural': '用户表',
                'db_table': 'UserInfo',
            },
        ),
        migrations.AddField(
            model_name='user2role',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.UserInfo', verbose_name='用户'),
        ),
        migrations.AlterUniqueTogether(
            name='urlactioninfo',
            unique_together=set([('caption', 'title')]),
        ),
        migrations.AddField(
            model_name='permissioninfo',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.UrlActionInfo', verbose_name='行为'),
        ),
        migrations.AddField(
            model_name='permissioninfo',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.UrlInfo', verbose_name='url'),
        ),
        migrations.AddField(
            model_name='permission2role',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.PermissionInfo', verbose_name='行为权限'),
        ),
        migrations.AddField(
            model_name='permission2role',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.RoleInfo', verbose_name='角色'),
        ),
    ]
