import collections
from myAdmin.acquirer.modelAdmin import ModelAdmin


class ModelDelViewModel(object):
    def __init__(self, admin, model_obj):
        self.model_obj = model_obj
        self.display_html = ''
        self.admin = admin
        self.num_config = collections.OrderedDict()
        self._init_config()

    def _init_config(self):
        """
        初始化配置信息:加入删除对象的配置信息
        :return: 
        """
        del_cls = self.model_obj._meta.db_table
        del_cls_verbose = self.model_obj._meta.verbose_name_plural
        self.num_config[del_cls] = {'cls_verbose_name': del_cls_verbose, 'count': 1}

        self.process_num_config(self.model_obj)
        self.display_html = self.process_display_html(self.model_obj)

    def process_num_config(self, model_obj):
        """
         {'UserInfo':{'cls_verbose_name':'用户表','count':1},}
        :param model_obj: 
        :return: 
        """
        for rel_obj in model_obj._meta.related_objects:
            related_args = '%s_set' % rel_obj.name
            related_objs = getattr(model_obj, related_args).all()
            if len(related_objs) == 0:
                continue
            self.num_config.setdefault(rel_obj.name, {})
            config = self.num_config[rel_obj.name]
            config['cls_verbose_name'] = rel_obj.related_model._meta.verbose_name_plural
            config['count'] = len(related_objs)

            for n_obj in related_objs:
                self.process_num_config(n_obj)

    # def process_obj_config(self, model_obj):
    #     """
    #
    #     :param model_obj:
    #     :return:
    #      {'obj':obj,'cls':'UserInfo','child':[{'obj':obj,'cls':'UserInfo','child':[{},{}]},{}]}
    #     """
    #     ret = {}
    #     for rel_obj in model_obj._meta.related_objects:
    #         related_args = '%s_set' % rel_obj.name
    #         related_objs = getattr(model_obj, related_args).all()
    #         if len(related_objs) == 0:
    #             continue
    #
    #         ret.setdefault('child', [])
    #         ret['obj'] = model_obj
    #         ret['cls'] = model_obj._meta.verbose_name
    #         for n_obj in related_objs:
    #             r = self.process_obj_config(n_obj)
    #             if r:
    #                 ret['child'].append(r)
    #     return ret


    def process_display_html(self, obj):
        """
        显示要被删除对象的所有关联对象
        :param obj:
        :return:
                ele += "<li><a href='/kingadmin/%s/%s/%s[表情]ange/'>%s</a><[表情]>" %(obj._meta.app_label,
                                                                         obj._meta.model_name,
                                                                         obj.id,obj)

        """
        ele = "<ul>"

        for reversed_fk_obj in obj._meta.related_objects:

            related_table_name = reversed_fk_obj.name
            related_lookup_key = "%s_set" % related_table_name
            related_objs = getattr(obj, related_lookup_key).all()  # 反向查所有关联的数据
            ele += "<li>%s<ul> " % related_table_name

            if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
                for n_obj in related_objs:
                    ele += "<li><a href='/myAdmin/%s/%s/change/%s'>%s</a>   &nbsp; 记录里与[%s]有关的都会被删除</li>" \
                           % (n_obj._meta.app_label, n_obj._meta.db_table, n_obj.id, n_obj, obj)
            else:
                for n_obj in related_objs:
                    ele += "<li><a href='/myAdmin/%s/%s/change/%s'>%s</a></li>" % (n_obj._meta.app_label,
                                                                                   n_obj._meta.db_table,
                                                                                   n_obj.id, n_obj)
                    ele += self.process_display_html(n_obj)

            ele += "</ul></li>"
        ele += "</ul>"
        return ele

    def get_context(self, **kwargs):
        context = {
            'num_config': self.num_config,
            'display_html': self.display_html,
        }
        context.update(self.admin.cls_detail)
        context.update(kwargs)
        return context


class ModelDelCollectionViewModel(object):
    def __init__(self, admin: ModelAdmin, obj_list):
        self.admin = admin
        self.obj_list = obj_list
        self.display_html = ''
        self.num_config = collections.OrderedDict()
        self.view_model_list = []
        self._init_config()

    def _init_config(self):
        for obj in self.obj_list:
            self.view_model_list.append(ModelDelViewModel(self.admin, obj))

        for view_model in self.view_model_list:
            # {'UserInfo': {'cls_verbose_name': '用户表', 'count': 1}, }
            for k, v in view_model.num_config.items():
                if k in self.num_config:
                    self.num_config[k]['count'] += v['count']
                else:
                    self.num_config[k] = v

            self.display_html += view_model.display_html

    def get_context(self, **kwargs):
        context = {
            'num_config': self.num_config,
            'display_html': self.display_html,
        }
        context.update(self.admin.cls_detail)
        context.update(kwargs)
        return context
