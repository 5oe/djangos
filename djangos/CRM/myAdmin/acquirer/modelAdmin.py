import operator

from django.db.models import Count
from functools import reduce

from myAdmin.acquirer.lib import add_id_field, get_field_verbose_name, format_values_list
from django.db.models.query import Q


class ModelAdmin(object):
    # 职责:根据配置信息获取数据
    replace_choice_flag = True

    def __init__(self):
        self.show_fields = []  # verbose
        # self.data_list = []  # [{},]

    def get_data_list(self, **kwargs):
        order_str = kwargs.get('order', '')
        q = kwargs.get('q', '')
        filter = kwargs.get('filter', {})
        filter_dict = self.get_filter_dict(filter)
        order_list = self.orders_to_fields(order_str)
        search_q = self.create_search_dict(q)

        list_display = self.get_setting('list_display')
        if not list_display:
            return self.get_default_data(filter_dict, order_list, search_q)
        else:
            return self.get_appointed_data(list_display, filter_dict, order_list, search_q)

    @staticmethod
    def get_filter_dict(filter_dict):
        ret = {}
        for k, v in filter_dict.items():
            if v:
                ret[k] = v
        return ret

    @property
    def data_total_num(self):
        cls_info = getattr(self, 'ClsInfo')
        return cls_info.objects.all().count()

    def get_default_data(self, filter_dict, order_list, search_q):
        cls_info = getattr(self, 'ClsInfo')
        self.show_fields = [cls_info.__name__, ]

        l = cls_info.objects.filter(search_q, **filter_dict).order_by(*order_list)
        data_list = [(single.id, single) for single in l]

        if self.replace_choice_flag:
            self.replace_choice_display(data_list)
        return data_list

    def get_appointed_data(self, list_display, filter_dict, order_list, search_q):
        cls_info = getattr(self, 'ClsInfo')
        self.show_fields = [get_field_verbose_name(cls_info, field) for field in list_display]

        data_list = cls_info.objects.filter(search_q, **filter_dict).order_by(*order_list). \
            values_list(*(self.get_real_list_display()))

        if self.replace_choice_flag:
            self.replace_choice_display(data_list)
        return data_list

    def replace_choice_display(self, data_list):
        list_display = self.get_real_list_display()
        cls_info = getattr(self, 'ClsInfo')
        for i in range(1, len(list_display)):
            field_name = list_display[i]
            field_obj = cls_info._meta.get_field(field_name)
            if field_obj.choices:
                column_data = getattr(field_obj, 'get_%s_display' % field_name)()
                data_list[i] = column_data

    def orders_to_fields(self, order):
        list_display = self.get_real_list_display()
        l = []
        for sz in order.split('.'):
            try:
                i = int(sz)
                field = list_display[i] if i else '-' + list_display[i]
                l.append(field)
            except:
                continue
        return l

    def get_search_args(self):
        search_fields = self.get_search_fields()
        if not search_fields:
            return []
        return [field + '__contains' for field in search_fields]

    def create_search_dict(self, q):
        l = []
        search_args = self.get_search_args()
        for k in search_args:
            q_obj = Q(**{k: q})
            l.append(q_obj)

        ret = reduce(operator.or_, l)
        return ret

    def analyze_list_filter(self):
        """
         [
            {'field_verbose_name':'价格','field':'price',data_list':[2000,11,11]},
        ]
        """
        cls_info = getattr(self, 'ClsInfo')
        list_filter = self.get_setting('list_filter')

        if not list_filter:
            return None
        else:
            l = []
            for field in list_filter:
                tmp = {}
                value_list = cls_info.objects.values(field). \
                    annotate(count=Count(field)).values_list(field)
                tmp['field'] = field
                tmp['field_verbose_name'] = get_field_verbose_name(cls_info, field)
                tmp['data_list'] = format_values_list(value_list)
                l.append(tmp)
            return l

    def get_search_fields(self):
        s = self.get_setting('search_fields')
        return s if s else None

    @classmethod
    def get_setting(cls, attr_name):
        if not hasattr(cls, attr_name):
            return None
        else:
            return getattr(cls, attr_name)

    def get_real_list_display(self):
        if hasattr(self, 'list_display'):
            list_display = getattr(self, 'list_display')
        else:
            list_display = []
        return add_id_field(list_display)
