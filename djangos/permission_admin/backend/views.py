from django.shortcuts import render, HttpResponse
from django.db import transaction
from django.views import View
from permission.models import *
from util import pagination
import json


# Create your views here.

class IndexView(View):
    def get(self, request):
        page_num = request.GET.get('p', '1')
        return render(request, 'backend/success.html', locals())

    def post(self, request):
        pass

    def put(self, request):
        pass


class IndexJsonView(View):
    def get(self, request):
        table_config = [
            {
                'field': None,
                'title': '选择',
                'display': True,
                'text': {'content': '<input type="checkbox">'},
                'attrs': {},
            },
            {
                'field': 'id',
                'title': 'ID',
                'display': False,
                'text': {},
                'attrs': {},
            },

            {
                'field': 'username',
                'title': '姓名',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@username'}},
                'attrs': {'edit-enable': True, 'edit-type': 'input', 'origin': '@username'},
            },

            {
                'field': 'password',
                'title': '密码',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@password'}},
                'attrs': {'edit-enable': True, 'edit-type': 'input', 'origin': '@password'},
            },

            {
                'field': 'sex',
                'title': '性别',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@@sex_choices'}},
                'attrs': {'edit-enable': True, 'edit-type': 'select', 'global-name': 'sex_choices', 'origin': '@sex'},
            },

            {
                'field': 'age',
                'title': '年龄',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@age'}},
                'attrs': {'edit-enable': True, 'edit-type': 'input', 'origin': '@age'},
            },

            {
                'field': 'cls',
                'title': '班级',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@cls'}},
                'attrs': {'edit-enable': True, 'edit-type': 'input', 'origin': '@cls'},
            },

            {
                'field': 'place',
                'title': '所在地',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@place'}},
                'attrs': {'edit-enable': False, 'edit-type': 'input'},
            },

            {
                'field': 'school',
                'title': '学校',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@school'}},
                'attrs': {'edit-enable': True, 'edit-type': 'input', 'origin': '@school'},
            }
        ]
        conditions = [d['field'] for d in table_config if d['field']]
        current_page = request.GET.get('p', '1')
        data_count = UserInfo.objects.values(*conditions).count()
        page = pagination.Pagination(current_page, data_count, 4)
        datas = UserInfo.objects.values(*conditions)[page.start:page.end]
        page_str = page.page_str('/backend')

        data_list = list(datas)

        # 全局变量
        # 性别字典
        sex_choices = {t[0]: t[1] for t in UserInfo.sex_choices}

        # 分页标签
        res = {
            'table_config': table_config,
            'data_list': data_list,
            'global_dict': {
                'sex_choices': sex_choices,
            },
            'page_str': page_str,
        }

        return HttpResponse(json.dumps(res))

    @transaction.atomic
    def post(self, request):
#        save_point = transaction.savepoint()
        update_list = json.loads(str(request.body, encoding='utf8'))
        msg = '更新成功'
        ret = {'status': 1, 'msg': msg}
        id = None
        try:
            for d in update_list:
                id = d['id']
                UserInfo.objects.filter(id=id).update(**d)
        except Exception as e:
 #           transaction.savepoint_rollback(save_point)
            msg = '更新失败,错误行号:%s,错误信息:%s' % (id, str(e))
            ret = {'status': 0, 'msg': msg}

  #      transaction.savepoint_commit(save_point)
        return HttpResponse(json.dumps(ret))


def text(request):
    a = MenuInfo.objects.filter(urlinfo__id=1)
    print(a)
    return HttpResponse('aaa')
