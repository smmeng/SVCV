from django.conf.urls import include, url
from django.contrib import admin
from webapp import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'pythonClass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^visitorType/$', views.visitorTypeListView.as_view(), name='list')
]
