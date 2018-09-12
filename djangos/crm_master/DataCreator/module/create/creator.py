from DataCreator.module.create.data import DataProducter
from DataCreator.module.exception.ForeignModelNullException import ForeignModelNullException
from django.db.models import Model


# def __init__(self, model_class_list):
#     self.model_class_list = model_class_list
#
# def create(self, time=1):
#     if not len(self.model_class_list):
#         return
#     model_class = self.model_class_list.pop(0)
#     data_producter = DataProducter(model_class)
#     for i in range(time):
#         d = {}
#         try:
#             data_producter.create_model_data(d)
#         except ForeignModelNullException as e:
#             self.model_class_list.insert(0, model_class)
#             self.model_class_list.insert(0, e.related_model)
#             self.create(time=time)
#         # obj = model_class.objects.create(*d)
#         if d:
#             print(model_class, '@@@@', d)
#             # print('创建模型对象成功%s' % obj)

class Creator(object):
    # 按照DataProducer提供的参数创建对象
    # 处理抛出来的异常
    # 异常处理流程
    def __init__(self, model_class):
        self.model_class = model_class
        self.data_producter = DataProducter(model_class)

    def create(self, time=1):
        for i in range(time):
            d = {}
            self.data_producter.create_model_data(d)
            print(d)
            obj = self.model_class.objects.create(**d)
            self.data_producter.create_manytomany_field(model_obj=obj)
            print('创建数据成功%s' % obj)


if __name__ == '__main__':
    from DataCreator.libs.env import init

    init('crm_master')
    from repository.models import *

    # from django.contrib.auth.models import User

    creator = Creator(ScoreInfo)
    creator.create(100)
