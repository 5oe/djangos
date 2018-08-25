import operator

from django.db.models import Count
from functools import reduce
from django.db.models.query import Q
from myAdmin.acquirer.lib import \
    add_id_field, get_field_verbose_name, format_values_list, get_filter_dict


class ModelAdmin(object):
    # 职责:根据配置信息获取数据

    def __init__(self):
        self.show_fields = []  # verbose
        # self.data_list = []  # [{},]
        self.query_set = None

    @property
    def cls_info(self):
        cls_info = getattr(self, 'ClsInfo')
        return cls_info

    def handle(self, **kwargs):
        order_str = kwargs.get('order', '')
        q = kwargs.get('q', '')
        filter = kwargs.get('filter', {})

        filter_dict = get_filter_dict(filter)
        order_list = self.orders_to_fields(order_str)
        search_q = self.create_search_q(q)

        list_display = self.get_setting('list_display')
        if not list_display:
            return self.default_required_handle(filter_dict, order_list, search_q)
        else:
            return self.appointed_required_handle(list_display, filter_dict, order_list, search_q)

    @property
    def obj_total_num(self):
        return self.cls_info.objects.all().count()

    def default_required_handle(self, filter_dict, order_list, search_q):
        self.show_fields = [self.cls_info.__name__, ]
        self.query_set = self.cls_info.objects.filter(search_q, **filter_dict).order_by(*order_list)

    def appointed_required_handle(self, list_display, filter_dict, order_list, search_q):
        self.show_fields = [get_field_verbose_name(self.cls_info, field) for field in list_display]
        self.query_set = self.cls_info.objects.filter(search_q, **filter_dict).order_by(*order_list)

    def orders_to_fields(self, order):
        list_display = self.real_list_display
        l = []
        for sz in order.split('.'):
            try:
                i = int(sz)
                if i > 0:
                    field = list_display[i]
                else:
                    field = '-' + list_display[abs(i)]
                l.append(field)
            except:
                continue
        return l

    @property
    def search_args(self):
        search_fields = self.search_fields
        if not search_fields:
            return []
        return [field + '__contains' for field in search_fields]

    def create_search_q(self, q):
        if not self.search_args:
            return Q()

        l = []
        for k in self.search_args:
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
        list_filter = self.get_setting('list_filter')

        if not list_filter:
            return None
        else:
            l = []
            for field in list_filter:
                tmp = {}
                value_list = self.cls_info.objects.values(field). \
                    annotate(count=Count(field)).values_list(field)
                tmp['field'] = field
                tmp['field_verbose_name'] = get_field_verbose_name(self.cls_info, field)
                tmp['data_list'] = format_values_list(value_list)
                l.append(tmp)
            return l

    @property
    def search_fields(self):
        s = self.get_setting('search_fields')
        return s if s else None

    @classmethod
    def get_setting(cls, attr_name):
        if not hasattr(cls, attr_name):
            return None
        else:
            return getattr(cls, attr_name)

    @property
    def real_list_display(self):
        if hasattr(self, 'list_display'):
            list_display = getattr(self, 'list_display')
        else:
            list_display = []
        return add_id_field(list_display)
