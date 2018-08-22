from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from responsitory.models import *


class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseForm, self).__init__(*args, **kwargs)


# class TestForm(BaseForm, forms.Form):
#     # def __init__(self, request, *args, **kwargs):
#     #     self.request = request
#     #     super().__init__(*args, **kwargs)
#
#     username = fields.CharField(
#         min_length=6,
#         max_length=20,
#         error_messages={'required': 'server:用户名不能为空',
#                         'min_length': 'server:用户名长度不能少于6',
#                         'max_length': 'server:用户名长度最长不能超过20',
#                         'invalid': 'server:用户名已经存在'
#                         },
#         label='测试',
#     )


class LoginForm(BaseForm, forms.Form):
    username = fields.CharField(
        error_messages={'required': '用户名不能为空',
                        },
        widget=widgets.TextInput(attrs={'name': 'username', 'placeholder': "请输入用户名", \
                                        'class': 'form-control', 'id': 'username'}),
        label='用户名',
    )

    password = fields.CharField(
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'name': 'password', 'placeholder': "请输入密码", \
                                            'class': 'form-control', 'id': 'password'}),
        label='密码',
    )

    verify = fields.CharField(
        error_messages={'required': '验证码不能为空'},
        widget=widgets.TextInput(attrs={'name': 'verify', 'placeholder': "请输入验证码", \
                                        'class': 'form-control', 'id': 'verify'}),
        label='验证码',
    )

    auto = forms.CharField(
        label='一个月内自动登录',
        widget=widgets.CheckboxInput(attrs={'id': "auto", 'name': 'auto'}),
        required=False,
    )

    # def clean_username(self):
    #     username = self.request.POST.get('username')
    #     try:
    #         UsrInfo.objects.get(username=username)
    #     except UsrInfo.DoesNotExist:
    #         raise ValidationError('用户名不存在')
    #     else:
    #         return self.cleaned_data['username']
    #
    # def clean_password(self):
    #     username = self.cleaned_data.get('username', '')
    #     if not username:
    #         return
    #     password = self.request.POST.get('password')
    #     user = UsrInfo.objects.get(username=username)
    #     if user.password == password:
    #         return self.cleaned_data['password']
    #     else:
    #         raise ValidationError('密码错误')
    #
    # def clean_auto(self):
    #     auto = self.request.POST.get('auto', '')
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     if username and password and auto:
    #         user = UsrInfo.objects.filter(username=username, password=password).values(
    #              'username', 'password', 'email', 'phone','img',
    #         ).first()
    #         self.request.session['user'] = user
    #         self.request.session.set_expiry(60 * 60 * 24 * 30)

    def clean_verify(self):
        user_verify_code = self.request.POST.get('verify', '').upper()
        verify_code = self.request.session.get('verify_code').upper()
        if user_verify_code != verify_code:
            raise ValidationError(message='验证码错误', code='invalid')


class RegiseterForm(BaseForm, forms.Form):
    username = fields.CharField(
        min_length=1,
        max_length=20,
        error_messages={'required': 'server:用户名不能为空',
                        'max_length': 'server:用户名长度最长不能超过20',
                        },
        widget=widgets.TextInput(attrs={'name': 'username', 'placeholder': "请输入用户名", \
                                        'class': 'form-control', 'id': 'username'}),
        label='用户名',
    )

    password = fields.CharField(
        min_length=6,
        max_length=20,
        widget=widgets.PasswordInput(attrs={'name': 'password', 'placeholder': "请输入密码", \
                                            'class': 'form-control', 'id': 'password'}),
        error_messages={'required': 'server:密码不能为空',
                        'min_length': 'server:密码长度不能少于6',
                        'max_length': 'server:密码长度最长不能超过20',
                        },
        validators=[RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$', '密码必须包含大小写字母和数字')],
        label='密码',
    )

    confirm = fields.CharField(
        min_length=6,
        max_length=20,
        widget=widgets.PasswordInput(attrs={'name': 'confirm', 'placeholder': "请再次输入密码", \
                                            'class': 'form-control', 'id': 'confirm'}),
        error_messages={'required': 'server:密码不能为空',
                        'min_length': 'server:密码长度不能少于6',
                        'max_length': 'server:密码长度最长不能超过20',
                        },
        label='确认密码',
    )

    phone = fields.CharField(
        min_length=11,
        max_length=12,
        error_messages={'required': 'server:手机号码不能为空',
                        'min_length': 'server:号码必须为11位或者12位',
                        'max_length': 'server:号码必须为11位或者12位',
                        },
        validators=[RegexValidator(r'^1[0-9]{10,11}$', '手机号码格式错误'), ],
        label='电话号码',
        widget=widgets.TextInput(attrs={'name': 'phone', 'placeholder': "请输入手机号码", \
                                        'class': 'form-control', 'id': 'phone'}),
    )

    email = fields.EmailField(
        error_messages={'required': 'server:邮箱不能为空',
                        'invalid': '邮箱格式错误',
                        },
        label='邮箱',
        widget=widgets.TextInput(attrs={'name': 'email', 'placeholder': "请输入邮箱", \
                                        'class': 'form-control', 'id': 'email'})
    )

    verify = fields.CharField(
        error_messages={'required': '验证码不能为空', },
        label='验证码',
        widget=widgets.TextInput(attrs={'name': 'verify', 'placeholder': "请输入验证码", \
                                        'class': 'form-control', 'id': 'verify'})
    )

    def clean_username(self):
        username = self.request.POST.get('username', '')
        res = UsrInfo.objects.filter(username=username)
        if len(res):
            raise ValidationError(message='用户名已经存在了哦！', code='invalid')
        else:
            return self.cleaned_data['username']

    def clean_verify(self):
        user_verify_code = self.request.POST.get('verify', '').upper()
        verify_code = self.request.session.get('verify_code').upper()
        if user_verify_code != verify_code:
            raise ValidationError(message='验证码错误', code='invalid')

    def clean_confirm(self):
        p1 = self.request.POST.get('password', '')
        p2 = self.request.POST.get('confirm', '')
        if p1 != p2:
            raise ValidationError('密码不一致')

            # def clean(self):
            #     '''
            #     测试整体验证
            #     :return:
            #     '''
            #     p1 = self.cleaned_data.get('password', '')
            #     if not p1:
            #         raise ValidationError('整体信息')
