from django import template
from django.utils.safestring import mark_safe

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
