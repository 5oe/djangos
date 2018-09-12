from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EnterView.as_view()),
    url(r'^teacher/$', views.Teacher.as_view(), name='teacher'),
    url(r'^student/$', views.student, name='student'),
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^news/$', views.news, name='news'),
    url(r'^boss/$', views.boss, name='boss'),
    url(r'^admin/$', views.admin, name='admin'),
]
