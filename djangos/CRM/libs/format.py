from myAdmin.acquirer.lib import get_cls_detail

def pack_base_info(request, app_name, cls_name):
    from myAdmin import site
    d = {}
    cls_info = site.get_cls_info(app_name, cls_name)
    cls_detail = get_cls_detail(cls_info)
    d['app_name'] = app_name
    d['cls_name'] = cls_name
    d['title'] = cls_name
    d.update(cls_detail)

    d['args'] = get_cls_index_dict(request)
    return d


def get_cls_index_dict(request):
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
