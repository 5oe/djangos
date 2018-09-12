import random

from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting


def create_new_text():
    text_length_range = get_setting('TEXT_FIELD_RANGE')
    text_length = random.randint(*text_length_range)
    last_index = len(source_setting.TEXT_FIELD_WORD) - text_length
    index = random.randint(0, last_index)
    return source_setting.TEXT_FIELD_WORD[index:index+text_length + 1]


if __name__ == '__main__':
    for i in range(10):
        print('*'*10)
        print(create_new_text())
