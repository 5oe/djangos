from django.db import models
from . import *


class StudentInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name='学员名')
    identity_id = models.CharField(max_length=18, verbose_name='身份证号码', unique=True)
    password = models.CharField(max_length=30, verbose_name='密码')
    cls = models.ManyToManyField('ClsInfo', verbose_name='所在班级')

    class Meta:
        db_table = 'StudentInfo'
        verbose_name_plural = '学员表'

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    contact_choices = [(0, 'qq'), (1, '微信'), (2, '电话联系')]
    source_choices = [(0, 'qq群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其他论坛')]
    status_choices = [(0, '未报名'), (1, '已报名'), (2, '已退学')]

    name = models.CharField(max_length=20, default='匿名用户')
    time = models.DateTimeField(auto_now_add=True, verbose_name='发掘时间')
    source = models.PositiveIntegerField(choices=source_choices, verbose_name='来源')
    contact = models.PositiveIntegerField(choices=contact_choices, verbose_name='联系方式')
    consultant = models.ForeignKey('UserInfo', verbose_name='课程顾问')
    status = models.PositiveIntegerField(choices=status_choices, verbose_name='状态')
    consult_courses = models.ManyToManyField('CourseInfo', verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询内容')
    introduce_customer = models.ForeignKey('self', blank=True, null=True, verbose_name='转介绍学员')

    class Meta:
        db_table = 'CustomerInfo'
        verbose_name_plural = '客户表'

    def __str__(self):
        return self.name


class CustomerFollowUpInfo(models.Model):
    status_choices = [
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '2周内要报名'),
        (3, '已报名')
    ]
    customer = models.ForeignKey('CustomerInfo', verbose_name='客户')
    content = models.TextField(verbose_name='跟踪内容')
    handler = models.ForeignKey('UserInfo', verbose_name='跟进入')
    status = models.SmallIntegerField(choices=status_choices, verbose_name='状态')
    date = models.DateField(auto_now_add=True, verbose_name='日期')

    class Meta:
        db_table = 'CustomerFollowUpInfo'
        verbose_name_plural = '客户跟踪表'

    def __str__(self):
        return '%s 跟踪 %s' % (self.handler.username, self.customer.name)


class QuestionInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    detail = models.TextField(verbose_name='问题详述')
    student = models.ForeignKey('StudentInfo', verbose_name='提问学生')

    class Meta:
        db_table = 'QuestionInfo'
        verbose_name_plural = '提交问题表'

    def __str__(self):
        return self.title
