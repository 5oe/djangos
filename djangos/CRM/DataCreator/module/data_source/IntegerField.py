import random

from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one, is_hit_pr


def create_new_int():
    int_range = source_setting.INTEGER_RANGE
    return random.randint(*int_range)


def create_old_int():
    default = get_setting('INTEGER_FIELD_DEFAULT')
    if default:
        return default

    # 检查概率设置
    pr = get_setting('INTEGER_FIELD_PR')
    integer_field_list = get_setting('INTEGER_FIELD_LIST')
    if pr and is_hit_pr(pr):
        return get_lucky_one(integer_field_list)
