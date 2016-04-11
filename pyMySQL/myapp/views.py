#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import   User
from django.db.models import Q
from datetime import date
from django.views.generic import   ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from myapp.forms import ProjectForm,  UserProfileForm
from myapp.models import PROJECT, InvestmentActivity, UserProfile,Announcement, Vendor

from myapp.utility import Utility, FieldSet

from django.views.decorators.csrf import csrf_exempt  
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

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
        #HttpResponse.set_cookie(this, "agree2disclaimer", value='true', max_age=365 * 24 * 60 * 60, expires=None, path='/', domain=None, secure=None, httponly=False)
        response = HttpResponse()
        content = 'Testing cookie serialization.'
        response.content = content
        response.set_cookie('agree2disclaimer', 'true')
        
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
    else: #get to load the login page
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        agree2disclaimer = request.COOKIES.get('agree2disclaimer') 
        return render(request, 'login.html', {'agree2disclaimer':agree2disclaimer})
    
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/auth/home/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
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

    print 'ProjectForm=', form
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
    print 'get_activity(()'
    
    util = Utility()
    user_list = util.viewable_user_list(request)
    
    allUserId_list = user_list['allUserId_list']
    allUser_list = user_list['allUser_list']
    allUserId_dict = user_list['allUserId_dict']
    print 'allUserId_dict[', allUserId_dict

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
        currentUser = None
        if uid == None or uid == '---': # investor self look up 
            userId = request.user.id
            uid = userId
            if orderBy == 'NONE':
                activity_list = InvestmentActivity.objects.filter(UserId = userId)
            else :
                activity_list = InvestmentActivity.objects.filter(UserId = userId).order_by(orderBy)
            
            #userName = User.objects.filter(id = uid).values_list('first_name', 'last_name')
            currentUser=allUserId_dict[int(uid)]
        elif uid == 'ALL'  and (user.is_staff or user.is_superuser) : # fetch all records the current user is allowed to view
            if orderBy == 'NONE':
                activity_list = InvestmentActivity.objects.all().filter(UserId__in=allUserId_list)
            else:
                activity_list = InvestmentActivity.objects.all().filter(UserId__in=allUserId_list).order_by(orderBy)
            userName = [(u'ALL', u'USERS')]
        else:
            currentUser=allUserId_dict[int(uid)]
            #userName = User.objects.filter(id = uid).values_list('first_name', 'last_name')
            
            if orderBy == 'NONE':
                activity_list = InvestmentActivity.objects.select_related('ProjectId__Status').filter(UserId = uid)
            else:
                activity_list = InvestmentActivity.objects.select_related('ProjectId__Status').filter(UserId = uid).order_by(orderBy)
        
        if currentUser != None  :  
            fname = allUserId_dict[int(uid)]['first_name']
            lname = allUserId_dict[int(uid)]['last_name']
            userName = fname + ' ' + lname
            
        sess[sess_userId_label] = uid
            
        print 'get_activity() user name=', userName
        total = 0.0
        total_principal = 0.0
        total_distribution = 0.0
        total_interest = 0.0
        total_dividend = 0.0
        
        for item in activity_list:
            if (item.Type_id == 'Deposit'):
                total_principal += item.Amount
            elif (item.Type_id == 'Check'):
                total_distribution += item.Amount
            elif (item.Type_id == 'Interest'):
                total_interest += item.Amount
            elif (item.Type_id == 'Dividend'):
                total_dividend += item.Amount
                
        
        total =  total_principal + total_distribution
        
        activity_dict= {'activities': activity_list, 'total_amount': total, 'total_distribution':total_distribution, 'total_principal':total_principal,
                        'total_interest':total_interest, 'total_dividend':total_dividend, 'allUser_list':allUser_list, 'investorId':uid, 'investorName':userName}
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

class ActivityList(ListView):
    template_name = "activity.html"
    #paginate_by = 10
    print 'ActivityList'
    
    def get_queryset(self):
        return InvestmentActivity.objects.filter(UserId = self.request.user)
