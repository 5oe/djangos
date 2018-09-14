from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group, Permission
from . import *
from utils.permissions import items


class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        :type username: object
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    # 用户名，无需设置密码，因为AbstractBaseUser提供了User类最核心的实现，
    # 包括哈希的passwords和 标识的密码重置。
    username = models.CharField(max_length=64, verbose_name="姓名")
    # 必须定义。 一个布尔属性，标识用户是否是 "active" 的。AbstractBaseUser默认为 Ture。
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)
    role = models.ManyToManyField("RoleInfo", blank=True, null=True)

    objects = UserProfileManager()

    # 必须设置。 设置认证标识，设置成标识的字段 unique=True
    USERNAME_FIELD = 'email'
    # 必须设置。当通过createsuperuser管理命令创建一个用户时，用于提示的一个字段名称列表。
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # 必须定义。 long格式的用户标识。
        return self.email

    def get_short_name(self):
        # 必须定义。 short格式的用户标识。
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    class Meta:
        # permissions = (
        #     ('crm_table_list', '可以查看@@@@@@@@@@@每张表里所有的数据'),
        #     ('crm_table_list_view', '可以访!!!!!!!!!!表里每条数据的修改页'),
        #     ('crm_table_list_change', '可以对XXXXXXXn表里的每条数据进行修改'),
        #     ('crm_table_obj_add_view', '可以访问kAAAAAadmin每张表的数据增加页'),
        #     ('crm_table_obj_add', '可以对kingadmin每张表进行数据添加'),
        #     ('crm_table_obj_add1', 'QWDAkingadmin每张表进行数据添加'),
        #
        # )
        permissions = items.permissions


class RoleInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='角色名', unique=True)
    menu = models.ManyToManyField('MenuInfo', verbose_name='菜单', blank=True, null=True)

    class Meta:
        db_table = 'RoleInfo'
        # verbose_name_plural = '角色表'

    def __str__(self):
        return self.title


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

