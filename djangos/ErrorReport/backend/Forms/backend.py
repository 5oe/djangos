from django import forms
from django.forms import fields
from django.forms import widgets


class TroubleInfoForm(forms.Form):
    title = fields.CharField(
        min_length=2,
        max_length=225,
        error_messages={
            'min_length': '长度不能少于2',
            'max_length': '长度不能大于225',
            'required': '标题必须填写',
        },
        label='标题',
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'id': 'artcle_title',
            'placeholder': "请输入文章标题",
        })
    )

    detail = fields.CharField(
        max_length=3000,
        required=False,
        error_messages={
            'max_length': '内容不能超过3000'
        },
        label='内容',
        widget=widgets.Textarea(attrs={
            'class': 'form-control',
            'id': 'artcle_detail',
            'rows': "10",
            'placeholder': "请输入文章内容"
        })
    )

    solution = fields.CharField(
        error_messages={
            'required': '必须填写解决方案',
        },
        label='解决方案',
        widget=widgets.Textarea(attrs={
            'class': 'form-control',
            'id': 'solution_detail',
            'rows': "15",
            'placeholder': "请输入解决方案内容"
        })
    )
