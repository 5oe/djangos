from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^enroll/(?P<customer_id>\d+)/s1/$', views.enroll1, name='enroll1'),
    url(r'^enroll/(?P<customer_id>\d+)/s2/$', views.enroll2, name='enroll2'),
    url(r'^customer-info/(?P<customer_id>\d+)/(?P<contract_id>\d+)/$', views.customer_info, name='customer_info'),
    url(r'^enroll/upload/(?P<enrollment_id>\d+)/$', views.enroll_upload, name='enroll_upload'),
    url(r'download/(?P<enrollment_id>\d+)/$', views.download, name='download'),
    url(r'test/(?P<id>\d+)/(?P<enrollment_id>\d+)/$', views.test, name='test')

]
