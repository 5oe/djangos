from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from responsitory.models import *
from utils import pagination
from backend.Forms import backend
import uuid


# Create your views here.

def index(request):
    return render(request, 'backend/backend_base.html')


def success_tips(request):
    return render(request, 'backend/backend.html')


def userinfo(request):
    return render(request, 'backend/backend-userinfo.html')


def article(request):
    return render(request, 'backend/backend-article.html')


def article_add(request):
    return render(request, 'backend/backend-article-add.html')


def article_tag(request):
    return render(request, 'backend/backend-tag.html')


def trouble(request):
    user = request.session.get('user')
    if not user:
        return redirect('/login')
    data_count = TroubleInfo.objects.filter(submitter_id=user['id']).count()
    p = request.GET.get('p')
    page = pagination.Pagination(p, data_count)
    datas = TroubleInfo.objects.filter(submitter_id=user['id'])[page.start:page.end]
    page_str = page.page_str(request.path)
    return render(request, 'backend/backend-trouble.html', locals())


def trouble_add(request):
    user = request.session.get('user')
    method = 'add'

    if not user:
        return redirect('/login')

    if request.method == 'GET':
        form = backend.TroubleInfoForm()
        return render(request, 'backend/backend-trouble-add.html', locals())
    elif request.method == 'POST':
        form = backend.TroubleInfoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            detail = form.cleaned_data['detail']
            u = uuid.uuid4()
            obj = TroubleInfo.objects.create(submitter_id=user['id'], title=title, detail=detail, uuid=u, )
            obj.save()
            return redirect('/backend/trouble')
        else:
            return render(request, 'backend/backend-trouble-add.html', locals())


def trouble_edit(request, trouble_id):
    user = request.session['user']
    method = 'edit'
    if request.method == 'GET':
        try:
            t = TroubleInfo.objects.get(id=int(trouble_id), status=-1)
        except Exception:
            return redirect('/backend/trouble')
        d = {'title': t.title, 'detail': t.detail}
        form = backend.TroubleInfoForm(initial=d)
        return render(request, 'backend/backend-trouble-add.html', locals())
    elif request.method == 'POST':
        form = backend.TroubleInfoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            detail = form.cleaned_data['detail']
            row = TroubleInfo.objects.filter(id=int(trouble_id), status=-1, submitter_id=user['id']). \
                update(title=title, detail=detail)
            if row == 0:
                return HttpResponse('不好意思，改迟一步了，单子状态已经被修改')
            return redirect('/backend/trouble')
        else:
            return render(request, 'backend/backend-trouble-add.html', locals())


def trouble_delete(request, trouble_id):
    user = request.session['user']
    try:
        t = TroubleInfo.objects.get(id=int(trouble_id), status=-1, submitter_id=user['id'])
    except Exception:
        return redirect('/backend/trouble')
    row = t.delete()
    if row:
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def trouble_handler(request):
    user = request.session.get('user')
    if not user:
        return redirect('/login')

    p = request.GET.get('p')
    data_count = TroubleInfo.objects. \
        filter(~Q(submitter_id=user['id']), status=-1, ).count()
    page = pagination.Pagination(p, data_count)
    datas = TroubleInfo.objects.filter(~Q(submitter_id=user['id']), status=-1) \
                .order_by('submit_time')[page.start:page.end]
    page_str = page.page_str(request.path)

    btn_status = -1
    return render(request, 'backend/backend-trouble-handler.html', locals())


def trouble_handling(request):
    user = request.session.get('user')
    if not user:
        return redirect('/login')

    p = request.GET.get('p')
    data_count = TroubleInfo.objects. \
        filter(submitter_id=user['id'], status=0, ).count()
    page = pagination.Pagination(p, data_count)
    datas = TroubleInfo.objects.filter(handler_id=user['id'], status=0) \
                .order_by('submit_time')[page.start:page.end]
    page_str = page.page_str(request.path)

    btn_status = 0
    return render(request, 'backend/backend-trouble-handler.html', locals())


def trouble_handled(request):
    user = request.session.get('user')
    if not user:
        return redirect('/login')

    p = request.GET.get('p')
    data_count = TroubleInfo.objects. \
        filter(submitter_id=user['id'], status=1, ).count()
    page = pagination.Pagination(p, data_count)
    datas = TroubleInfo.objects.filter(handler_id=user['id'], status=1) \
                .order_by('submit_time')[page.start:page.end]
    page_str = page.page_str(request.path)

    btn_status = 1
    return render(request, 'backend/backend-trouble-handler.html', locals())


def trouble_handler_show(request, trouble_id):
    user = request.session['user']
    try:
        t = TroubleInfo.objects.get(id=int(trouble_id))
    except TroubleInfo.DoesNotExist:
        return redirect('/backend/trouble')

    d = {'title': t.title, 'detail': t.detail}
    form = backend.TroubleInfoForm(initial=d)
    # form.fields['title'].widget.attrs['readonly'] = True
    # form.fields['detail'].widget.attrs['readonly'] = True
    form.fields['title'].disabled = True
    form.fields['detail'].disabled = True
    # form.detail.disabled = True
    return render(request, 'backend/backend-handler-detail.html', locals())


def trouble_handler_accept(request, trouble_id):
    user = request.session['user']
    t = TroubleInfo.objects.filter(id=int(trouble_id), status=-1)
    row = t.update(status=0, handler_id=user['id'])
    if row:
        return redirect('/backend/trouble_handling')
    else:
        return HttpResponse('单子被抢走了')


def trouble_handler_delete(request, trouble_id):
    user = request.session['user']
    t = TroubleInfo.objects.filter(id=int(trouble_id), status=0, handler_id=user['id'])
    row = t.update(status=-1, handler_id=None)
    if row:
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def trouble_handler_solute(request, trouble_id):
    user = request.session['user']
    try:
        t = TroubleInfo.objects.get(id=int(trouble_id), handler_id=user['id'])
    except TroubleInfo.DoesNotExist:
        return HttpResponse('去你妈的')
    d = {'title': t.title, 'detail': t.detail}
    if request.method == 'GET':
        form = backend.TroubleInfoForm(initial=d)
        # 这里如若使用disabled = True就会使得不会将该字段数据提交到POST里，导致form.is_valid失败
        form.fields['title'].widget.attrs['readonly'] = True
        form.fields['detail'].widget.attrs['readonly'] = True
        return render(request, 'backend/backend-trouble-solution.html', locals())
    elif request.method == 'POST':
        t = TroubleInfo.objects.filter(id=int(trouble_id), handler_id=user['id'])
        t_count = t.count()
        if not t_count:
            return HttpResponse('去你妈的')
        form = backend.TroubleInfoForm(request.POST)
        if form.is_valid():
            solution = form.cleaned_data['solution']
            row = t.update(solution=solution, status=1)
            if not row:
                return HttpResponse('添加解决方案失败')
            else:
                return redirect('/backend/trouble_handled')
        else:
            form.fields['title'].widget.attrs['readonly'] = True
            form.fields['detail'].widget.attrs['readonly'] = True
            return render(request, 'backend/backend-trouble-solution.html', locals())
