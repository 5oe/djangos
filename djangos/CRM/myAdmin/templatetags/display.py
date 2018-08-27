from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def display(value_dict):
    return value_dict.get('display', None) or value_dict['value']


@register.filter
def get_id(config_dict):
    return config_dict['id']['value']
