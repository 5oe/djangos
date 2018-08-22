import re
from .models import *


class PermissionHelper(object):
    """
    1。八张表
    用户表：UserInfo
    角色表：RoleInfo
    用户表to角色表：User2Role

    URL表：UrlInfo  注意：该表的Url字段存的是正则
    可执行动作表：UrlActionInfo 注意：存的是增(add),删（delete）,改（change）,查（check）
    URL表to可执行动作表（权限表）：PermissionInfo  #为url绑定动作
    权限表to角色表：Permission2Role # 为角色赋予权限

    菜单表：MenuInfo

    2。我想要做什么？
         1.登录时存取权限 --> 做成装饰器
            -获取用户所有的权限(PermissionInfo),存放于session
            -获取用户的被权限依附的所有菜单,要求只展开当前url的菜单
        2.访问权限url时验证 --> 也是做成装饰器

    3。分析类应有的方法
        1.使用场景
        2.返回值的使用场景
        3.以上两步确定之后，便可以将问题细化
    """

    def __init__(self, request, username):
        self.request = request
        self.username = username
        self.store_info()

    def store_info(self):
        """
        存取菜单，权限 至session
        :return:

        ！！！不要乱！保持心性（清醒自己的目标，求胜，找出杂念，一刻也不要松懈），应用正确的方法！
        ！！！注意最少的那几样东西，进行攻击。目标和约束，愿意看到的场景，自知自省
        ！！！使用参考物来证明，编程是你自己聪明才智和勇气的体现,干其他事是你自己意志懦弱，重蹈覆辙的证明

        """
        # 权限方面
        # 1.根据用户的id或者用户名，获取其所有权限
        # 2.整理成{'index.html':['add','delete','check']} 格式
        # 3.存取至seesion

        # 菜单方面
        # 1.获取全部菜单，只有叶子级菜单才带url,但是中间级的菜单也需要显示出来。
        # 2.存取中间产物，至seesion
        # 3.借由中间产物，使得非当前url依附的菜单不打开
        # 4.借由中间产物生成最终的层级菜单
        # 5.并通过层级生成菜单html字符串传递给被装饰函数(通过kwargs)
        self.request.session['menus'] = self.get_menus()

    def get_permissions(self):
        """
        获得权限，并整理成{'index.html':['add','delete','check']} 格式，返回
        :param username: 
        :return: {'index.html':['add','delete','check']}
        """
        # 获取所有权限url，并去重
        roles = RoleInfo.objects.filter(user2role__user__username=self.username)
        permissions = PermissionInfo.objects.filter(permission2role__role__in=roles). \
            distinct().order_by('url')

        # 整理成类似{'index.html':['add','delete','check']}的格式
        ret = {}
        for row in permissions:
            ret.setdefault(row.url.url_name, [])
            ret[row.url.url_name].append(row.action.title)

        return ret

    def get_menus(self):
        """
        获得菜单，并返回中间产物
        :param username: 
        """
        menus = MenuInfo.objects.all()

        # 获取叶子菜单，减少多次查找
        tmp = UrlInfo.objects.all().values('menu_id')
        leaf_menu_id = []
        for dic in tmp:
            leaf_menu_id.append(dic['menu_id'])

        # 转化为指定数据结构的字典
        print(leaf_menu_id)
        menu_dict = {}
        for menu in menus:
            if menu.id in leaf_menu_id:
                url = menu.urlinfo_set.all()[0]
                url_name = url.url_name
                caption = url.caption
            else:
                url_name = ''
                caption = ''
            menu_dict[menu.id] = {
                'title': menu.title,
                'menu_parent_id': menu.partent_menu_id,
                'child': [],
                'url': url_name,
                'open': False,
                'display': False,
                'caption': caption
            }

        # 将子菜单和父菜单挂钩
        for k, v in menu_dict.items():
            parent_id = v['menu_parent_id']
            if parent_id:
                menu_dict[parent_id]['child'].append(v)

        # 将是该用户的菜单的菜单'显示',即display:True
        permissions = self.get_permissions()
        url_list = permissions.keys()

        for k, v in menu_dict.items():
            if v['url'] in url_list:
                menu_dict[k]['display'] = True
                parent_id = menu_dict[k]['menu_parent_id']
                while parent_id:
                    menu_dict[parent_id]['display'] = True
                    parent_id = menu_dict[parent_id]['menu_parent_id']

        return menu_dict

    def menu_ready(self):
        """
        该函数设置菜单字典为转化为html前的最终状态
        1.设置打开菜单为当前页面
        2.做成层级菜单，即去除非根级菜单。
        :return: 
        """
        menu_dict = self.get_menus()
        res = self.permission_test()
        if res:
            url, action = res
        else:
            return menu_dict

        # 设置打开菜单为当前页面
        for k, v in menu_dict.items():
            if v['url'] == url:
                menu_dict[k]['open'] = True
                parent_id = menu_dict[k]['menu_parent_id']
                while parent_id:
                    menu_dict[parent_id]['open'] = True
                    parent_id = menu_dict[parent_id]['menu_parent_id']
        # 转化为层级菜单
        finally_menu_dict = {}
        for k, v in menu_dict.items():
            if not v['menu_parent_id']:
                finally_menu_dict[k] = v
        return finally_menu_dict

    def permission_test(self):
        """
        权限测试
        :return:（index.html,['GET','POST','PUT'] 
        """
        url = self.request.path
        url = url[1:]  # '/avmoo'
        permissions = self.get_permissions()
        # {'index.html':['add','delete','check']}
        for k in permissions:
            param = k
            if re.match(param, url):
                return k, permissions[k]

    def create_html(self, menu_dict):
        """
        传入单一的层级。返回html
        :param menu_tree_dict: 
        :return: 
        """
        # menu_dict[menu.id] = {
        #     'title': menu.title,
        #     'menu_parent_id': menu.partent_menu_id,
        #     'child': [],
        #     'url': url,
        #     'open': False,
        #     'display': False,
        # }
        html = """
                    <div class="item %s">
                        <div class="title">%s</div>
                        <div class="content">%s</div>
                    </div>
                """

        active = ''
        if menu_dict['open']:
            active = 'active'

        title = menu_dict['title']

        content = ''
        if menu_dict['child']:
            for child_menu_dict in menu_dict['child']:
                content += self.create_html(child_menu_dict)
        else:
            content = '<a href = "%s">%s</a>' % (menu_dict['url'], menu_dict['caption'])

        return html % (active, title, content,)

    def create_menu_html(self):
        """
        传入层级菜单，返回所有菜单html组成的html
        :param menu_tree: 
        :return: 
        """
        menus_dict = self.menu_ready()
        ret = ''
        for v in menus_dict.values():
            ret += self.create_html(v)

        return ret
