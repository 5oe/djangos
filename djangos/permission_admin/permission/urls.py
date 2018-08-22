from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login),
    url(r'^backend$', views.test),
    url(r'^loginOut$', views.loginOut),
]
