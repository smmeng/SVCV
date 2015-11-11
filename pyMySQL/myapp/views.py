#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import   User
from django.db.models import Q

from myapp.forms import ProjectForm,  UserProfileForm
from myapp.models import PROJECT, InvestmentActivity, UserProfile

from myapp.utility import Utility
#from myapp import RegisterTableColumns
#import MySQLdb

###############Log in
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your SVCV account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})
    
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
################## Project related
@login_required
def get_projects(request):
    
    # Create a context dictionary which we can pass to the template rendering engine.
    project_dict = {}

    try:
        # Can we find a project name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        project_list = PROJECT.objects.all()

        # We also add the project object from the database to the context dictionary.
        # We'll use this in the template to verify that the project exists.
        #project_dict['projects'] = project_list
        
        total = 0
        total_principal = 0
        total_distribution = 0
        
        for item in project_list:
            if (item.Status_id == 'Completed'):
                total_distribution += item.Committed
            else:
                total_principal += item.Committed
                
            total +=  item.Committed

        project_dict= {'projects': project_list, 'total_amount': total, 'total_distribution':total_distribution, 'total_principal':total_principal}

    except PROJECT.DoesNotExist:
        # We get here if we didn't find the specified project.
        # Don't do anything - the template displays the "no project" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'project.html', project_dict, )

@login_required
def add_project(request, id=None):
    print 'add_project() received request.method[{}] projectId[{}]'.format(request.method, id)
    
    project = None
    user = request.user
    if not user.is_staff  and not user.is_superuser : 
        print 'not staff or superuser!! Forward to home'
        return render(request, 'index.html')

    
    if id:
        project = PROJECT.objects.get(pk=id)

    print 'Found project[{}]'.format(project)
                                      
    # A HTTP POST? 
    if request.method == 'POST':
        
        if id == None:
            form = ProjectForm(request.POST)
        else:
            #form = ProjectForm(request.POST, instance=project)
            object_to_edit = get_object_or_404(PROJECT, ProjectId=id) #Or slug=slug
            print 'Found object_to_edit[{}]'.format(object_to_edit)
            form = ProjectForm(data = request.POST or None, instance=object_to_edit)
    
        # Have we been provided with a valid form?
        form.fields['ProjectId'].required = False
        if form.is_valid():
            # Save the new project to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return get_projects(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        if project is None:
            form = ProjectForm()
        else:
            form = ProjectForm(instance=project)

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_project.html', {'form': form})
    #return render(request, 'project.html', {}, RequestContext(request))


################## for investment activity history
@login_required
def get_activity(request, orderBy=None):
    # Create a context dictionary which we can pass to the template rendering engine.
    activity_dict = {}
    user = request.user
    
    util = Utility()
    user_list = util.viewable_user_list(request)
    allUserId_list = user_list['allUserId_list']
    allUser_list = user_list['allUser_list']

    uid=request.POST.get('investorId')
    userName = None
    activity_list = None
    print 'get_activity() orderBy=[', orderBy, "] id=[", uid
    
    sess= request.session;
    sess_userId_label = "current_activity_uid"
    sess_orderBy_label = "current_orderBy"
    
    if request.method == 'GET' and uid == None and sess.get(sess_userId_label) != None:
        uid = sess.get(sess_userId_label)
        print 'get_activity() finds session stored uid=', uid

    oldOrderBy = sess.get(sess_orderBy_label)
    
    if orderBy == None:
        orderBy = '-Date'
    elif orderBy == oldOrderBy and orderBy != 'NONE':
        orderBy = '-' + orderBy #sort descending

    sess[sess_orderBy_label] = orderBy

    try:
        if uid == None or uid == '---': # investor self look up 
            userId = request.user.id
            uid = userId
            if orderBy == 'NONE':
                activity_list = InvestmentActivity.objects.filter(UserId = userId)
            else :
                activity_list = InvestmentActivity.objects.filter(UserId = userId).order_by(orderBy)
            
            userName = User.objects.filter(id = uid).values_list('first_name', 'last_name')
        elif uid == 'ALL'  and (user.is_staff or user.is_superuser) : # fetch all records the current user is allowed to view
            if orderBy == 'NONE':
                activity_list = InvestmentActivity.objects.all().filter(UserId__in=allUserId_list)
            else:
                activity_list = InvestmentActivity.objects.all().filter(UserId__in=allUserId_list).order_by(orderBy)
            userName = [(u'ALL', u'USERS')]
        else:
            userName = User.objects.filter(id = uid).values_list('first_name', 'last_name')
            
            if orderBy == 'NONE':
                activity_list = InvestmentActivity.objects.select_related('ProjectId__Status').filter(UserId = uid)
            else:
                activity_list = InvestmentActivity.objects.select_related('ProjectId__Status').filter(UserId = uid).order_by(orderBy)
        
        sess[sess_userId_label] = uid
            
        print 'get_activity() user record=', userName
        total = 0.0
        total_principal = 0.0
        total_distribution = 0.0
        
        for item in activity_list:
            if (item.Type_id == 'Deposit'):
                total_principal += item.Amount
            elif (item.Type_id == 'Check'):
                total_distribution += item.Amount
                
            total +=  item.Amount
        
        activity_dict= {'activities': activity_list, 'total_amount': total, 'total_distribution':total_distribution, 'total_principal':total_principal, 'allUser_list':allUser_list, 'investorId':uid, 'investorName':userName}
        print 'get_activity() activity_dict[', activity_dict
        # We also add the project object from the database to the context dictionary.
        # We'll use this in the template to verify that the project exists.
        #activity_dict['projects'] = activity_list
    except InvestmentActivity.DoesNotExist:
        # We get here if we didn't find the specified project.
        # Don't do anything - the template displays the "no project" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'activity.html', activity_dict)

################## for updating userProfile
@login_required
def get_userProfile(request):
    user = request.user
    myUserId = user.id
    print 'myUserId=[', myUserId

    profileInfo = UserProfile.objects.filter(UserId = myUserId )
    #profileInfo = UserProfile.objects.get(pk=myUserId)
    print 'profileInfo=', profileInfo.count()
         
    if profileInfo is None or profileInfo.count() == 0:
        form = UserProfileForm()
        dbOperation = 'Create'
    else:
        form = UserProfileForm(instance=profileInfo)
        dbOperation = 'Update'

    print 'form=', form
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'userProfile.html', {'myUserId':myUserId, 'dbOperation':dbOperation, 'form': form})
    #return render(request, 'userProfile.html', userProfile_dict)
    
########################################################################
def index(request):
    return render(request, 'index.html')


