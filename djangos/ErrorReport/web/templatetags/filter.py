from django import template
from responsitory.models import *

register = template.Library()


@register.filter
def like_count(article):
    return EvaluateInfo.objects.filter(action=1, article=article).count()


@register.filter
def unlike_count(article):
    return EvaluateInfo.objects.filter(action=-1, article=article).count()
