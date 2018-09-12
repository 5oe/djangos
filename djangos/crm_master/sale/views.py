import os
import json
from django.conf import settings
from django.http import Http404, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_exempt

from repository.models import *
from form.sale.enroll import EnrollFormClassFactory
from django.core.urlresolvers import reverse


# Create your views here.
def enroll1(request, customer_id):
    customer = get_object_or_404(CustomerInfo, id=customer_id)
    user = request.user  # 课程顾问自己

    # 这是步骤一函数，若已经存储在数据库里头，则跳转至步骤二
    if EnrollmentInfo.objects.filter(customer=customer, consultant=user).first():
        if not request.GET.get('reset'):
            return redirect(reverse('enroll2', kwargs={'customer_id': customer_id}))
        if request.method == 'POST' and request.GET.get('reset'):
            EnrollmentInfo.objects.filter(customer=customer, consultant=user).delete()

    form_cls = EnrollFormClassFactory.from_base_info(customer=customer, consultant=user)
    context = {
        'customer': customer,
        'consultant': user,
    }
    if request.method == 'GET':
        context.update({'form': form_cls()})
        return render(request, 'sale/enroll1.html', context)

    elif request.method == 'POST':
        form = form_cls(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('enroll2', kwargs={'customer_id': customer_id}))
        else:
            context.update({'form': form})
            return render(request, 'sale/enroll1.html', context)


def enroll2(request, customer_id):
    return HttpResponse('fuck')
    # customer = get_object_or_404(CustomerInfo, id=customer_id)
    # user = request.user  # 课程顾问自己
    #
    # if EnrollmentInfo.objects.filter(customer=customer, consultant=user).first():
    #     if not request.GET.get('reset'):
    #         return redirect(reverse('enroll2', kwargs={'customer_id': customer_id}))
    #     if request.method == 'POST' and request.GET.get('reset'):
    #         EnrollmentInfo.objects.filter(customer=customer, consultant=user).delete()
    #
    # form_cls = EnrollFormClassFactory.from_base_info(customer=customer, consultant=user)
    # context = {
    #     'customer': customer,
    #     'consultant': user,
    # }
    # if request.method == 'GET':
    #     context.update({'form': form_cls()})
    #     return render(request, 'sale/enroll1.html', context)
    #
    # elif request.method == 'POST':
    #     form = form_cls(data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse('enroll2', kwargs={'customer_id': customer_id}))
    #     else:
    #         context.update({'form': form})
    #         return render(request, 'sale/enroll1.html', context)


def customer_info(request, customer_id, contract_id):
    from repository.models import CustomerInfo
    from form.sale.customer_info import EnrollmentForm, CustomerDetailForm
    user = request.user  # 课程顾问自己
    customer = get_object_or_404(CustomerInfo, id=customer_id)
    enrollment = get_object_or_404(EnrollmentInfo, customer=customer, consultant=user)
    contract = get_object_or_404(ContractTemplateInfo, id=contract_id)

    detail_form = CustomerDetailForm()
    enrollment_form = EnrollmentForm(instance=enrollment)
    return render(request, 'sale/customer_info.html', locals())


@csrf_exempt
def enroll_upload(request, enrollment_id):
    from form.sale.customer_info import ImgForm
    enrollment_upload_dir = os.path.join(settings.CRM_FILE_UPLOAD_DIR, enrollment_id)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)

    form = ImgForm(request.POST, request.FILES)
    if form.is_valid():
        print('@ok' * 10)
    else:
        print(form.errors)
        print('!' * 20)

    file_obj = request.FILES.get('file')
    if len(os.listdir(enrollment_upload_dir)) < 2:
        with open(os.path.join(enrollment_upload_dir, file_obj.name), "wb") as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        return HttpResponse(json.dumps({'status': False, 'err_msg': 'max upload limit is 2'}))
    return HttpResponse(json.dumps({'status': True, }))


def download(request, enrollment_id):
    def file_iterator(file_path, chunk_size=1024):
        with open(file_path, 'rb', ) as f:  # 循环打开 文件#以二进制读模式打开
            while True:
                byte = f.read(chunk_size)  #
                if byte:
                    yield byte
                else:
                    break

    enrollment_upload_dir = os.path.join(settings.CRM_FILE_UPLOAD_DIR, enrollment_id)
    file_name = os.listdir(enrollment_upload_dir)[0]
    file_path = os.path.join(enrollment_upload_dir, file_name)
    print(file_path)

    response = StreamingHttpResponse(file_iterator(file_path))  # StreamingHttpResponse是将文件内容进行流式传输
    response['Content-Type'] = 'application/octet-stream'  # 文件类型 #应用程序/octet-stream.*（ 二进制流，不知道下载文件类型）
    file_name = 'attachment;filename=%s' % file_name  # 文件名字# 支持中文
    response['Content-Disposition'] = file_name.encode()  # 支持中文#编码默认encoding='utf-8'
    return response  # 返回下载 请求的内容


def test(request, id, enrollment_id):
    from django.core.urlresolvers import resolve
    obj = resolve(request.path)
    print(id, '@@@')
    print(obj, obj.url_name)
    print('*' * 10, dir(obj))
    return render(request, 'sale/t.html')
