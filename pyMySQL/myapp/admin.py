from django.contrib import admin

# Register your models here.
from myapp.models import  PROJECT, UserProfile, Status, Company, Vendor, Announcement, TransactionType, ProjectType

admin.site.register(PROJECT)
admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(Vendor)
admin.site.register(Status)
admin.site.register(Announcement)
admin.site.register(TransactionType)
admin.site.register(ProjectType)