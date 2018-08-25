import random
from DataCreator.module.exception.ForeignModelNullException import ForeignModelNullException
from DataCreator.libs.setting import get_setting


def create_foreign_key(related_model, column):
    # column : consultant_id
    # 查找出所有已存在的model的id,随机选择一个id
    l = related_model.objects.all().values_list('id')
    # required_num = get_setting('FOREIGN_OBJ_REQUIRED_NUMBER')
    # ingore_required_list = get_setting('CAN_IGNORE_REQUIRED_MODEL')
    id_list = list(l)
    if not len(id_list):
        raise ForeignModelNullException(related_model, column)
    # if len(id_list) < required_num:
    #     if related_model._meta.label not in ingore_required_list:
    #         raise ForeignModelNullException(related_model, column)
    foreign_id = random.choice(id_list)[0]
    return foreign_id
