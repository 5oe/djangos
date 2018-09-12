from django import template
from django.utils.safestring import mark_safe
import copy
from general_admin.templatetags.lib import remove_previous_field, parse_filter_kwargs

register = template.Library()


@register.filter
def get_user_menu(user):
    """
    :param user: 
    :return: 返回用户的不同角色组成的菜单集合，要做去重 
    """
    s = set()
    if user.is_anonymous():
        return s

    for role in user.role.select_related():
        for menu in role.menu.select_related():
            s.add(menu)
    return s


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
