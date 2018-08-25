import random

from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one,is_hit_pr


def create_new_name():
    family_name = random.choice(source_setting.FAMILY_NAME_LIST)
    name = ''.join(random.sample(source_setting.NAME_WORD, 2))
    full_name = family_name + name
    return full_name


def create_old_name():
    # 小分支，用户名类生成
    # 检查是否有默认值
    default = get_setting('NAME_DEFAULT')
    if default:
        return default

    # 检查概率设置
    pr = get_setting('NAME_PR')
    name_list = get_setting('NAME_LIST')
    if pr and is_hit_pr(pr):
        return get_lucky_one(name_list)


if __name__ == '__main__':
    for i in range(10):
        print(create_new_name())

