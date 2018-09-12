from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^create_verify_code/$', views.create_verify_code),
    url(r'^change_password/$', views.change_password),
    url(r'^register/$', views.user_register),
]
