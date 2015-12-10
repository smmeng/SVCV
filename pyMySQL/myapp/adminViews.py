from myapp.utility import Utility
from django.contrib.auth.decorators import login_required

################## To generate all user list based on the current role
@login_required
def adminGetAllUsers(request):
    user = request.user
    print 'get_activity() ] user=[', user

    if user.is_staff or user.is_superuser:
        util = Utility()
        user_list = util.viewable_user_list(request)
    
    #allUserId_list = user_list['allUserId_list']
    #allUser_list = user_list['allUser_list']

    
    #activity_dict= {'allUserId_list', 'allUser_list':allUser_list, 'investorId':uid, 'investorName':userName}
    #print 'get_activity() activity_dict[', activity_dict
    # We also add the project object from the database to the context dictionary.
    # We'll use this in the template to verify that the project exists.
    #activity_dict['projects'] = activity_list

    # Go render the response and return it to the client.
    return user_list

