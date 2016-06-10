from django.conf.urls import include, url
from django.contrib import admin
from webapp import views
from django.views.generic import ListView, DetailView

from webapp.models import vistorType, visitorLog,employee

vistorType_detail  = DetailView.as_view(model=vistorType)
vistorType_list  = ListView.as_view(model=vistorType)
visitorLog_list = ListView.as_view(model=visitorLog)
employee_list = ListView.as_view(model=employee)

urlpatterns = [
    # Examples:
    # url(r'^$', 'pythonClass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^adminView/$', views.adminView),
    url(r'^aboutUs/$', views.aboutUs),
    url(r'^contactUs/$', views.contactUs)
    , 
    url(r'^visitorType0/(?P<pk>[0-9a-zA-Z\d]+)/$', vistorType_detail, name='vistorType_detail'),
    url(r'^visitorType/$', vistorType_list, name='vistorType_list' ),
    url(r'^visitorType/add/$', views.visitorTypeCreateView.as_view(), name='vistorType_create' ),
    url(r'^visitorType/(?P<pk>[0-9a-zA-Z\d]+)/$', views.visitorTypeUpdateView.as_view())
    ,
    url(r'^visitorLog0/$', visitorLog_list, name='visitorLog_list' ),
    url(r'^visitorLog/$', views.visitorLogListView.as_view(), name='visitorLog_list' ),
    url(r'^visitorLog/add/$', views.visitorLogCreateView.as_view(), name='visitorLog_create' ),
    url(r'^visitorLog/(?P<pk>[0-9a-zA-Z\d]+)/$', views.visitorLogUpdateView.as_view())
    ,
    url(r'^employee/$', employee_list, name='employee_list' ),
    url(r'^employee/add/$', views.employeeCreateView.as_view(), name='employee_create' ),
    url(r'^employee/(?P<pk>[0-9a-zA-Z\d]+)/$', views.employeeUpdateView.as_view()),

]
