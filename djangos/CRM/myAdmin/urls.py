from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.backend),
    url('^index/$', views.index),
    url('^(?P<app>\w+)/(?P<cls>\w+)/$',views.cls_index),
    url(r'^teacher$', views.teacher, name='teacher'),
    url(r'^student$', views.student, name='student'),
    url(r'^sale$', views.sale, name='sale'),
    url(r'^answer$', views.answer, name='answer'),
    url(r'^enroll$', views.enroll, name='enroll'),
    url(r'^question$', views.question, name='question')
]
