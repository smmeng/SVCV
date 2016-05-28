from django.conf.urls import include, url
from django.contrib import admin
from webapp import views
from django.views.generic import ListView, DetailView

from webapp.models import vistorType

vistorType_detail  = DetailView.as_view(model=vistorType)
vistorType_list  = ListView.as_view(model=vistorType)

urlpatterns = [
    # Examples:
    # url(r'^$', 'pythonClass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^visitorType0/(?P<pk>[0-9a-zA-Z\d]+)/$', vistorType_detail, name='vistorType_detail'),
    url(r'^visitorType/$', vistorType_list, name='vistorType_list' ),
    url(r'^visitorType/add/$', views.visitorTypeCreateView.as_view(), name='vistorType_create' ),
    url(r'^visitorType/(?P<pk>[0-9a-zA-Z\d]+)/$', views.visitorTypeUpdateView.as_view()),
    #url(r'^update/', 'blog.blogapp.views.update'),
    #url(r'^delete/', 'blog.blogapp.views.delete'),
]
