from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from myAdmin import site

site.import_admin()

from form.myAdmin.cls_index import AppArgsForm, AppClsArgsForm
from libs.format import pack_base_info, get_cls_index_dict


# Create your views here.

def backend(request):
    return render(request, 'base.html')


def index(request):
    info = site.get_all_app_cls()
    return render(request, 'myAdmin/index2.html', {'info': info, 'title': '站点管理'})


def app_index(request, **kwargs):
    form = AppArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        info = site.get_app_cls(app_name)
        return render(request, 'myAdmin/index2.html', {'info': info, 'title': app_name})
    else:
        raise Http404('你所访问的页面不存在')


def cls_index(request, **kwargs):
    form = AppClsArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        model_admin = site.model_admin(app_name, cls_name)
        args_dict = get_cls_index_dict(request)

        from view_model.myAdmin.cls_index import ClsIndexViewModel
        context = ClsIndexViewModel.cls_index_context(model_admin, args_dict)
        context.update(pack_base_info(request, app_name, cls_name, ))
        return render(request, 'myAdmin/cls_index2.html', context)
    else:
        raise Http404("你所访问的页面不存在")


def teacher(request):
    # from responsitory.models import *
    # CourseInfo.objects.filter(id)
    return render(request, 'myAdmin/admin.html')


def student(request):
    pass


def news(request):
    pass


def admin(request):
    pass


def boss(request):
    pass


def sale(request):
    pass
