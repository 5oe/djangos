from django.db import models
from . import *

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserInfo(models.Model):
    user = models.ForeignKey(User, verbose_name='用户名')
    role = models.ManyToManyField('RoleInfo', verbose_name='角色')
    img = models.ImageField(upload_to='head', verbose_name='头像', blank=True, null=True)
    identity_id = models.CharField(max_length=18, verbose_name='身份证号码', unique=True)

    class Meta:
        db_table = 'UserInfo'
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.user.username


class RoleInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='角色名', unique=True)
    menu = models.ManyToManyField('MenuInfo', verbose_name='菜单', blank=True, null=True)

    class Meta:
        db_table = 'RoleInfo'
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.title


class CourseInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='课程名')
    price = models.PositiveIntegerField(verbose_name='价格')
    outline = models.TextField(verbose_name='课程大纲')
    cyc = models.PositiveIntegerField(verbose_name='课程周期(月)')

    class Meta:
        db_table = 'CourseInfo'
        verbose_name_plural = '课程表'

    def __str__(self):
        return self.title


