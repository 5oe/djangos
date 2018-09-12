from . import hook

# 后面values列表里第一个值如'table_index'是django中的url name，在这里必须相对的url name,
#  而不是绝对url路径，因为考虑到django url正则匹配的问题，搞绝对路径，不好控制。
# values里第2个值是http请求方法
# values里第3个[]是要求这个请求中必须带有某些参数，但不限定对数的值是什么
# values里的第4个{}是要求这个请求中必须带有某些参数，并且限定所带的参数必须等于特定的值

# 说几点，权限定义很辛苦，不存在一个权限包含另外一个权限，权限都是最小单位，'大权限'由多个权限条目组成
"""

"""
permissions = (
    ('repository.index', 'repository.index'),
    ('repository.app_index', 'repository.app_index'),
    ('repository.cls_index', 'repository.cls_index'),
    ('repository.add_model_obj', 'repository.add_model_obj'),
    ('repository.add_model_obj:POST', 'repository.add_model_obj:POST'),
    ('repository.action_model_obj:POST', 'repository.action_model_obj:POST'),
    ('repository.delete_model_obj:POST', 'repository.delete_model_obj:POST'),
    ('repository.delete_collection:POST', 'repository.delete_collection:POST'),
    ('repository.cls_index@UserInfo', 'repository.cls_index@UserInfo'),
    ('repository.cls_index@CustomerInfo', 'repository.cls_index@CustomerInfo'),
)

permission_items = {
    'repository.index': ['index', 'GET', [], {}],
    'repository.app_index': ['app_index', 'GET', [], {}],  # 错误,没有定义kwargs的参数
    'repository.cls_index': ['cls_index', 'GET', [], {}],  # 错误,没有定义kwargs的参数
    'repository.cls_index@UserInfo': ['cls_index', 'GET', [], {'app': 'repository', 'cls': 'UserInfo'}],
    # 单一权限：只能访问UserInfo
    'repository.cls_index@CustomerInfo': ['cls_index', 'GET', [], {'app': 'repository', 'cls': 'CustomerInfo'},
                                          hook.visit_acquired_customer],  # 单一权限：只能访问指定的CustomerInfo
    'repository.add_model_obj': ['add_model_obj', 'GET', [], {}],  # 错误,没有定义kwargs的参数
    'repository.add_model_obj:POST': ['add_model_obj', 'GET', [], {}],  # 错误,没有定义kwargs的参数
    'repository.delete_model_obj:POST': ['delete_model_obj', 'POST', [], {}],  # 错误,没有定义kwargs的参数
    'repository.action_model_obj:POST': ['action_model_obj', 'POST', [], {}],  # 错误,没有定义kwargs的参数
    'repository.delete_collection:POST': ['delete_collection', 'POST', [], {}],  # 错误,没有定义kwargs的参数
}


# permission_items = {
#
#     'crm.table_index': ['table_index', 'GET', [], {'source': 'qq'}, ],  # 可以查看CRM APP里所有数据库表
#     'crm.table_list': ['table_obj_list', 'GET', [], {}, hook.view_my_own_customers],  # 可以查看每张表里所有的数据
#     'crm.table_list_view': ['table_obj_change', 'GET', [], {}],  # 可以访问表里每条数据的修改页
#     'crm.table_list_change': ['table_obj_change', 'POST', [], {}],  # 可以对表里的每条数据进行修改
#     'crm.table_obj_add_view': ['table_obj_add', 'GET', [], {}],  # 可以访问数据增加页
#     'crm.table_obj_add': ['table_obj_add', 'POST', [], {}],  # 可以创建表里的数据
#
# }
