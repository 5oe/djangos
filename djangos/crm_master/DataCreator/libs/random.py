import random


def is_hit_pr(pr):
    # 是否命中概率
    if 0 < pr < 1:
        stand = random.random()
        return True if stand < pr else False
    else:
        raise Exception('概率设置不合规范,应该满足0<pr<1')


def get_lucky_one(data_list):
    return random.choice(data_list)
