from django import template
from django.utils.safestring import mark_safe
import copy

from myAdmin.templatetags.lib import remove_previous_field, parse_filter_kwargs

register = template.Library()


# {% create_filter_str args.order args.q args.filter data_dict.field %}"
# %{ create_filter_str args.order args.q args.filter data_dict.field value %}
@register.simple_tag
def create_filter_str(field, args_dict, value=''):
    filter_dict = args_dict['filter']
    order = args_dict['order']
    q = args_dict['q']

    d = copy.copy(filter_dict)
    remove_previous_field(d, field)
    d[field] = value

    order_str = 'order=%s' % order
    q_str = 'q=%s' % q
    filter_str = parse_filter_kwargs(d)
    return '?' + '&'.join([order_str, q_str, filter_str])


# @register.simple_tag
# def create_filter_str(order, q, filter_dict, field, value=''):
#     d = copy.copy(filter_dict)
#     remove_previous_field(d, field)
#     d[field] = value
#
#     order_str = 'order=%s' % order
#     q_str = 'q=%s' % q
#     filter_str = parse_filter_kwargs(d)
#     return '?' + '&'.join([order_str, q_str, filter_str])


@register.filter
def get_value(d, field):
    return d.get(field, '')


@register.simple_tag
def get_value(d, field):
    return d.get(field, '')


@register.filter
def to_string(s):
    return str(s)
