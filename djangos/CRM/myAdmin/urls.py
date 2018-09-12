from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(\d+)$', views.Teacher.as_view(), name='teacher'),
    url(r'^student/$', views.student, name='student'),
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^news/$', views.news, name='news'),
    url(r'^boss/$', views.boss, name='boss'),
    url(r'^admin/$', views.admin, name='admin'),
    url('^$', views.index),
    url('^(?P<app>\w+)/(?P<cls>\w+)/$', views.cls_index, name='cls_index'),
    url('^(?P<app>\w+)/$', views.app_index),
    url('^(?P<app>\w+)/(?P<cls>\w+)/add/$', views.add_model_obj, name='add_model_obj'),
    url('^(?P<app>\w+)/(?P<cls>\w+)/change/(?P<id>\d+)/$', views.change_model_obj, name='change_model_obj'),
    url('^(?P<app>\w+)/(?P<cls>\w+)/delete/(?P<id>\d+)/$', views.delete_model_obj, name='delete_model_obj'),
    url('^(?P<app>\w+)/(?P<cls>\w+)/action/$', views.action_model_obj, name='action_model_obj'),
    url('^(?P<app>\w+)/(?P<cls>\w+)/delete_collection/$', views.delete_collection, name='delete_collection'),
]
