#from django.conf.urls import include, url
#from django.contrib import admin

#urlpatterns = [
    # Examples:
    # url(r'^$', 'pyMySQL.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#]
from django.conf.urls import patterns, include, url
#from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework import renderers
#from rest_framework.routers import DefaultRouter

from AirtrafficUI import  views
#from django.contrib.auth.forms import AdminPasswordChangeForm 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#RESTful Framework
#investor_list = InvestorViewSet.as_view({'get': 'list'})


urlpatterns = patterns('',
        url(r'^$', views.showRoutes, name='index'),     
        #url(r'^admin/', include(admin.site.urls)),
        url(r'^showRoutes/$', views.showRoutes),
        url(r'^showRouteData/$', views.showRouteData),
        url(r'^showRoutes0/', views.showRoutes0),
        url(r'^showBadPlanes/$', views.showBadPlanes),
)


#urlpatterns = format_suffix_patterns(urlpatterns)

