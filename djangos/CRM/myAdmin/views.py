from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from myAdmin import site
from django.views import View
from .view_libs import process_return

site.import_admin()

from form.myAdmin.cls_index import AppArgsForm, AppClsArgsForm, AppClsObjArgsForm
from form.myAdmin.model_obj import FormClassFactory


# Create your views here.
def index(request):
    info = site.get_total_cls()
    return render(request, 'myAdmin/index.html', {'info': info, 'title': '站点管理'})


def app_index(request, **kwargs):
    form = AppArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        info = {app_name: site.get_cls_list(app_name)}
        return render(request, 'myAdmin/index.html', {'info': info, 'title': app_name})
    else:
        raise Http404('你所访问的页面不存在')


def cls_index(request, **kwargs):
    form = AppClsArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        model_admin = site.get_admin(app_name, cls_name)

        from view_model.myAdmin.cls_index import ClsIndexViewModel
        view_model = ClsIndexViewModel(request, model_admin)
        base_context = {
            'title': cls_name,
            'app_name': app_name,
            'cls_name': cls_name
        }
        context = view_model.get_context(request, **base_context)
        return render(request, 'myAdmin/cls_index.html', context)
    else:
        raise Http404("你所访问的页面不存在")


def change_model_obj(request, **kwargs):
    from view_model.myAdmin.model_obj import ModelObjViewModel
    form = AppClsObjArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        id = form.cleaned_data['id']

        admin = site.get_admin(app_name=app_name, cls_name=cls_name)
        obj = admin.cls_info.objects.get(id=int(id))
        view_model = ModelObjViewModel(admin, obj)
        form_cls = FormClassFactory.from_admin(admin)
        base_context = {
            'title': obj,
            'app_name': app_name, 'cls_name': cls_name,
            'model_obj': obj
        }

        if request.method == 'GET':
            form = form_cls(instance=obj)
            context = view_model.get_context(**{'form': form}, **base_context)
            return render(request, 'myAdmin/model-obj.html', context)

        elif request.method == 'POST':
            form = form_cls(instance=obj, data=request.POST)
            if form.is_valid():
                n_obj = form.save()
                return process_return(request, app_name=app_name, cls_name=cls_name, id=n_obj.id)
            else:
                context = view_model.get_context(**{'form': form}, **base_context)
                return render(request, 'myAdmin/model-obj.html', context)
    else:
        raise Http404('你所访问的页面不存在')


def add_model_obj(request, **kwargs):
    from view_model.myAdmin.model_obj import ModelObjViewModel
    form = AppClsArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']

        admin = site.get_admin(app_name=app_name, cls_name=cls_name)
        form_cls = FormClassFactory.from_admin(admin, is_add=True)
        view_model = ModelObjViewModel(admin)
        base_context = {
            'title': '增加 ' + cls_name,
            'app_name': app_name,
            'cls_name': cls_name,
            'add': True
        }

        if request.method == "GET":
            form = form_cls()
            context = view_model.get_context(**{'form': form}, **base_context)
            return render(request, 'myAdmin/model-obj.html', context)

        elif request.method == "POST":
            form = form_cls(request.POST)
            if form.is_valid():
                obj = form.save()
                return process_return(request, app_name=app_name, cls_name=cls_name, id=obj.id)
            else:
                context = view_model.get_context(**{'form': form}, **base_context)
                return render(request, 'myAdmin/model-obj.html', context)
    else:
        raise Http404('你所访问的页面不存在')


def delete_model_obj(request, **kwargs):
    from view_model.myAdmin.model_del import ModelDelViewModel
    form = AppClsObjArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        id = form.cleaned_data['id']

        admin = site.get_admin(app_name=app_name, cls_name=cls_name)
        obj = admin.cls_info.objects.get(id=int(id))
        if request.method == 'GET':
            view_model = ModelDelViewModel(admin, obj)
            base_context = {
                'title': obj,
                'app_name': app_name,
                'cls_name': cls_name,
                'model_obj': obj
            }
            context = view_model.get_context(**base_context)
            return render(request, 'myAdmin/model-del.html', context)

        elif request.method == 'POST':
            obj.delete()
            return redirect(reverse('cls_index', kwargs={'app': app_name, 'cls': cls_name}))
    else:
        return Http404


def action_model_obj(request, **kwargs):
    from view_model.myAdmin.model_del import ModelDelCollectionViewModel
    form = AppClsArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        admin = site.get_admin(app_name=app_name, cls_name=cls_name)
        id_list = request.POST.getlist('id')
        func_name = request.POST.get('action', '')
        query_set = admin.cls_info.objects.filter(id__in=id_list)
        view_model = ModelDelCollectionViewModel(admin, query_set)
        base_context = {
            'title': '你确定吗?',
            'app_name': app_name,
            'cls_name': cls_name,
            'model_obj': '%s多个对象' % cls_name
        }
        context = view_model.get_context(**base_context, id_list=id_list)
        if func_name == admin.del_action_func_name:
            return render(request, 'myAdmin/model-del-collection.html', context)
        else:
            admin.execute_action(func_name, request, query_set)
            return redirect(reverse('cls_index', kwargs={'app': app_name, 'cls': cls_name}))
    else:
        return Http404


def delete_collection(request, **kwargs):
    if request.method == 'POST':
        form = AppClsArgsForm(kwargs)
        if form.is_valid():
            app_name = form.cleaned_data['app']
            cls_name = form.cleaned_data['cls']
            admin = site.get_admin(app_name=app_name, cls_name=cls_name)
            id_list = request.POST.getlist('id')
            query_set = admin.cls_info.objects.filter(id__in=id_list)
            query_set.delete()
            return redirect(reverse('cls_index', kwargs={'app': app_name, 'cls': cls_name}))
    else:
        return Http404


class Teacher(View):  # 自定义的类必须继承View
    # 重写父类dispatch方法。程序定制时可以使用
    # 父类的dispatch方法，查找get、post等方法，基于反射实现的。
    def dispatch(self, request, *args, **kwargs):
        print("类似装饰器：before")
        print(*args, **kwargs)
        result = super(Teacher, self).dispatch(request, *args, **kwargs)
        print("类似装饰器：after")
        return result

    def get(self, request, *args, **kwargs):  # 定义get方法，get请求执行这个方法
        print(request.method)
        return render(request, 'myAdmin/test.html')

    def post(self, request, *args, **kwargs):  # 定义post方法，post请求执行这个方法
        print(request.method, "post方式")
        return render(request, 'myAdmin/test.html')


def student(request):
    return render(request, 'father.html')


def sale(request):
    return render(request, 'sub.html')


def news(request):
    pass


def admin(request):
    pass


def boss(request):
    pass
