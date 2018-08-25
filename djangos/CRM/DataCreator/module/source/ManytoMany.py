import random
from DataCreator.module.exception.ForeignModelNullException import ForeignModelNullException
from DataCreator.libs.setting import get_setting


def create_foreign_key(related_model, column):
    # column : consultant_id
    # 查找出所有已存在的model的id,随机选择一个id
    l = related_model.objects.all().values_list('id')
    required_num = get_setting('FOREIGN_OBJ_REQUIRED_NUMBER ')
    ingore_required_list = get_setting('CAN_IGNORE_REQUIRED_MODEL')
    id_list = list(l)
    if len(id_list) < 0:
        raise ForeignModelNullException(related_model, column)
    if len(id_list) < required_num:
        if related_model._meta.label not in ingore_required_list:
            raise ForeignModelNullException(related_model, column)
    foreign_id = random.choice(id_list)[0]
    return foreign_id


def create_manytomany_field(model_obj, many_to_many):
    # 获得manytomany的模型对象,然后查出已存在的id,随机选择一个
    # CustomerInfo._meta.many_to_many
    # ( < django.db.models.fields.related.ManyToManyField: consult_courses >)

    # a=RoleInfo._meta.many_to_many[0]
    # 关联名字 a.attname  # menu
    # a. related_model # 关联模型

    # 数据操作
    # r=RoleInfo.objects.all().last()
    # r.menu.add(6)  # menu是manytomany字段，6是MenuInfo存在的id
    # r.menu.add(3,4) #可以添加多个
    for obj in many_to_many:
        column = obj.attname
        related_model = obj.related_model
        l = related_model.objects.all().values_list('id')
        id_list = list(l)
        # required_num = get_setting('FOREIGN_OBJ_REQUIRED_NUMBER')
        # ingore_required_list = get_setting('CAN_IGNORE_REQUIRED_MODEL')
        if len(id_list) < 0:
            raise ForeignModelNullException(related_model, column)
        # if len(id_list) < required_num:
        #     if related_model._meta.label not in ingore_required_list:
        #         raise ForeignModelNullException(related_model, column)
        id_list = [row[0] for row in id_list]
        foreign_num = random.randint(1, len(id_list))
        foreign_id_list = random.sample(id_list, foreign_num)

        getattr(model_obj, column).add(*foreign_id_list)
