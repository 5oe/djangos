from django.db import models
from . import *


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
    detail = models.ForeignKey('CustomerDetailInfo', blank=True, null=True, verbose_name='报名时的详细信息')

    class Meta:
        db_table = 'CustomerInfo'
        verbose_name_plural = '客户表'

    def __str__(self):
        return '%s发掘的 %s' % (self.time.strftime('%Y-%m-%d %H-%M'), self.name)


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
        return '%s 跟踪 %s' % (self.handler, self.customer.name)


class CourseInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='课程名')
    price = models.PositiveIntegerField(verbose_name='价格')
    outline = models.TextField(verbose_name='课程大纲')
    cyc = models.PositiveIntegerField(verbose_name='课程周期(月)')

    class Meta:
        db_table = 'CourseInfo'
        verbose_name_plural = '课程条目信息表'

    def __str__(self):
        return self.title


class ContractTemplateInfo(models.Model):
    """
    合同模版
    """
    title = models.CharField(max_length=64, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    create_date = models.DateField(auto_now_add=True, verbose_name='创建日期')

    class Meta:
        db_table = 'ContractTemplate'
        verbose_name_plural = '合同模版'

    def __str__(self):
        return self.title


class EnrollmentInfo(models.Model):
    customer = models.ForeignKey('CustomerInfo', verbose_name='顾客')
    cls = models.ForeignKey('ClsInfo', verbose_name='班级')
    # course = models.ForeignKey('CourseInfo', verbose_name='报名课程', default=1)
    consultant = models.ForeignKey('UserInfo', verbose_name='招待员(销售)')
    contract_agreed = models.BooleanField(default=False, verbose_name='达成协议？')
    contract_agreed_date = models.DateTimeField(blank=True, null=True, verbose_name='合同签订日期时间')
    contract_approved = models.BooleanField(default=False, verbose_name='审核通过？')
    contract_approved_date = models.DateTimeField(blank=True, null=True, verbose_name='合同审核日期时间')

    class Meta:
        db_table = 'EnrollmentInfo'
        unique_together = ['customer', 'consultant']

    def __str__(self):
        return '顾客 %s 与 销售 %s 的报名协议' % (self.customer.name, self.consultant.username)


class PaymentRecordInfo(models.Model):
    payment_type_choices = [(0, '报名费'), (1, '学费'), (2, '退费')]

    enrollment = models.ForeignKey('EnrollmentInfo', verbose_name='报名相关信息')
    payment_type = models.SmallIntegerField(choices=payment_type_choices, default=0, verbose_name='付费类型')
    amount = models.IntegerField(verbose_name='数额')
    pay_date = models.DateTimeField(auto_now_add=True, verbose_name='付费日期时间')

    class Meta:
        db_table = 'PaymentRecordInfo'

    def __str__(self):
        return '%s 付费记录' % self.enrollment.customer.name


class CustomerDetailInfo(models.Model):
    name = models.CharField(max_length=8, verbose_name='真实姓名')
    identity_id = models.CharField(max_length=18, verbose_name='身份号码', unique=True)
    id_img_path = models.ImageField(verbose_name='身份证照片路径', unique=True, null=True)
    passport_img_path = models.ImageField(verbose_name='户口本照片路径', unique=True, null=True)
    birthday = models.DateField(verbose_name='出生日期')
    sex = models.SmallIntegerField(choices=[(0, '男'), (1, '女')], verbose_name='性别', default=0)
    phone = models.CharField(max_length=12, verbose_name='电话', unique=True)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    qq = models.CharField(max_length=16, verbose_name='qq账号', unique=True)
    wechar = models.CharField(max_length=32, verbose_name='微信号', null=True, blank=True, unique=True)
    work_status = models.SmallIntegerField(choices=[(0, '无业'), (1, '在职')], verbose_name='职业状态')
    place = models.CharField(max_length=32, verbose_name='居住地点')
    contract = models.ForeignKey('ContractTemplateInfo', verbose_name='合同')

    class Meta:
        db_table = 'CustomerDetailInfo'
        verbose_name_plural = '加入时必填信息表'

    def __str__(self):
        return '%s 的信息表' % self.name
