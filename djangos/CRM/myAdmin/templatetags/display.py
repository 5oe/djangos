from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def display(value_dict):
    return value_dict.get('display', None) or value_dict['value']


@register.filter
def get_id(config_dict):
    return config_dict['id']['value']


@register.filter
def can_show_other_link(bound_field):
    """
    :param field: field组件化的对象,里面有一个field参数
    :return: 当field是外键字段时返回True。否则返回False
    """
    from django.forms.models import ModelChoiceField
    field = bound_field.field
    if isinstance(field, ModelChoiceField):
        return True
    return False


# @register.filter
# def can_show_change_link(bound_field):
#     """
#
#     :param bound_field: field组件化的对象,里面有一个field参数
#     :return: 当field的组件是CharField类型或者TextField返回True。否则返回False
#     """
#     field = bound_field.field
#     from django.forms.widgets import Textarea, TextInput
#     from django.forms.fields import DateTimeField, DateField
#     widget = field.widget
#     if isinstance(widget, Textarea) or isinstance(widget, TextInput):
#         if type(field) != DateField and type(field) != DateTimeField:
#             return True
#     return False


@register.simple_tag
def get_field_cls_name(cls_info, field):
    """
    返回field字段所指向的模型类的类名
    :param:cls_info: 模型类
    :param field: 字段名字符串
    :return: 
    """
    field_obj = cls_info._meta.get_field(field)
    related_model = field_obj.related_model
    return related_model.__name__


@register.simple_tag
def get_field_app_name(cls_info, field):
    """
    返回field字段所指向的模型类所在的app名字
    :param cls_info: 模型类
    :param field:  字段名字符串
    :return: 
    """
    field_obj = cls_info._meta.get_field(field)
    related_model = field_obj.related_model
    return related_model._meta.app_label
