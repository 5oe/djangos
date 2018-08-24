# ------
# 配置默认
# 先检查默认,若默认有值,则不去检查概率
NAME_DEFAULT = '赵子懿'
CHAR_FIELD_DEFAULT = 'zhaoziyi'
# EMAIL_FIELD_DEFAULT = '973697101@qq.com'
# -------
# 配置概率重复
NAME_PR = 0.4  # 0-1
NAME_LIST = ['曹操', '司马懿', '郭奉孝', '旬令君', '贾诩']  # 若概率命中，随机在列表中取一个

CHAR_FIELD_PR = 0.2
CHAR_FIELD_LIST = ['freedom', ' django默认的BASE_DIR目录是总项目文件夹下的', ]

EMAIL_FIELD_PR = 0.3
EMAIL_FIELD_LIST = ['973697101@qq.com', '363396239@qq.com', '913719647@qq.com', '2218390337@qq.com']

FILE_FIELD_PR = 1  # 文件配置必须为1
FILE_FIELD_LIST = ['uploads/a.png', 'upload/b.png']

IMAGE_FIELD_PR = 1  # 文件配置必须为1
IMAGE_FIELD_LIST = ['uploads/a.png', 'upload/b.png']

# 其他

# TextField的长度取值范围
TEXT_FIELD_RANGE = (50, 300)
