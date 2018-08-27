from myAdmin.acquirer.modelAdmin import ModelAdmin
from myAdmin.acquirer.lib import get_single_key


class ClsIndexViewModel(object):
    def __init__(self, request, model_admin: ModelAdmin):
        self.model_admin = model_admin
        self.model_admin.handle_setting(request)
        self.query_set = model_admin.query_set
        self.data_container = []
        if self.model_admin.default_handle_flag:
            self.init_default_display()
        else:
            self.init_required_display()

    def init_default_display(self):
        self.data_container = [{'id': {'value': single.id}, 'obj': {'value': single}} \
                               for single in self.query_set]

    def init_required_display(self):
        # add_display_arg(query_set, has_choice_fields, real_list_display, data_container):
        has_choice_fields = self.model_admin.get_display_choice_fields()
        self.process_list_display_config(has_choice_fields)

    @staticmethod
    def get_replace_func_name(field_name):
        func_name = 'get_%s_display' % field_name
        return func_name

    @staticmethod
    def process_single_values(model_obj, real_list_display):
        # 处理结果 {'price':{'value':10000},'status':{'value':1}}
        d = {}
        for field in real_list_display:
            value = getattr(model_obj, field)
            d[field] = {'value': value}
        return d

    def process_list_display_config(self, has_choice_fields):
        # 加工,是将带choices带字段替换为文本
        # single_data初始状态:{'status':1,'sex':女}
        # 处理后 {'status':{'value':1,'display':'未选中'},'sex':{'data':'女'}}
        for obj in self.query_set:
            single_data = self.process_single_values(obj, self.model_admin.real_list_display)
            for field in has_choice_fields:
                func_name = self.get_replace_func_name(field)
                func = getattr(obj, func_name)
                single_data[field]['display'] = func()
            self.data_container.append(single_data)

    def process_list_filter_config(self):
        """
        [{'price':<QuerySet [{'price': 145}, {'price': 7}]>,
         'title':<QuerySet [{'title': '行动的习惯'}, {'title': '它。积极行'}]>]
        
         ----------------
        [
           {'field_verbose_name':'价格','field':'price',
           data_list':[{'value':1,'display':'男'},{'value':2,'display':'女'}]},
       ]
        """
        config_list = self.model_admin.list_filter_config
        li = []
        if not config_list:
            return li

        for config in config_list:
            new_config = {}
            field = get_single_key(config)
            new_config['field'] = field
            new_config['field_verbose_name'] = self.model_admin.get_field_verbose_name(field)
            data_list = config[field]
            new_config['data_list'] = self.process_list_filter_data(field, data_list)
            li.append(new_config)
        return li

    def process_list_filter_data(self, field, data_list):
        """
        :param data_list: <QuerySet [{'price': 145}, {'price': 7}]>, 
        :param field: 'price' 
        :return:{'value':1,'display':'男'}
        """
        choices = self.model_admin.get_field_choices(field)
        related_model = self.model_admin.get_field_related_model(field)
        if choices:
            # 带choices参数字段
            choices_dict = self.model_admin.get_choices_dict(choices)
            return self.process_choices_field_data(field, data_list, choices_dict)
        elif related_model:
            # 外键字段
            return self.process_foreign_field_data(field, data_list, related_model)
        else:
            return self.process_data(field, data_list)

    @staticmethod
    def process_foreign_field_data(field, data_list, model):
        li = []
        for row in data_list:
            data = row[field]
            if data:
                display = model.objects.get(id=data)
                d = {'value': data, 'display': display}
            else:
                d = {'value': data}
            li.append(d)
        return li

    @staticmethod
    def process_choices_field_data(field, data_list, choices_dict):
        li = []
        for row in data_list:
            data = row[field]
            display = choices_dict[data]
            li.append({'value': data, 'display': display})
        return li

    @staticmethod
    def process_data(field, data_list):
        li = []
        for row in data_list:
            data = row[field]
            li.append({'value': data})
        return li

    def get_context(self, request, **kwargs):
        context = {
            'show_fields': self.model_admin.show_fields,
            'data_list': self.data_container,
            'list_filter': self.process_list_filter_config(),
            'search_fields': self.model_admin.search_fields,
            'data_total_num': self.model_admin.obj_total_num,
            'args': self.model_admin.get_kwargs(request)
        }
        context.update(self.model_admin.cls_detail)
        context.update(kwargs)
        return context
