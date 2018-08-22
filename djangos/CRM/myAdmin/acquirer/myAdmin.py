from django.db import models
from django.conf import settings
from django.db.models import Count
import importlib
from myAdmin.acquirer.modelAdmin import ModelAdmin
from .lib import add_id_field


# 职责：获得所有注册的类，放在一个列表里
class Site(object):
    def __init__(self):
        self.app_to_cls = {}
        self.app_to_detail = {}

    def init_container(self, app_name):
        self.app_to_cls.setdefault(app_name, [])
        self.app_to_detail.setdefault(app_name, [])

    def register(self, cls_info, model_admin=ModelAdmin):
        app_name = cls_info._meta.app_label
        self.init_container(app_name)
        if not issubclass(cls_info, models.Model):
            raise TypeError('not a subclass to models.Model')
        tmp = {
            'cls': cls_info,
            'cls_real_name': cls_info.__name__,
            'cls_name': cls_info._meta.verbose_name_plural,
            'ModelAdmin': model_admin,
        }
        self.app_to_cls[app_name].append(cls_info)
        self.app_to_detail[app_name].append(tmp)

    def parse_to_str(self):
        # ret = {}
        # for k, v in self.app_to_cls.items():
        #     ret[k] = []
        #     for cls in v:
        #         tmp = {'cls': cls.__name__, 'cls_name': cls._meta.verbose_name_plural}
        #         ret[k].append(tmp)
        # return ret
        return self.app_to_detail

    def get_verbose_name(self, app_name, cls_name):
        cls_detail = self.find_cls_detail(app_name, cls_name)
        if not cls_detail:
            return
        return cls_detail['cls_name']

    def analyze_model_admin(self, app, cls_name):
        # 返回一个字典,针对于某个类
        cls_detail = self.find_cls_detail(app, cls_name)
        cls_info = cls_detail['cls']
        model_admin = cls_detail['ModelAdmin']

        d = dict()
        d['list_display'] = self.analyze_list_display(cls_info, model_admin)
        d['list_filter'] = self.analyze_list_filter(cls_info, model_admin)
        return d

    def analyze_list_display(self, cls_info, model_admin):
        """
        {
            'fields':[{'field':'id','field_name':'编号'},{'field':'title,'field_name':'标题'}],
            'data_list':<QuerySet [{'user': 12, 'id': 2, 'img': 'head/record_ZIWjrXD.png'},
             {'user': 8, 'id': 3, 'img': ''} ],
             'data_count':27,
        }
        :param cls_info: 
        :param model_admin: 
        :return: 
        """
        list_display = model_admin.list_display
        if not list_display:
            return self.default_display_list(cls_info)
        res = {
            'fields': [],
            'data_list': []
        }

        for field in list_display:
            tmp = {}
            field_name = cls_info._meta.get_field(field).verbose_name
            tmp['field'] = field
            tmp['field_name'] = field_name
            res['fields'].append(tmp)
        res['data_list'] = cls_info.objects.values_list(*(add_id_field(list_display)))
        res['data_count'] = len(res['data_list'])

        return {'info': res}

    @staticmethod
    def default_display_list(cls_info):
        datas = cls_info.objects.all()
        data_list = [[single.id, single, ] for single in datas]
        tmp = {
            'fields': [{'field': cls_info.__name__, 'field_name': cls_info.__name__}],
            'data_list': data_list,
            'data_count': len(datas),
        }
        return {'info': tmp}

    @staticmethod
    def analyze_list_filter(cls_info, model_admin):
        """
         {
            'price':{'field_name':'价格','data_list':<QuerySet [{'price': 12000, 'c': 2}, {'price': 4999, 'c': 1}]>},
            'title':{'field_name':'标题','data_list':<QuerySet [{'title': '好爱好散', 'c': 1}, {'title': '天后', 'c': 1}]>},
        }
        :param cls_info: 
        :param model_admin: 
        :return: 
        """
        list_filter = model_admin.list_filter
        if not list_filter:
            return {'status': False}
        res = {}
        for field in list_filter:
            res[field] = {}
            field_name = cls_info._meta.get_field(field).verbose_name
            res[field]['field_name'] = field_name
            res[field]['data_list'] = cls_info.objects.values(field).annotate(count=Count(field)).values(field)
        return {'status': True, 'info': res}

    @staticmethod
    def import_admin():
        for app in settings.INSTALLED_APPS:
            if not app.startswith('django.contrib.'):
                try:
                    importlib.import_module(app + '.myadmin')
                except Exception as e:
                    print(e)

    def find_cls_detail(self, app, cls_name):
        cls_detail_list = self.app_to_detail.get(app, [])
        for cls_detail in cls_detail_list:
            if cls_detail['cls'].__name__ == cls_name:
                return cls_detail

    def get_cls_model_admin(self, app, cls_name):
        cls_detail = self.find_cls_detail(app, cls_name)
        if not cls_detail:
            return None
        return cls_detail['ModelAdmin']

    def is_cls_in_register(self, app, cls_name):
        cls_list = self.app_to_cls.get(app, [])
        for cls in cls_list:
            if cls.__name__ == cls_name:
                return True
        return False

    def is_app_in_register(self, app):
        return True if app in self.app_to_cls else False
