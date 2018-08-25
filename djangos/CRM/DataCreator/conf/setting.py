import datetime

# 配置默认
# 先检查默认,若默认有值,则不去检查概率
# NAME_DEFAULT = '赵子懿'
# CHAR_FIELD_DEFAULT = 'zhaoziyi'
# EMAIL_FIELD_DEFAULT = '973697101@qq.com'
# DATE_FIELD_DEFAULT = datetime.date(year=1995, month=8, day=29)
# DATETIME_FIELD_DEFAULT = datetime.datetime(2014, 2, 14, 18, 34, 11)
PASSWORD_DEFAULT = 'pbkdf2_sha256$36000$ylwXxEPtmFcQ$nctksrh4PdsX8RdH89iwTLxWJlthHPjIGBXdRDgC0Fc'
# -------
# 配置概率重复
NAME_PR = 0  # 0-1
NAME_LIST = ['曹操', '司马懿', '郭奉孝', '旬令君', '贾诩']  # 若概率命中，随机在列表中取一个

PASSWORD_PR = 0.7
PASSWORD_LIST = ['pbkdf2_sha256$36000$ylwXxEPtmFcQ$nctksrh4PdsX8RdH89iwTLxWJlthHPjIGBXdRDgC0Fc']

CHAR_FIELD_PR = 0.2
CHAR_FIELD_LIST = ['love', ' django', ]  # 切忌太长

EMAIL_FIELD_PR = 0.3
EMAIL_FIELD_LIST = ['973697101@qq.com', '363396239@qq.com', '913719647@qq.com', '2218390337@qq.com']

FILE_FIELD_PR = 1  # 文件配置必须为1
FILE_FIELD_LIST = ['uploads/a.png', 'upload/b.png']

IMAGE_FIELD_PR = 1  # 文件配置必须为1
IMAGE_FIELD_LIST = ['uploads/a.png', 'upload/b.png']

DATE_FIELD_PR = 0.6
DATE_FIELD_LIST = [
    datetime.date(year=2016, month=12, day=17),
    datetime.date(year=2017, month=5, day=11),
    datetime.date(year=2017, month=1, day=13),
    datetime.date(year=2017, month=11, day=11),
    datetime.date(year=2017, month=11, day=29),
    datetime.date(year=2018, month=6, day=29),
    datetime.date(year=2018, month=3, day=17),
    datetime.date(year=2018, month=3, day=1),
]

DATETIME_FIELD_PR = 0.6
DATETIME_FIELD_LIST = [
    datetime.datetime(2016, 2, 14, 18, 34, 11),
    datetime.datetime(2017, 2, 14, 18, 34, 11),
    datetime.datetime(2017, 2, 22, 18, 34, 11),
    datetime.datetime(2017, 6, 1, 1, 34, 11),
    datetime.datetime(2017, 12, 14, 1, 2, 11),
    datetime.datetime(2018, 1, 1, 18, 34, 11),
    datetime.datetime(2018, 3, 17, 18, 34, 11),
]
# 其他

# TextField的长度取值范围
TEXT_FIELD_RANGE = (50, 300)

# 是否指定创建为空的关联对象
AUTO_CREATE_RELATED_MODEL_OBJ = True

# 外键模型对象要求个数
FOREIGN_OBJ_REQUIRED_NUMBER = 100
# 不用满足外键模型对象要求个数的模型名字列表
CAN_IGNORE_REQUIRED_MODEL = ['responsitory.UserInfo', 'responsitory.MenuInfo', 'auth.User']
