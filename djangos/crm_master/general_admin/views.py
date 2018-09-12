from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from general_admin import site
from django.views import View
from .view_libs import process_return
from utils.permissions.decorator import check_permission

site.import_admin()

from general_admin.form.cls_index import AppArgsForm, AppClsArgsForm, AppClsObjArgsForm
from general_admin.form.model_obj import FormClassFactory


# Create your views here.
@check_permission
def index(request):
    info = site.get_total_cls()
    return render(request, 'general_admin/index.html', {'info': info, 'title': '站点管理'})


@check_permission
def app_index(request, **kwargs):
    form = AppArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        info = {app_name: site.get_cls_list(app_name)}
        return render(request, 'general_admin/index.html', {'info': info, 'title': app_name})
    else:
        raise Http404('你所访问的页面不存在')


@check_permission
def cls_index(request, **kwargs):
    form = AppClsArgsForm(kwargs)
    if form.is_valid():
        app_name = form.cleaned_data['app']
        cls_name = form.cleaned_data['cls']
        model_admin = site.get_admin(app_name, cls_name)

        from general_admin.view_model.cls_index import ClsIndexViewModel
        view_model = ClsIndexViewModel(request, model_admin)
        base_context = {
            'title': cls_name,
            'app_name': app_name,
            'cls_name': cls_name
        }
        context = view_model.get_context(request, **base_context)
        return render(request, 'general_admin/cls_index.html', context)
    else:
        raise Http404("你所访问的页面不存在")


def change_model_obj(request, **kwargs):
    from general_admin.view_model.model_obj import ModelObjViewModel
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
            return render(request, 'general_admin/model-obj.html', context)

        elif request.method == 'POST':
            form = form_cls(instance=obj, data=request.POST)
            if form.is_valid():
                n_obj = form.save()
                add_popup_flag = request.GET.get('change_popup')
                if add_popup_flag:
                    context = view_model.get_context(**{'form': form}, **base_context)
                    return render(request, 'general_admin/model-obj.html', context)
                else:
                    return process_return(request, app_name=app_name, cls_name=cls_name, id=n_obj.id)
            else:
                context = view_model.get_context(**{'form': form}, **base_context)
                return render(request, 'general_admin/model-obj.html', context)
    else:
        raise Http404('你所访问的页面不存在')


@check_permission
def add_model_obj(request, **kwargs):
    from general_admin.view_model.model_obj import ModelObjViewModel
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
            return render(request, 'general_admin/model-obj.html', context)

        elif request.method == "POST":
            form = form_cls(request.POST)
            if form.is_valid():
                obj = form.save()
                add_popup_flag = request.GET.get('add_popup')
                if add_popup_flag:
                    return render(request, 'general_admin/model-obj.html', {'form': form})
                else:
                    return process_return(request, app_name=app_name, cls_name=cls_name, id=obj.id)
            else:
                context = view_model.get_context(**{'form': form}, **base_context)
                return render(request, 'general_admin/model-obj.html', context)
    else:
        raise Http404('你所访问的页面不存在')


@check_permission
def password_reset(request, **kwargs):
    from general_admin.form.password_reset import PasswordArgsForm
    from general_admin.form.password_reset import PasswordChangeForm
    from general_admin.view_model.model_obj import ModelObjViewModel

    form = PasswordArgsForm(kwargs)
    if not form.is_valid():
        return Http404('你所访问的页面不存在')

    app_name = form.cleaned_data['app']
    cls_name = form.cleaned_data['cls']
    id = form.cleaned_data['id']

    admin = site.get_admin(app_name=app_name, cls_name=cls_name)
    user = admin.cls_info.objects.get(id=int(id))
    view_model = ModelObjViewModel(admin)
    base_context = {
        'title': '重置 %s 的密码' % user,
        'app_name': app_name, 'cls_name': cls_name,
        'model_obj': user
    }
    context = view_model.get_context(**base_context)

    if request.method == 'GET':
        form = PasswordChangeForm()
        context.update({'form': form})
        return render(request, 'general_admin/password-reset.html', context)
    elif request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password2'])
            user.save()
            if request.GET.get('popup') == '1':
                context.update({'form': form, 'success_flag': True})
        else:
            context.update({'form': form})
        return render(request, 'general_admin/password-reset.html', context)


@check_permission
def delete_model_obj(request, **kwargs):
    from general_admin.view_model.model_del import ModelDelViewModel
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
            return render(request, 'general_admin/model-del.html', context)

        elif request.method == 'POST':
            obj.delete()
            return redirect(reverse('cls_index', kwargs={'app': app_name, 'cls': cls_name}))
    else:
        return Http404


@check_permission
def action_model_obj(request, **kwargs):
    from general_admin.view_model.model_del import ModelDelCollectionViewModel
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
            return render(request, 'general_admin/model-del-collection.html', context)
        else:
            admin.execute_action(func_name, request, query_set)
            return redirect(reverse('cls_index', kwargs={'app': app_name, 'cls': cls_name}))
    else:
        return Http404


@check_permission
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