################## for updating userProfile
@login_required
@csrf_exempt
def get_userProfile(request, form=None, id=None):
    user = request.user
    myUserId = user.id
            
    if request.method == 'POST' and (user.is_staff or user.is_superuser): #check security
        myUserId = request.POST.get('investorId')
    print 'request.method[', request.method , '] myUserId=[', myUserId

    if request.method == 'POST' and id is not  None:
        myUserId = id

    print 'get_userProfile() myUserId=[', myUserId, '] form is None:', form is None

    profileInfo = UserProfile.objects.filter(UserId = myUserId )
    
    if profileInfo.count() > 0:
        profileInfo = UserProfile.objects.get(pk=myUserId)
    else:
        profileInfo = None
        
    #print 'profileInfo=', profileInfo
    
    if form is None:
        if profileInfo is None:
            form = UserProfileForm(initial={'UserId_id': myUserId, 'UserId': myUserId})
            dbOperation = 'Create'
        else:
            form = UserProfileForm(instance=profileInfo)
            dbOperation = 'Update'
    else: #previous submission error?
        if profileInfo is None:
            dbOperation = 'Create'
        else:
            dbOperation = 'Update'
        
    #print 'UserProfileForm=', form
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    user_list = Utility().viewable_user_list(request)
    allUser_list = user_list['allUser_list']
    allUserId_dict = user_list['allUserId_dict']
    
    currentUser = None
    userName = None
    #print 'allUserId_dict=[', allUserId_dict
    
    if myUserId == 'ALL'  and (user.is_staff or user.is_superuser) : # fetch all records the current user is allowed to view
        userName = [(u'ALL', u'USERS')]
    else:
        currentUser=allUserId_dict[int(myUserId)]
            
    if currentUser != None  :  
        fname = allUserId_dict[int(myUserId)]['first_name']
        lname = allUserId_dict[int(myUserId)]['last_name']
        userName = fname + ' ' + lname
        
    fieldsetsPersonalInfo = (FieldSet(form, ('UserId', 'Address1','Address2','City', 'State', 'ZipCode', 'Telephone', 'Cell'),
                        legend='Personal Info.',
                        styleClass="form_name_info"), )
            
    fieldsetsOthers = (FieldSet(form, ('minCommitment', 'maxCommitment', 'lastCommitmentDate', 'W9Ready','website', ), 
                        legend="Other Info.",
                        styleClass="form_name_info"),)

    fieldsetsBank1 = (FieldSet(form, ('bank1Name','bank1UserName', 'bank1Rounting', 'bank1AccountNumber'), 
                        legend="Bank1 Instructions", styleClass="form_name_info"), )
    fieldsetsBank2 = (FieldSet(form, ('bank2Name','bank2UserName', 'bank2Rounting', 'bank2AccountNumber'), 
                        legend="Bank2 Instructions",  styleClass="form_name_info"), )
    fieldsetsBank3 = (FieldSet(form, ('bank3Name','bank3UserName', 'bank3Rounting', 'bank3AccountNumber'), 
                        legend="Bank3 Instructions", styleClass="form_name_info"), )
    
    #print 'user.id - myUserId', user.id, '-', myUserId, 'same user? [', (user.id == myUserId), ' > ', user.id >  myUserId, ' <= ', user.id <= myUserId
    return render(request, 'userProfile.html', 
                  {'myUserId':myUserId, 'investorName':userName, 'investorId':myUserId, 'dbOperation':dbOperation, 'allUser_list':allUser_list, 
                    'form': form, 'fieldsetsPersonalInfo': fieldsetsPersonalInfo, 'fieldsetsOthers':fieldsetsOthers, 
                    'fieldsetsBank1':fieldsetsBank1, 'fieldsetsBank2':fieldsetsBank2, 'fieldsetsBank3':fieldsetsBank3})
    #return render(request, 'userProfile.html', userProfile_dict)

@login_required
def  save_userProfile(request, id=None):
    user = request.user
    myUserId = user.id
    
    print 'save_userProfile  for uid=[', id
    if id == None:
        print 'create'
        form = UserProfileForm(request.POST, request.FILES)
    else: # fraud detection
        if user.is_staff or user.is_superuser:
        #form = ProjectForm(request.POST, instance=project)
            print 'super user updating regular user'
        elif id is not None and myUserId != id :
            print 'prevent [', user.id, '] fake super user updating regular user'
            return get_userProfile(request, None, user.id)
        
        object_to_edit = get_object_or_404(UserProfile, UserId=id) #Or slug=slug
        print 'Found object_to_edit[{}]'.format(object_to_edit)
        form = UserProfileForm(data = request.POST or None, instance=object_to_edit)
        

    #print 'UserProfileForm=', form
    print 'before committing request.method=[', request.method , "] validation=[", form.is_valid()
    # Have we been provided with a valid form?
    form.fields['UserId'].required = False
    if form.is_valid():
        # Save the new project to the database.
        print 'committing'
        form.save(commit=True)
    else:
        # The supplied form contained errors - just print them to the terminal.
        print form.errors
        return get_userProfile(request, form)
        #return render(request, 'userProfile.html', {'myUserId':myUserId,  'form': form})

    print 'after committing'
    return get_userProfile(request, form, id)

@login_required
def change_password(request):
    return render(request, 'passwordUpdate.html')
@login_required
def  save_password(request):
    user = request.user
    myUserId = user.id
    error_msg = None

    if request.method == 'POST':
        oldPassword = request.POST['oldPassword'].strip()
        newPassword1 = request.POST.get('newPassword1')
        newPassword2 = request.POST.get('newPassword2')
        
        print oldPassword, newPassword1, newPassword2
        
        saveuser = User.objects.get(id=myUserId)
        if user.check_password(oldPassword):
            saveuser.set_password(newPassword1);
            saveuser.save()
        else:
            error_msg ='The old password doesn\'t match. Try again!'
            print error_msg

    return render(request, 'passwordUpdate.html', {"error_msg": error_msg})

@login_required
def get_announcement(request):
    msgs=None
    #only query latest 3 messages
    queryset = Announcement.objects.filter(ExpireOn__gte= date.today()).order_by('-ExpireOn')[:3]
    print "announcement[", queryset
    
    return render(request, "announcement.html", {"messages":queryset})
########################################################################
# index.html
def index(request):
    return render(request, 'index.html')
# about-us.html
def aboutUs(request):
    return render(request, 'about-us.html')
# contact-us.html
def contactUs(request):
    return render(request, 'contact-us.html')

def disclaimer(request):
    return render(request, "disclaimer.html")

def get_ourProjects(request):
    return render(request, "ourProjects.html")

###
class OverallProjectsListView(ListView):
    model = PROJECT
    template_name = "overallProjects.html"
    paginate_by = 10
    print 'OverallProjectsListView'

