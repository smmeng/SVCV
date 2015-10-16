
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

#from myapp.forms import ProjectForm, InvestmentActivityForm
from myapp.models import PROJECT, InvestmentActivity, UserProfile

class Utility:
    
    def ValuesQuerySetToDict(self, vqs):
        return [item for item in vqs]

    # viewable_user_list defines a list of active investors 
    def viewable_user_list(self, request):
        allUser_list = None
        viewableUserId_list = None
        
        try:
            user = request.user
            myId =  request.user.id
            activeUsers = InvestmentActivity.objects.values('UserId').distinct()
            print 'viewable_user_list() activeUsers:  ', activeUsers
            
            if user.is_superuser: #for superusers. They can't view super users' records but staffs' records 
                allUser_list = User.objects.values('id', 'first_name', 'last_name', 'is_active').order_by('first_name').filter(id__in=activeUsers)
                viewableUserId_list = User.objects.values('id').filter(id__in=activeUsers)
            elif user.is_staff: #for staff users. They can't view super users' and other staffs' records 
                #activeUsers.append({'UserId':myId})
                allUser_list = User.objects.values('id', 'first_name', 'last_name', 'is_active').order_by('first_name').filter(Q(id__in=activeUsers, is_superuser=False, is_staff=False)|Q(id=myId))
                viewableUserId_list = User.objects.values('id').filter(Q(id__in=activeUsers, is_superuser=False, is_staff=False)|Q(id=myId))

            print 'viewable_user_list() allUser_list:', allUser_list, ' allUserId_list=', viewableUserId_list
            
        except InvestmentActivity.DoesNotExist:
        # We get here if we didn't find the specified project.
        # Don't do anything - the template displays the "no project" message for us.
            pass
        return  {'allUser_list': allUser_list , 'allUserId_list':viewableUserId_list}
        