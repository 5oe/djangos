import random
import string

from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one,is_hit_pr


def create_new_email():
    max_length = 9
    word_length = random.randint(0, max_length)
    number_length = max_length - word_length
    word = ''.join(random.sample(string.ascii_letters, word_length))
    num = ''.join(random.sample(string.digits, number_length))
    postfix = random.choice(source_setting.EMAIL_POSTFIX)
    return word + num + postfix


def create_old_email():
    default = get_setting('EMAIL_FIELD_DEFAULT')
    if default:
        return default

    # 检查概率设置
    pr = get_setting('EMAIL_FIELD_PR')
    char_field_list = get_setting('EMAIL_FIELD_LIST')
    if pr and is_hit_pr(pr):
        return get_lucky_one(char_field_list)


if __name__ == '__main__':
    for i in range(10):
        a = create_old_email()
        print(a)
