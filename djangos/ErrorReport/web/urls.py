from django.conf.urls import url
from . import views
from utils.uplaod import upload_image

urlpatterns = [
    url(r'^login$', views.login),
    url(r'loginOut', views.login_out),
    url(r'^register$', views.register),
    url(r'^fregister$', views.fregister),
    url(r'^test$', views.test),
    url(r'register_check_username', views.register_check_username),
    url(r'verify_code', views.create_verify_code),
    url(r'^blog_article$', views.blog_article),
    url(r'^type_(?P<index_kind>[1-3])', views.index, name='index'),
    url(r'^$', views.index),
    # url(r'^(?P<surfix>.+)_(?P<tag>\d+)_(?P<type>\d+)_(?P<time>.+)', views.blog, name='blog'),
    url(r'^(?P<surfix>\w+)/(?P<article_id>\d+)/page_handler$', views.page_handler),
    url(r'^(?P<surfix>\w+)/(?P<article_id>\d+)$', views.blog_article, name='blog_article'),
    url(r'^(?P<surfix>\w+)/(?P<condition>((tag)|(type)|(date)))=(?P<value>.+)', views.blog, name='blog'),
    url(r'^(?P<surfix>\w+)$', views.blog),
]
