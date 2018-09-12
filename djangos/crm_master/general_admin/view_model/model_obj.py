from general_admin.acquirer.modelAdmin import ModelAdmin


class ModelObjViewModel(object):
    def __init__(self, admin: ModelAdmin, model_obj=None):
        self.admin = admin
        self.data_container = []
        self.model_obj = model_obj

    def process_readonly_fields(self):
        """
        ['price','status']
        
        -------------------
        
        [{'field':'price','label':'价格','data':'1200},
        {'field':'status','label':'状态','data':1,'display':'未选中'}]
        :return: 
        """
        li = []
        readonly_fields = self.admin.readonly_fields
        for field in readonly_fields:
            config = dict()
            config['field'] = field
            config['label'] = self.admin.get_field_verbose_name(field)
            config['data'] = getattr(self.model_obj, field)
            config['display'] = self.process_readonly_field_display(field)
            li.append(config)
        return li

    def process_readonly_field_display(self, field):
        """
        :param field: 'status' 
        :return: '未选中'
        """
        choices = self.admin.get_field_choices(field)
        # related_model = self.admin.get_field_related_model(field)
        data = getattr(self.model_obj, field)
        display = data
        if choices:
            # 带choices参数字段
            choices_dict = self.admin.get_choices_dict(choices)
            display = choices_dict[data]
        # elif related_model:
        #     # 外键字段
        #     if data:
        #         print(data, type(data))
        #         display = related_model.objects.get(id=int(data))
        return display

    def process_filter_horizontal(self):
        """
        filter_horizontal =['teacher']
        返回处理数据字典
        :return: 
        {
        'teacher':{'checked':[obj1,obj2],'unchecked':[obj3,obj4]},
        }
        
        注意:checked和unchecked对象总数加起来为模型总数
        
        
        field_obj=model_obj._meta.get_field('teachers')
        Out[230]: <django.db.models.fields.related.ManyToManyField: teachers>
        
        field_obj.rel.to
        Out[238]: responsitory.models.UserInfo
        
        
        所有对象：model_obj.teachers.all()
        """
        from django.db.models.fields.related import ManyToManyField
        ret = dict()
        filter_horizontal = self.admin.filter_horizontal
        for field in filter_horizontal:
            # 判断 filter_horizontal是不是manytomany字段,如果不是抛出异常
            field_obj = self.admin.cls_info._meta.get_field(field)
            if not isinstance(field_obj, ManyToManyField):
                raise Exception('%s不是manytomany字段' % field)

            related_model = field_obj.rel.to
            total = list(related_model.objects.all())
            ret[field] = {}
            ret[field]['checked'] = []
            ret[field]['unchecked'] = total
            # 根据对象是否为空,区分对待
            if self.model_obj:
                # 获得对象已经关联的外键对象
                checked = list(getattr(self.model_obj, field).all())
                ret[field]['checked'] = checked
                # 获得未关联的
                unchecked = list(set(total) - set(checked))
                unchecked.sort(key=lambda obj: obj.id)
                ret[field]['unchecked'] = unchecked
        return ret

    def get_context(self, **kwargs):
        context = {}
        if self.model_obj:
            context['readonly_config_list'] = self.process_readonly_fields()
        context['filter_horizontal_config'] = self.process_filter_horizontal()
        context['filter_horizontal'] = self.admin.filter_horizontal
        context.update(self.admin.cls_detail)
        context.update(kwargs)
        return context
