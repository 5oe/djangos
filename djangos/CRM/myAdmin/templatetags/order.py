from django import template
from django.utils.safestring import mark_safe
from .lib import parse_filter_kwargs, get_arg_index, get_arg_value
import copy

register = template.Library()


@register.simple_tag
def make_order_str(index, order_arg, q, kwargs):
    if order_arg == '':
        order_list = []
    else:
        order_list = order_arg.split('.')

    value = get_arg_value(index, order_list)
    if value is not None:
        order_list.remove(value)
        index = -int(value)

    order_list.insert(0, str(index))

    d = copy.deepcopy(kwargs)
    order_str = 'order=' + '.'.join(order_list)
    q_str = 'q=%s' % q
    filter_str = parse_filter_kwargs(d)

    return '?' + '&'.join([order_str, q_str, filter_str])


# simple_tag开始
@register.simple_tag
def invert_order_href(index, order_arg, q, kwargs):
    order_list = order_arg.split('.')
    index = get_arg_index(index, order_list)

    if index is None:
        return ''
    else:
        i = int(order_list[index])
        order_list[index] = str(-i)
        order_str = '.'.join(order_list)
        filter_str = parse_filter_kwargs(kwargs)
        html_href = '''
        <a class =
        "glyphicon glyphicon-sort" 
        aria-hidden="true" 
        href="?order=%s&q=%s&%s" 
        title="颠倒排序"></a>''' % (order_str, q, filter_str)
        return mark_safe(html_href)


@register.simple_tag
def delete_order_href(index, order_arg, q, kwargs):
    order_list = order_arg.split('.')
    value = get_arg_value(index, order_list)

    if value is not None:
        order_list.remove(value)
        order_str = '.'.join(order_list)
        filter_str = parse_filter_kwargs(kwargs)
        html_href = '''
        <a class =
        "glyphicon glyphicon-scissors" 
        aria-hidden="true" 
        href="?order=%s&q=%s&%s" 
        title="删除排序"></a>''' % (order_str, q, filter_str)
        return mark_safe(html_href)
    else:
        return ''


@register.simple_tag
def test(a, b, c, d):
    return '%s@@@@@%s!!!!!%s~~~~~~%s' % (d, c, b, a)

# lib
