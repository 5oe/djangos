import operator

from django.db.models import Count
from functools import reduce
from django.db.models.query import Q
from myAdmin.acquirer.lib import add_id_field
from myAdmin.acquirer.lib import clean_filter_dict


class ModelAdmin(object):
    # 职责:根据配置信息获取数据
    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []

    def __init__(self):
        self.show_fields = []  # verbose
        # self.data_list = []  # [{},]
        self.query_set = None
        self.default_handle_flag = True

    @property
    def cls_info(self):
        cls_info = getattr(self, 'ClsInfo')
        return cls_info

    def handle_setting(self, request):
        kwargs = self.get_kwargs(request)
        order_str = kwargs.get('order', '')
        q = kwargs.get('q', '')
        filter = kwargs.get('filter', {})

        filter_dict = clean_filter_dict(filter)
        order_list = self.orders_to_fields(order_str)
        search_q = self._create_search_q(q)

        list_display = self.list_display
        if not list_display:
            self.default_required_handle(filter_dict, order_list, search_q)
        else:
            self.appointed_required_handle(list_display, filter_dict, order_list, search_q)

    @property
    def obj_total_num(self):
        return self.cls_info.objects.all().count()

    def default_required_handle(self, filter_dict, order_list, search_q):
        self.show_fields = [self.cls_info.__name__, ]
        self.query_set = self.cls_info.objects.filter(search_q, **filter_dict).order_by(*order_list)
        self.default_handle_flag = True

    def appointed_required_handle(self, list_display, filter_dict, order_list, search_q):
        self.show_fields = [self.get_field_verbose_name(field) for field in list_display]
        self.query_set = self.cls_info.objects.filter(search_q, **filter_dict).order_by(*order_list)
        self.default_handle_flag = False

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
        l = []
        for field in search_fields:
            field_obj = self.cls_info._meta.get_field(field)
            if field_obj.related_model:
                arg = field
            else:
                arg = field + '__contains'
            l.append(arg)
        return l

    def _create_search_q(self, q):
        if not q:
            return Q()

        l = []
        for k in self.search_args:
            q_obj = Q(**{k: q})
            l.append(q_obj)

        ret = reduce(operator.or_, l)
        return ret

    #
    # @property
    # def list_filter(self):
    #     s = self.get_setting('list_filter')
    #     return s[:] if s else []
    #
    # @property
    # def search_fields(self):
    #     s = self.get_setting('search_fields')
    #     return s[:] if s else []
    #
    # @property
    # def list_display(self):
    #     s = self.get_setting('list_display')
    #     return s[:] if s else []

    @property
    def real_list_display(self):
        if self.list_display:
            list_display = self.list_display[:]
        else:
            list_display = []
        return add_id_field(list_display)

    # @classmethod
    # def get_setting(cls, attr_name):
    #     if not hasattr(cls, attr_name):
    #         return None
    #     else:
    #         return getattr(cls, attr_name)

    @property
    def cls_detail(self):
        cls_info = self.cls_info
        detail = {
            'cls': cls_info,
            'cls_real_name': cls_info.__name__,
            'cls_verbose_name': cls_info._meta.verbose_name_plural,
        }
        return detail

    def get_display_choice_fields(self):
        # 从list_display判断出是带有choices参数的字段,并返回
        l = []
        list_display = self.list_display
        cls_info = self.cls_info
        for field_name in list_display:
            field_obj = cls_info._meta.get_field(field_name)
            if field_obj.choices:
                l.append(field_name)
        return l

    @property
    def list_filter_config(self):
        """
        :return:
         [{'price':<QuerySet [{'price': 145}, {'price': 7}]>,
         'title':<QuerySet [{'title': '行动的习惯'}, {'title': '它。积极行'}]>]
        """
        li = []
        if not self.list_filter:
            return li
        for field in self.list_filter:
            query_set = self.cls_info.objects.values(field).annotate(count=Count(field))
            li.append({field: query_set})
        return li

    # @property
    # def list_filter_config(self):
    #     """
    #      [
    #         {'field_verbose_name':'价格','field':'price',data_list':[2000,11,11]},
    #     ]
    #     """
    #     list_filter = self.list_filter
    #     if not list_filter:
    #         return []
    #     ret = []
    #     for field in list_filter:
    #         single_data = {}
    #         value_list = []
    #         query_set = self.cls_info.objects.values(field).annotate(count=Count(field))
    #         field_obj = self.cls_info._meta.get_field(field)
    #         # 处理choices参数
    #         choices = field_obj.choices
    #         value_list.append(get_filter_info_list(query_set, field_obj, choices=choices))
    #         single_data['field'] = field
    #         single_data['field_verbose_name'] = get_field_verbose_name(self.cls_info, field)
    #         single_data['data_list'] = value_list  # {'value':1,'display':'未选中'}
    #         ret.append(single_data)
    #     return ret

    def get_readonly_info_list(self, obj):
        pass

    def get_field_verbose_name(self, field):
        return self.cls_info._meta.get_field(field).verbose_name

    def get_field_choices(self, field):
        field_obj = self.cls_info._meta.get_field(field)
        choices = field_obj.choices
        return choices

    def get_field_related_model(self, field):
        field_obj = self.cls_info._meta.get_field(field)
        related_model = field_obj.related_model
        return related_model

    @staticmethod
    def get_choices_dict(choices):
        # choices: [(0, '未报名'), (1, '已报名'), (2, '已退学')]
        # 返回{0:'未报名',1: '已报名',2:'已退学'}
        d = {}
        for row in choices:
            d[row[0]] = row[1]
        return d

    @staticmethod
    def get_kwargs(request):
        kwarg = dict(request.GET)
        # {'o': ['1'], 'q': ['fdfddsaf'], 'title': ['111'], 'price': ['232121']}
        ret = {}
        filter_args = {}
        my_set = ('order', 'q')

        ret['order'] = request.GET.get('order', '')
        ret['q'] = request.GET.get('q', '')
        for k in kwarg:
            if k not in my_set:
                filter_args[k] = request.GET.get(k, '')
        ret['filter'] = filter_args
        # {'order': '1', 'q': 'fdfddsaf', 'filter_args': {'title': '111', 'price': '232121'}}
        return ret
