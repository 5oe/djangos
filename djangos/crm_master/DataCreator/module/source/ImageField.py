from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one


def create_new_image():
    file_field_list = get_setting('IMAGE_FIELD_LIST')
    return get_lucky_one(file_field_list)


if __name__ == '__main__':
    for i in range(10):
        print(create_new_image())
