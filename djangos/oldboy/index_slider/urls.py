from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^job$', views.student_job),
    url(r'^stu$',views.students),
    url(r'^course_(?P<direct>\d+)_(?P<type>\d+)_(?P<level>\d+)$', views.courses),
]
