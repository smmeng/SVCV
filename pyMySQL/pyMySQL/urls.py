#from django.conf.urls import include, url
#from django.contrib import admin

#urlpatterns = [
    # Examples:
    # url(r'^$', 'pyMySQL.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#]
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from myapp import views, adminViews

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#RESTful Framework
#investor_list = InvestorViewSet.as_view({'get': 'list'})

router = DefaultRouter()
router.register(r'InvestorList', adminViews.InvestorViewSet)
router.register(r'users', adminViews.UserViewSet)
router.register(r'projects', adminViews.ProjectViewSet)
router.register(r'userProfiles', adminViews.UserProfileViewSet)

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),     
        url(r'^about-us.html/', views.aboutUs, name='aboutUs'),     
        url(r'^contact-us.html/', views.contactUs, name='contactUs'),
        url(r'^disclaimer.html/', views.disclaimer, name='disclaimer'),
        url(r'^ourProjects.html/', views.get_ourProjects),
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
        url(r'^save_UserProfile/(?P<id>\d+)/$', views.save_userProfile),
        # Change Password URLs:
        url(r'^changePassword/$', views.change_password),
        url(r'^savePassword/$', views.save_password),
        #RESTful implementation for ADMIN pages
        #url(r'^InvestorList/(?P<Pid>[0-9]+)/$', adminViews.InvestorDetail.as_view(),  name='InvestorList'),  
        url(r'^restapi/', include(router.urls)),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^projectInvestors/$', adminViews.get_projectInvestors),
        url(r'^testAG/$', adminViews.get_testAG),
        url(r'^encryptIt/$', adminViews.encryptIt),
        url(r'^decryptIt/$', adminViews.decryptIt),
)


#urlpatterns = format_suffix_patterns(urlpatterns)

