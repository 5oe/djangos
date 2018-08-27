from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index),
    url('^(?P<app>\w+)/(?P<cls>\w+)/$', views.cls_index),
    url('^(?P<app>\w+)/$', views.app_index),
    url('^(?P<app>\w+)/(?P<cls>\w+)/add/$', views.add_model_obj),
    url('^(?P<app>\w+)/(?P<cls>\w+)/change/(?P<id>\d+)/$', views.model_obj),
    url(r'^teacher$', views.teacher, name='teacher'),
    url(r'^student$', views.student, name='student'),
    url(r'^sale$', views.sale, name='sale'),
    url(r'^news$', views.news, name='news'),
    url(r'^boss$', views.boss, name='boss'),
    url(r'^admin$', views.admin, name='admin')
]
