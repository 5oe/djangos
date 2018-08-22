# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-18 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course2Direct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '课程与方向关系表',
                'db_table': 'Course2Direct',
            },
        ),
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True, verbose_name='课程标题')),
                ('img', models.ImageField(upload_to='upload/course', verbose_name='图片')),
                ('content', models.CharField(max_length=1200, verbose_name='课程描述')),
                ('level', models.ImageField(choices=[(1, '初级'), (2, '中级'), (3, '高级'), (4, '骨灰级')], default=1, upload_to='', verbose_name='课程等级')),
            ],
            options={
                'verbose_name_plural': '课程表',
                'db_table': 'CourseInfo',
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='课程类型')),
            ],
            options={
                'verbose_name_plural': '课程类型表',
                'db_table': 'CourseType',
            },
        ),
        migrations.CreateModel(
            name='DirectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='方向')),
            ],
            options={
                'verbose_name_plural': '方向类型表',
                'db_table': 'DirectType',
            },
        ),
        migrations.CreateModel(
            name='EnterpriseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='企业名')),
                ('content', models.CharField(max_length=1200, verbose_name='描述内容')),
                ('img', models.ImageField(upload_to='upload/enterprise', verbose_name='图片')),
                ('href', models.CharField(max_length=250, verbose_name='链接')),
            ],
            options={
                'verbose_name_plural': '企业表',
                'db_table': 'EnterpriseInfo',
            },
        ),
        migrations.CreateModel(
            name='LifeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='标题')),
                ('content', models.CharField(max_length=1200, verbose_name='具体描述')),
                ('img', models.ImageField(upload_to='upload/life', verbose_name='图片')),
            ],
            options={
                'verbose_name_plural': '学员生活表',
                'db_table': 'LifeInfo',
            },
        ),
        migrations.CreateModel(
            name='NoticeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='公告标题')),
                ('content', models.CharField(max_length=1200, verbose_name='公告内容')),
                ('weight', models.IntegerField(default=0, verbose_name='权重')),
            ],
            options={
                'verbose_name_plural': '公告表',
                'db_table': 'NoticeInfo',
            },
        ),
        migrations.CreateModel(
            name='NoticeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='公告类型')),
            ],
            options={
                'verbose_name_plural': '公告类型表',
                'db_table': 'NoticeType',
            },
        ),
        migrations.CreateModel(
            name='RecruitInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='招聘标题')),
                ('content', models.CharField(max_length=1200, verbose_name='详细内容')),
                ('salary', models.IntegerField(verbose_name='薪资')),
                ('start_date', models.DateTimeField(verbose_name='发布日期')),
                ('end_date', models.DateTimeField(null=True, verbose_name='过期日期')),
            ],
            options={
                'verbose_name_plural': '招聘信息发布表',
                'db_table': 'RecruitInfo',
            },
        ),
        migrations.CreateModel(
            name='SliderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='upload/Slider', verbose_name='图片')),
                ('href', models.CharField(max_length=250, verbose_name='链接')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('status', models.IntegerField(choices=[(0, '下线'), (1, '上线')], default=1, verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '首页轮播表',
                'db_table': 'SliderInfo',
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='姓名')),
                ('birthday', models.DateField(verbose_name='生日')),
                ('company', models.CharField(max_length=50, verbose_name='工作所在公司名称')),
                ('salary', models.IntegerField(verbose_name='薪资')),
                ('img', models.ImageField(upload_to='upload/student', verbose_name='图片')),
            ],
            options={
                'verbose_name_plural': '学员表',
                'db_table': 'StudentInfo',
            },
        ),
        migrations.CreateModel(
            name='StudentThanksInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1200, verbose_name='感谢描述')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index_slider.StudentInfo', unique=True, verbose_name='学员')),
            ],
            options={
                'verbose_name_plural': '学员感谢信息表',
                'db_table': 'StudentThanksInfo',
            },
        ),
        migrations.AddField(
            model_name='noticeinfo',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index_slider.NoticeType', verbose_name='公告类型'),
        ),
        migrations.AddField(
            model_name='course2direct',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index_slider.CourseInfo', verbose_name='课程'),
        ),
        migrations.AddField(
            model_name='course2direct',
            name='direct',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index_slider.DirectType', verbose_name='方向'),
        ),
    ]