from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse


def process_return(request, **kwargs):
    app_name = kwargs['app_name']
    cls_name = kwargs['cls_name']
    id = kwargs['id']
    if 'save' in request.POST:
        return redirect(reverse('cls_index', kwargs={'app': app_name, 'cls': cls_name}))
    elif 'continue' in request.POST:
        return redirect(reverse('change_model_obj', \
                                kwargs={"app": app_name, 'cls': cls_name, 'id': id}))
    elif 'add_another' in request.POST:
        return redirect(reverse('add_model_obj', kwargs={"app": app_name, 'cls': cls_name}))


