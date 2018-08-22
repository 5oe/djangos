from django.shortcuts import render, HttpResponse
from .models import *
from .permission_helper import *


# Create your views here.
def test(request):
    username = 'zhaoziyi'
    p = PermissionHelper(request=request, username=username)
    menus = request.session['menus']
    menu_str = p.create_menu_html()

    return render(request, 'test.html', locals())


def loginOut(request):
    request.session.clear()


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        if not username:
            return render(request, 'login.html')
        try:
            user = UserInfo.objects.get(username=username)
        except UserInfo.DoesNotExist:
            return HttpResponse('没有该用户')

        # 获取用户的所有权限url
        roles = RoleInfo.objects.filter(user2role__user=user)
        permissions = PermissionInfo.objects.filter(permission2role__role__in=list(roles)).order_by('id').distinct()

        # 递归获取所有菜单
        menus = MenuInfo.objects.filter(partent_menu__isnull=True)
        '''
        [
         {'caption':'菜单1','child':[{'caption':'菜单1.1','child':[XXX]},{'child':'菜单1.2'}]},
         {'caption':'菜单2'},
          {'caption':'菜单3'},
        ]
        '''
        res = list()
        menu_handler(menus, res)
        print(res)

        #  更简单for循环解决
        print('*' * 100)
        menus = MenuInfo.objects.all()
        menu_dict = dict()  # key为菜单id，value为菜单信息
        # 第一步  创造出key为菜单id的大字典，并将菜单和权限组合在一起
        for menu in menus:
            menu_dict[menu.id] = {
                'title': menu.title,
                'menu_parent_id': menu.partent_menu_id,
                'child': [],
                'url': [],
                'display': False,
                'open': False,
            }
            if len(menu.permissioninfo_set.all()):
                for permission in menu.permissioninfo_set.all():
                    menu_dict[menu.id]['href'].append(str(permission))

        # 第二步 将父菜单和子菜单挂钩
        for key, val in menu_dict.items():
            if val['menu_parent_id']:
                parent_id = val['menu_parent_id']
                menu_dict[parent_id]['child'].append({key: val})
                # 让没url链接的菜单不显示
                while parent_id:
                    parent = menu_dict[parent_id]
                    parent['display'] = True
                    parent_id = parent['menu_parent_id']
                # 让请求的当前页面url菜单打开，其他关闭。
                import re
                if re.match(val['url'], request.path):  # TODO 未验证
                    val['open'] = True
                    parent_id = val['menu_parent_id']
                    while parent_id:
                        parent = menu_dict[parent_id]
                        parent['display'] = True
                        parent_id = parent['menu_parent_id']

            # 第三部 产生最终数据结构
            res_list = []
            for key, val in menu_dict.items():
                if not val['menu_parent_id']:
                    res_list.append({key: val})
            print(res_list)
            return HttpResponse('success')


def menu_html(child_list):
    html_str = '''
    <div class="item %s"> 
    <div class="title">%s</div>
    <div class="content">%s</div>
</div>
'''
    res = ''
    for row in child_list:
        if not row['display']: continue
        active = 'active' if row['open'] else ''

        if 'url' in row:
            res += '<a href="%s">%s</a>' % (row['url'], row['caption'])
        else:
            title = row['caption']
            content = menu_html(row['child'])
            res += html_str % (active, title, content)
    return html_str


def menu_handler(menus, res):
    for menu in menus:
        tmp = dict()
        tmp['caption'] = menu.title
        if len(menu.menuinfo_set.all()):
            tmp['child'] = list()
            menu_handler(list(menu.menuinfo_set.all()), tmp['child'])
        res.append(tmp)
