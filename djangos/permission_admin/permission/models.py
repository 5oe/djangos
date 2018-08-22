from django.db import models


class UserInfo(models.Model):
    sex_choices = [(1, '男'), (2, '女')]
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=20, verbose_name='密码', default='freedom')
    age = models.IntegerField(verbose_name='年龄', default='13')
    sex = models.IntegerField(choices=sex_choices, verbose_name='性别', default=1)
    school = models.CharField(max_length=30, verbose_name='学校', default='塘厦初级中学')
    cls = models.CharField(max_length=20, verbose_name='班级', default='初二13班')
    place = models.CharField(max_length=50, verbose_name='所在地', default='广东省东莞市塘厦镇')


    class Meta:
        verbose_name_plural = '用户表'
        db_table = 'UserInfo'

    def __str__(self):
        return self.username


class RoleInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='角色名')

    class Meta:
        verbose_name_plural = '角色表'
        db_table = 'RoleInfo'

    def __str__(self):
        return self.title


class UrlInfo(models.Model):
    caption = models.CharField(max_length=50, verbose_name='说明')
    url_name = models.CharField(max_length=225, verbose_name='url标志')
    menu = models.ForeignKey('MenuInfo', on_delete=models.CASCADE, verbose_name='归属菜单', null=True, blank=True, \
                             default=None)

    class Meta:
        verbose_name_plural = 'url表'
        db_table = 'UrlInfo'

    def __str__(self):
        return self.caption + ' : ' + self.url_name


class UrlActionInfo(models.Model):
    caption = models.CharField(max_length=50, verbose_name='说明')
    title = models.CharField(max_length=20, verbose_name='get参数字符串', blank=True, null=True)

    class Meta:
        verbose_name_plural = '行为表'
        db_table = 'UrlActionInfo'
        unique_together = ('caption', 'title')

    def __str__(self):
        return self.caption + ' : ' + self.title


class User2Role(models.Model):
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='用户')
    role = models.ForeignKey('RoleInfo', on_delete=models.CASCADE, verbose_name='角色')

    class Meta:
        verbose_name_plural = '用户->角色表'
        db_table = 'User2Role'

    def __str__(self):
        return self.user.username + ' -> ' + self.role.title


class PermissionInfo(models.Model):
    # Url2Action
    url = models.ForeignKey('UrlInfo', on_delete=models.CASCADE, verbose_name='url')
    action = models.ForeignKey('UrlActionInfo', on_delete=models.CASCADE, verbose_name='行为')

    class Meta:
        verbose_name_plural = '行为权限表'
        db_table = 'PermissionInfo'

    def __str__(self):
        return self.url.url_name + '  : ' + self.action.title


class Permission2Role(models.Model):
    permission = models.ForeignKey('PermissionInfo', on_delete=models.CASCADE, verbose_name='行为权限')
    role = models.ForeignKey('RoleInfo', on_delete=models.CASCADE, verbose_name='角色')

    class Meta:
        verbose_name_plural = '角色权限表'
        db_table = 'Permission2Role'

    def __str__(self):
        return str(self.permission) + '->' + self.role.title


class MenuInfo(models.Model):
    title = models.CharField(max_length=30, verbose_name='菜单名')
    partent_menu = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='父菜单', blank=True, null=True, )

    class Meta:
        verbose_name_plural = '菜单表'
        db_table = 'MenuInfo'

    def __str__(self):
        return self.title
