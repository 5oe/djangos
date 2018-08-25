import random

from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one,is_hit_pr


def create_new_password(max_length):
    password = ''.join(random.sample(source_setting.PASSWORD_WORD, max_length))
    return password


def create_old_password():
    # 小分支，用户名类生成
    # 检查是否有默认值
    default = get_setting('PASSWORD_DEFAULT')
    if default:
        return default

    # 检查概率设置
    pr = get_setting('PASSWORD_PR')
    password_list = get_setting('PASSWORD_LIST')
    if pr and is_hit_pr(pr):
        return get_lucky_one(password_list)


if __name__ == '__main__':
    for i in range(10):
        print(create_old_password())

