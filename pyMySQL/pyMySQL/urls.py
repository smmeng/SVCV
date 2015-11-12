#from django.conf.urls import include, url
#from django.contrib import admin

#urlpatterns = [
    # Examples:
    # url(r'^$', 'pyMySQL.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#]
from django.conf.urls import patterns, include, url
from myapp import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),     
        url(r'^admin/', include(admin.site.urls)),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^projects/', views.get_projects),
        url(r'^add_project/$', views.add_project, name='add_project'),
        url(r'^add_project/(?P<id>\d+)/$', views.add_project, {}, name='add_project'),
        url(r'^edit_project/(?P<id>\d+)/$', views.add_project, {}, name='add_project'),  
        url(r'^activity/(?P<orderBy>[a-zA-Z]+)/$', views.get_activity, {}, name='get_activity'),
        url(r'^activity/', views.get_activity),
        url(r'^profile/', views.get_userProfile),
        url(r'^save_UserProfile/$', views.save_userProfile),
)

