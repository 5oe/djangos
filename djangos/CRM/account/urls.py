from django.conf.urls import url
from . import views

urlpatterns = [
    url('^login', views.user_login),
    url('^logout', views.user_logout),
]


