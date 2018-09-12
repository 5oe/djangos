from django.core.urlresolvers import resolve
from django.shortcuts import redirect, HttpResponse
from django.conf import settings
from .items import permission_items


# 权限系统就是将url转化成一个字符串（key)来检测

class PermissionItemParser(object):
    def __init__(self, item):
        self.item = item
        self.url_name = None
        self.method = None
        self.args = None
        self.kwargs = None
        self.hook_func = None
        self.parse()

    def parse(self):
        self.url_name = self.item[0]
        self.method = self.item[1]
        self.args = self.item[2]
        self.kwargs = self.item[3]
        self.hook_func = self.item[4] if len(self.item) > 4 else None

    def is_equal_args(self, args):
        """
        判断参数args 和 self.args 的元素是否相等
        要求，顺序相等，值相等
        :param args: 
        :return: 
        """

        l1 = list(args)
        l2 = list(self.args)
        if len(l1) != len(l2):
            return False

        iter1 = iter(l1)
        iter2 = iter(l2)
        while True:
            try:
                v1 = next(iter1)
                v2 = next(iter2)
                if v1 != v2:
                    return False
            except StopIteration:
                break
        return True

    def is_equal_kwargs(self, kwargs):
        """
        
        由于判断参数kwargs 是否为 self.kwargs的子集会出现 { 
        :param kwargs: 
        :return: 
        """

        kwargs = dict(kwargs)
        for k, v in kwargs.items():
            if self.kwargs.get(k, '') != v:
                return False
        return True

    @staticmethod
    def clear_null_value(GET):
        ret = {}
        for k in GET:
            v = GET.get(k, '')
            if v != '':
                ret[k] = v
        return ret


def get_match_permission(*args, **kwargs):
    request = args[0]
    # 解析成url结构体
    resolve_obj = resolve(request.path)
    is_match = False
    match_key = None
    for k, item in permission_items.items():
        parser_obj = PermissionItemParser(item)
        # 检测url部分是否匹配
        # 检测请求方法是否匹配
        # print(parser_obj.url_name == resolve_obj.url_name, parser_obj.url_name, resolve_obj.url_name)
        # print(parser_obj.method == request.method, parser_obj.method, request.method)
        # print(parser_obj.is_equal_args(url_args), url_args, parser_obj.args)
        # print(parser_obj.is_equal_kwargs(url_kwargs), url_kwargs, parser_obj.kwargs)
        if parser_obj.url_name == resolve_obj.url_name and \
                        parser_obj.method == request.method and \
                parser_obj.is_equal_args(resolve_obj.args) and \
                parser_obj.is_equal_kwargs(resolve_obj.kwargs):

            is_match = True
            # 钩子函数主要排除指定GET参数以外的访问
            if parser_obj.hook_func:
                is_match &= parser_obj.hook_func(request)

            if is_match:
                match_key = k
                print('match_key:', match_key)
                break

    return is_match, match_key


def check_perm(*args, **kwargs):
    request = args[0]
    if request.user.is_admin:
        return True
    is_match, match_key = get_match_permission(*args, **kwargs)
    if is_match:
        # myuser.has_perm('myapp.fix_car')
        # 格式为<app label>.<permission codename>
        app_label, other = match_key.split('.', 1)
        perm_str = '%s.%s' % (app_label, match_key)
        if request.user.has_perm(perm_str):
            # 有权限
            return True
        else:
            return False


# 装饰器函数
def check_permission(func):
    def inner(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL)
        if not check_perm(*args, **kwargs):
            return HttpResponse(status=403)
        else:
            return func(*args, **kwargs)

    return inner
