from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success_tips),
    url(r'^userinfo$', views.userinfo),
    url(r'^article$', views.article),
    url(r'^article_add$', views.article_add),
    url(r'^article_tag$', views.article_tag),
    url(r'^trouble$', views.trouble),
    url(r'^trouble/add$', views.trouble_add),
    url(r'^trouble/(?P<trouble_id>\d+)/edit$', views.trouble_edit),
    url(r'^trouble/(?P<trouble_id>\d+)/delete$', views.trouble_delete),
    url(r'^trouble_handler$', views.trouble_handler),
    url(r'^trouble_handling$', views.trouble_handling),
    url(r'^trouble_handled$', views.trouble_handled),
    url(r'^trouble_handler/(?P<trouble_id>\d+)/show$', views.trouble_handler_show),
    url(r'^trouble_handler/(?P<trouble_id>\d+)/accept$', views.trouble_handler_accept),
    url(r'^trouble_handler/(?P<trouble_id>\d+)/delete$', views.trouble_handler_delete),
    url(r'^trouble_handler/(?P<trouble_id>\d+)/solute$', views.trouble_handler_solute),
]
