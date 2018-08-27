from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from myAdmin import site

site.import_admin()

from form.myAdmin.cls_index import AppArgsForm, AppClsArgsForm, AppClsObjArgsForm
from form.myAdmin.model_obj import FormClassFactory


# Create your views here.

def backend(request):
    return render(request, 'base.html')


def index(request):
    info = site.get_total_cls()
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
        model_admin = site.get_admin(app_name, cls_name)

        from view_model.myAdmin.cls_index import ClsIndexViewModel
        view_model = ClsIndexViewModel(request, model_admin)
        context = view_model.get_context(request, **{'title': cls_name, 'app_name': app_name, 'cls_name': cls_name})
        return render(request, 'myAdmin/cls_index2.html', context)
    else:
        raise Http404("你所访问的页面不存在")


def model_obj(request, **kwargs):
    form = AppClsObjArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        id = form.cleaned_data['id']
        model_admin = site.get_admin(app_name=app_name, cls_name=cls_name)
        model_obj = model_admin.cls_info.objects.get(id=int(id))
        form_cls = FormClassFactory.from_admin(model_admin)
        form = form_cls(instance=model_obj)
        context = {'form': form}
        return render(request, 'myAdmin/model-obj.html', context)
    else:
        raise Http404('你所访问的页面不存在')


def add_model_obj(request, **kwargs):
    form = AppClsArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        model_admin = site.get_admin(app_name=app_name, cls_name=cls_name)
        form_cls = FormClassFactory.from_admin(model_admin)
        form = form_cls()
        context = {'form': form}
        return render(request, 'myAdmin/model-obj.html', context)
    else:
        raise Http404('你所访问的页面不存在')


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
