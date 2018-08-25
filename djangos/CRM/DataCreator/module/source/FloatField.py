import random

from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one, is_hit_pr


def create_new_float():
    float_range = source_setting.FLOAT_RANGE
    return random.uniform(*float_range)


def create_old_float():
    default = get_setting('FLOAT_FIELD_DEFAULT')
    if default:
        return default

    # 检查概率设置
    pr = get_setting('FLOAT_FIELD_PR')
    float_field_list = get_setting('FLOAT_FIELD_LIST')
    if pr and is_hit_pr(pr):
        return get_lucky_one(float_field_list)

if __name__ == '__main__':
    for i in range(10):
        print(create_old_float())