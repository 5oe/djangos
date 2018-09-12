from django.db.models.fields import NOT_PROVIDED
from DataCreator.libs.format import format_variable
from DataCreator.libs.random import get_lucky_one


# 传入model对象,根据其不同的字段生成单一字段的随机测试数据
class DataProducter(object):
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

    def create_model_data(self, d):
        # d为容器，字典类型，{'price':12000,'title':'调度'}
        fields = self.model_class._meta.fields
        for field in fields:
            column = field.column

            self.args_setting[column] = {}
            max_length = getattr(field, 'max_length')
            if max_length:
                self.args_setting[column].setdefault('max_length', max_length)

            related_model = getattr(field, 'related_model')
            if related_model:
                self.args_setting[column].setdefault('related_model', related_model)

            default = getattr(field, 'default')
            if default != NOT_PROVIDED:
                continue

            choices = getattr(field, 'choices')
            if choices:
                self.args_setting[column].setdefault('choices', choices)

            auto_now_add = hasattr(field, 'auto_now_add')
            if auto_now_add:
                auto_now_add = getattr(field, 'auto_now_add')
                if auto_now_add: continue

            auto_now = hasattr(field, 'auto_now')
            if auto_now:
                auto_now = getattr(field, 'auto_now')
                if auto_now: continue

            auto_created = getattr(field, 'auto_created')
            if auto_created:
                continue

            null = getattr(field, 'null')
            if null:
                continue

            blank = getattr(field, 'blank')
            if blank:
                continue

            unique = getattr(field, 'unique')
            if unique:
                print('注意:这个字段存在unique')
                self.args_setting[column].setdefault('unique', True)

            field_name = field.get_internal_type()
            func_name = format_variable(field_name=field_name)
            print(field_name, func_name)
            try:
                func = getattr(self, func_name)
            except:
                raise Exception('不支持%s字段的数据生成' % field_name)
            # {'id':1,'price':1221}
            d[column] = func(column)

    def create_char_field(self, column):
        max_length = self.args_setting[column]['max_length']
        unique = self.args_setting[column].get('unique')
        if 'identity_id' in column:
            from DataCreator.module.source.identity_id import \
                create_new_id
            return create_new_id()
        elif 'name' in column:
            from DataCreator.module.source.name \
                import create_new_name, create_old_name
            if unique:
                return create_new_name()
            else:
                name = create_old_name()
                return name if name else create_new_name()
        elif 'password' in column:
            from DataCreator.module.source.password \
                import create_new_password, create_old_password
            password = create_old_password()
            return password if password else create_new_password(max_length)
        elif 'email' in column:
            from DataCreator.module.source.EmailField import create_new_email
            if unique:
                return create_new_email()
            else:
                return self.create_email_field(column)
        else:
            from DataCreator.module.source.CharField \
                import create_new_char, create_old_char
            if 'title' in column:
                max_length = 5
            if unique:
                return create_new_char(max_length)
            else:
                char_field_data = create_old_char(max_length)
                return char_field_data if char_field_data else create_new_char(max_length)

    def create_smallinteger_field(self, column):
        return self.create_integer_field(column)

    def create_integer_field(self, column):
        """
        [(100, 'A+'),
             (95, 'A'),
             (90, 'A-'),
             (85, 'B+'),
             (80, 'B'),
             (75, 'B-'),
             (70, 'C+'),
             (65, 'C'),
             (60, 'C-'),
             (0, '不及格')]
        """
        from DataCreator.module.source.IntegerField \
            import create_new_int, create_old_int, create_choice_int
        choices = self.args_setting[column].get('choices')
        if choices:
            return create_choice_int(choices)
        else:
            integer_field_data = create_old_int()
            return integer_field_data if integer_field_data else create_new_int()

    def create_positiveinteger_field(self, column):
        return self.create_integer_field(column)

    def create_float_field(self, column):
        from DataCreator.module.source.FloatField \
            import create_new_float, create_old_float
        float_field_data = create_old_float()
        return float_field_data if float_field_data else create_new_float()

    def create_text_field(self, column):
        from DataCreator.module.source.TextField import create_new_text
        return create_new_text()

    def create_boolean_field(self, column):
        return get_lucky_one((0, 1))

    def create_date_field(self, column):
        from DataCreator.module.source.DateField \
            import create_old_date, create_new_date
        date_field_data = create_old_date()
        return date_field_data if date_field_data else create_new_date()

    def create_datetime_field(self, column):
        from DataCreator.module.source.DateTimeField \
            import create_old_datetime, create_new_datetime
        date_field_data = create_old_datetime()
        return date_field_data if date_field_data else create_new_datetime()

    def create_email_field(self, column):
        from DataCreator.module.source.EmailField \
            import create_new_email, create_old_email
        email_field_data = create_old_email()
        return email_field_data if email_field_data else create_new_email()

    def create_file_field(self, column):
        # 文件不支持随机
        from DataCreator.module.source.FileField import create_new_file
        return create_new_file()

    def create_image_field(self, column):
        # 文件不支持随机
        from DataCreator.module.source.ImageField import create_new_image
        return create_new_image()

    def create_foreign_key(self, column):
        from DataCreator.module.source.ForeignKey import create_foreign_key
        # column : consultant_id
        related_model = self.args_setting[column]['related_model']
        return create_foreign_key(related_model, column)

    def create_manytomany_field(self, model_obj):
        from DataCreator.module.source.ManytoMany import create_manytomany_field
        many_to_many = self.model_class._meta.many_to_many
        if not many_to_many:
            return
        return create_manytomany_field(model_obj, many_to_many)
