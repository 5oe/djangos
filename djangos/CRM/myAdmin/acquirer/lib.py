def add_id_field(field_list):
    l = ['id', ]
    l = l + field_list
    return l


def get_cls_detail(cls_info):
    detail = {
        'cls': cls_info,
        'cls_real_name': cls_info.__name__,
        'cls_verbose_name': cls_info._meta.verbose_name_plural,
    }
    return detail


def get_field_verbose_name(cls_info, field):
    return cls_info._meta.get_field(field).verbose_name


def get_filter_dict(filter_dict):
    ret = {}
    for k, v in filter_dict.items():
        if v:
            ret[k] = v
    return ret


def format_values_list(value_list):
    # 'value_list': < QuerySet[(4,), (2,), (1,), (3,), (5,)] >
    return [row[0] for row in value_list]
