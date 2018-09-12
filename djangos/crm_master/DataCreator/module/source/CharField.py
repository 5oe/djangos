import random

from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one, is_hit_pr


def create_new_char(max_length):
    last_index = len(source_setting.CHAR_FIELD_WORD) - max_length
    index = random.randint(0, last_index)
    return source_setting.CHAR_FIELD_WORD[index:index + max_length]


def create_old_char(max_length):
    default = get_setting('CHAR_FIELD_DEFAULT')
    if default:
        return default

    # 检查概率设置
    pr = get_setting('CHAR_FIELD_PR')
    char_field_list = get_setting('CHAR_FIELD_LIST')
    if pr and is_hit_pr(pr):
        ret = get_lucky_one(char_field_list)
        if max_length >= len(ret):
            return ret


if __name__ == '__main__':
    for i in range(10):
        print(create_new_char(5))
