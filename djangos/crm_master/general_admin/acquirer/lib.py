def add_id_field(field_list):
    l = ['id', ]
    l = l + field_list
    return l


def clean_filter_dict(filter_dict):
    # 将filter_dict中value值为空的键值对去掉
    ret = {}
    for k, v in filter_dict.items():
        if v:
            ret[k] = v
    return ret


def get_single_key(d):
    for k in d:
        return k

# def get_filter_info_list(query_set, field_obj, choices=None):
#     # 根据filter列表的一个字段，返回这个字段的所有信息（数据和显示）列表
#     # [{'value':1,'display':'男'},{'value':2,'display':'女'}]
#     field_name = field_obj.column
#     l = []
#     if choices:
#         replace_dict = get_replace_choice_dict(field_obj.choices)
#         for row in query_set:
#             data = row[field_name]
#             display = replace_dict[data]
#             d = {'value': data, 'display': display}
#             l.append(d)
#     else:
#         if field_name.endswith('_id'):
#             field_name = field_name[0:-3]
#             model = field_obj.foreign_related_fields[0].model
#             for row in query_set:
#                 data = row[field_name]
#                 if data:
#                     display = model.objects.get(id=data)
#                     d = {'value': data, 'display': display}
#                 else:
#                     d = {'value': data}
#                 l.append(d)
#         else:
#             for row in query_set:
#                 data = row[field_name]
#                 d = {'value': data}
#                 l.append(d)
#     return l

# ]: ScoreInfo.objects.filter().values('student')
# Out[53]: <QuerySet [{'student': 7}, {'student': 7}, {'student': 8}, {'student': 9}, {'student': 9}, {'student': 10}, {'student': 12}, {'student': 15}, {'student': 16}, {'student': 16}, {'student': 16}, {'student': 19}, {'student': 20}, {'student': 22}, {'student': 24}, {'student': 24}, {'student': 24}, {'student': 26}, {'student': 26}, {'student': 27}, '...(remaining elements truncated)...']>
#
# In [54]: ScoreInfo.objects.filter().values('student_id')
# Out[54]: <QuerySet [{'student_id': 7}, {'student_id': 7}, {'student_id': 8}, {'student_id': 9}, {'student_id': 9}, {'student_id': 10}, {'student_id': 12}, {'student_id': 15}, {'student_id': 16}, {'student_id': 16}, {'student_id': 16}, {'student_id': 19}, {'student_id': 20}, {'student_id': 22}, {'student_id': 24}, {'student_id': 24}, {'student_id': 24}, {'student_id': 26}, {'student_id': 26}, {'student_id': 27}, '...(remaining elements truncated)...']>
#
