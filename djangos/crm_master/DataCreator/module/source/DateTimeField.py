import random
import datetime
from DataCreator.conf import source_setting
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one, is_hit_pr


def create_new_datetime():
    ret = None
    flag = True

    year_range = source_setting.DATETIME_FILED_RANGE['year']
    month_range = source_setting.DATETIME_FILED_RANGE['month']
    day_range = source_setting.DATETIME_FILED_RANGE['day']
    hour_range = source_setting.DATETIME_FILED_RANGE['hour']
    minute_range = source_setting.DATETIME_FILED_RANGE['minute']
    second_range = source_setting.DATETIME_FILED_RANGE['second']

    while flag:
        try:
            year = random.randint(*year_range)
            month = random.randint(*month_range)
            day = random.randint(*day_range)
            hour = random.randint(*hour_range)
            minute = random.randint(*minute_range)
            second = random.randint(*second_range)
            ret = datetime.datetime(year, month, day, hour, minute, second)
            flag = False
        except:
            pass
    return ret


def create_old_datetime():
    default = get_setting('DATETIME_FIELD_DEFAULT')
    if default:
        return default

    # 检查概率设置
    pr = get_setting('DATETIME_FIELD_PR')
    datetime_field_list = get_setting('DATE_FIELD_LIST')
    if pr and is_hit_pr(pr):
        return get_lucky_one(datetime_field_list)


if __name__ == '__main__':
    for i in range(100):
        print(create_new_datetime())
