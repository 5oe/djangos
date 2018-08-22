from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^/index-json$', views.IndexJsonView.as_view()),
    url(r'^/text$',views.text),
]
