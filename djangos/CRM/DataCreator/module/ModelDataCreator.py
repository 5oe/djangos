from DataCreator.libs.format import format_variable
from DataCreator.libs.setting import get_setting
from DataCreator.libs.random import get_lucky_one
from django.db.models.fields import NOT_PROVIDED


# 传入model对象,根据其不同的字段生成单一字段的随机测试数据
class ModelDataCreator(object):
    """
    Char_fields = ['CharField']
    Number_fields = ['IntegerField', 'FloatField']
    Date_fields = [' DateField', 'DateTimeField']
    Text_field = 'TextField'
    Email_field = 'EmailField'
    Boolean_field = 'BooleanField'
    File_field = [' ImageField', ' FileField']
    """

    def __init__(self, model_class):
        self.model_class = model_class
        self.args_setting = {}  # {'title': {'max_length': 20}}

    def init_args_setting(self):
        fields = self.model_class._meta.fields
        for field in fields:
            column = field.column
            self.args_setting[column] = {}
            max_length = getattr(field, 'max_length')
            if max_length:
                self.args_setting[column]['max_length'] = max_length

    def create_model_data(self, d):
        # d为容器，字典类型，{'price':12000,'title':'调度'}
        fields = self.model_class._meta.fields
        for field in fields:
            column = field.column

            self.args_setting[column] = {}
            max_length = getattr(field, 'max_length')
            if max_length:
                self.args_setting[column]['max_length'] = max_length

            default = getattr(field, 'default')
            if default == NOT_PROVIDED:
                return

            auto_now_add = getattr(field, 'auto_now_add')
            if auto_now_add:
                return

            auto_now = getattr(field, 'auto_now')
            if auto_now:
                return

            field_name = field.get_internal_type()
            func_name = format_variable(field_name=field_name)
            try:
                func = getattr(self, func_name)
            except:
                raise Exception('不支持%s字段的数据生成' % field_name)
            # {'id':1,'price':1221}
            d[column] = func(column)

    def create_char_field(self, column):
        if 'name' in column:
            from DataCreator.module.data_source.name \
                import create_new_name, create_old_name
            name = create_old_name()
            return name if name else create_new_name()
        else:
            max_length = self.args_setting[column]
            from DataCreator.module.data_source.CharField \
                import create_new_char, create_old_char
            char_field_data = create_old_char()
            return char_field_data if char_field_data else create_new_char(max_length)

    def create_integer_field(self):
        from DataCreator.module.data_source.IntegerField \
            import create_new_int, create_old_int
        integer_field_data = create_old_int()
        return integer_field_data if integer_field_data else create_new_int()

    def create_float_field(self):
        from DataCreator.module.data_source.FloatField \
            import create_new_float, create_old_float
        float_field_data = create_old_float()
        return float_field_data if float_field_data else create_new_float()

    def create_text_field(self):
        from DataCreator.module.data_source.TextField import create_new_text
        return create_new_text()

    def create_boolean_field(self):
        return get_lucky_one((0, 1))

    def create_date_field(self):
        # field.auto_now_add
        # field.auto_now
        pass

    def create_datetime_field(self):
        # field.auto_now_add
        # field.auto_now
        pass

    def create_email_field(self):
        from DataCreator.module.data_source.EmailField \
            import create_new_email, create_old_email
        email_field_data = create_old_email()
        return email_field_data if email_field_data else create_new_email()

    def create_file_field(self):
        # 文件不支持随机
        pass

    def create_image_field(self):
        # 文件不支持随机
        pass

    def create_forign_key(self):
        pass

        # 这个需要重新判断格式 format
        # field.related_model

        # CustomerInfo._meta.many_to_many
        #  ( < django.db.models.fields.related.ManyToManyField: consult_courses >)


        # In[176]: UserInfo._meta.related_objects
        # Out[176]:
        # ( < ManyToOneRel: responsitory.customerinfo >,
        # < ManyToOneRel: responsitory.customerfollowupinfo >,
        # < ManyToOneRel: responsitory.answerinfo >,
        # < ManyToManyRel: responsitory.clsinfo >,
        # < ManyToOneRel: responsitory.lectureinfo >)
