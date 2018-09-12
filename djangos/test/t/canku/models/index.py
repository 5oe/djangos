from django.db import models
from . import *

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class UserInfo(models.Model):
#     user = models.ForeignKey(User, verbose_name='用户名')
#     role = models.ManyToManyField('RoleInfo', verbose_name='角色')
#     img = models.ImageField(upload_to='head', verbose_name='头像', blank=True, null=True)
#     identity_id = models.CharField(max_length=18, verbose_name='身份证号码', unique=True)
#
#     class Meta:
#         db_table = 'UserInfo'
#         verbose_name_plural = '用户表'
#
#     def __str__(self):
#         return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.ManyToManyField('RoleInfo', verbose_name='角色')
    img = models.ImageField(upload_to='head', verbose_name='头像', blank=True, null=True)
    identity_id = models.CharField(max_length=18, verbose_name='身份证号码', unique=True)

    def __str__(self):
        return self.user.username

    # 设置3个权限字段，拥有权限者可操作此表(在admin中授权用户)
    class Meta:
        permissions = (
            ('view_customer_list', u"查看客户列表@@@@@"),  # 权限字段名称及其解释
            ('view_customer_info', u"查看客户详情!!!!!!!"),
            ('edit_own_customer_info', u"修改客户信息!!!!!!!!!"),
        )


class RoleInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='角色名', unique=True)
    menu = models.ManyToManyField('MenuInfo', verbose_name='菜单', blank=True, null=True)

    class Meta:
        db_table = 'RoleInfo'
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ('crm_table_list', '可以查看@@@@@@@@@@@每张表里所有的数据'),
            ('crm_table_list_view', '可以访!!!!!!!!!!表里每条数据的修改页'),
            ('crm_table_list_change', '可以对XXXXXXXn表里的每条数据进行修改'),
            ('crm_table_obj_add_view', '可以访问kAAAAAadmin每张表的数据增加页'),
            ('crm_table_obj_add', '可以对kingadmin每张表进行数据添加'),
            ('crm_table_obj_add1', 'QWDAkingadmin每张表进行数据添加'),

        )


class MenuInfo(models.Model):
    url_type_choices = [(0, '固定url'), (1, '动态url')]

    title = models.CharField(max_length=64, verbose_name='菜单名')
    url_type = models.SmallIntegerField(choices=url_type_choices, verbose_name='URL类型')
    url_name = models.CharField(max_length=128, verbose_name='URL后缀')

    class Meta:
        db_table = 'MenuInfo'
        verbose_name_plural = '菜单表'

    def __str__(self):
        return self.title
