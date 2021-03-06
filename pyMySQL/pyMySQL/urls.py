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
#from django.contrib.auth.forms import AdminPasswordChangeForm 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#RESTful Framework
#investor_list = InvestorViewSet.as_view({'get': 'list'})

router = DefaultRouter()
router.register(r'InvestorList', adminViews.InvestorViewSet)
router.register(r'projects', adminViews.ProjectViewSet)
router.register(r'userProfiles', adminViews.UserProfileViewSet)
router.register(r'investmentActivity', views.activityViewSet)

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
        url(r'^overallProjects/$', views.OverallProjectsListView.as_view(),name='PROJECT-list'),
        #url(r'^overProjects/(?P<category_id>[0-9]+)/edit_entry/(?P<pk>[0-9]+)/$', views.OverallProjectoView().as_view(),name='project-view'),
        url(r'^add_project/$', views.add_project, name='add_project'),
        url(r'^add_project/(?P<id>\d+)/$', views.add_project, {}, name='add_project'),
        url(r'^edit_project/(?P<id>\d+)/$', views.add_project, {}, name='add_project'),  
        url(r'^activity/(?P<orderBy>[a-zA-Z]+)/$', views.get_activity, {}, name='get_activity'),
        url(r'^activity/', views.get_activity),        
        url(r'^activity2/', views.get_activity2),
        #url(r'^activityJSON/', views.get_activityJSON),  
        url(r'^profile/', views.get_userProfile),
        url(r'^announcement/', views.get_announcement),
        url(r'^save_UserProfile/$', views.save_userProfile),
        url(r'^save_UserProfile/(?P<id>\d+)/$', views.save_userProfile),
        # Change Password URLs:
        url(r'^changePassword/$', views.change_password),
        url(r'^savePassword/$', views.save_password),
        #RESTful implementation for ADMIN pages
        #url(r'^InvestorList/(?P<Pid>[0-9]+)/$', adminViews.InvestorDetail.as_view(),  name='InvestorList'),  
        url(r'^restapi/', include(router.urls)),
        #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^announcements/$', adminViews.announcementListView.as_view(), name="Announcements-list"),
        url(r'^announcements/add/$', adminViews.announcementCreateView.as_view(),name="Announcements-create"),
        url(r'^announcements/(?P<pk>\d+)/$', adminViews.announcementUpdateView.as_view(),name="Announcements-update"),
        url(r'^projectInvestors/$', adminViews.get_projectInvestors),
        url(r'^projectInvestorSummaryData/$', adminViews.get_projectInvestorSummaryData),
        url(r'^projectInvestorSummary/$', adminViews.get_projectInvestorSummary),
        url(r'^investorProfits/$', adminViews.getInvestorProfits),
        url(r'^testAG/$', adminViews.get_testAG),
        url(r'^encryptIt/$', adminViews.encryptIt),
        url(r'^decryptIt/$', adminViews.decryptIt),
        url(r'^investorProfitsJSON/$', adminViews.getInvestorProfitsJSON),
        url(r'^vendors/$', adminViews.VendorsListView.as_view(), name='Vendor-list'),
        url(r'^company/$', adminViews.CompanyListView.as_view(), name='Company-list'),
        url(r'^company/add/$', adminViews.CompanyCreateView.as_view(), name='Company-create'),
        url(r'^company/(?P<pk>\d+)/$', adminViews.CompanyUpdateView.as_view(), name='Company-update'),
        url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            views.reset_confirm, name='password_reset_confirm'),
        url(r'^reset/$', views.reset, name='reset'),
)


#urlpatterns = format_suffix_patterns(urlpatterns)

