from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from webapp.models import vistorType, visitorLog, employee
from webapp.forms  import visitorLogForm

# Create your views here.    
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

#############
#############
#############    
def index(request):
    return render_to_response('index.html')    

def adminView(request):
    return render_to_response('adminIndex.html')

def contactUs(request):
    return render_to_response('contact.html')    
    
def aboutUs(request):
    return render_to_response('about.html')    
######
    #def get_queryset(self):
    #    return vistorType.objects
class visitorTypeUpdateView(UpdateView):
    print 'entering svistorType update'
    model = vistorType
    template_name = "webapp/vistortype_detail.html"
    fields = ['Type', 'Description', 'Comments']
    print 'vistorType update'
    success_url = '/visitorType/'

class visitorTypeCreateView(CreateView):
    print 'entering svistorType create'
    model = vistorType
    template_name = "webapp/vistortype_detail.html"
    fields = ['Type', 'Description']
    print 'vistorType create'
    success_url = '/visitorType/'

class visitorTypeDeleteView(DeleteView):
    print 'entering svistorType create'
    model = vistorType
    template_name = "webapp/vistortype_detail.html"
    fields = ['Type', 'Description']
    print 'vistorType delete'
    success_url = '/visitorType/'

##################################### visitorLog
    
class visitorLogListView(ListView):
    print 'entering visitorLog ListView'
    model = visitorLog
    
    template_name = "webapp/visitorLog_list.html"
    paginate_by = 10
    print 'Calling visitorLog ListView()  ['

class visitorLogUpdateView(UpdateView):
    print 'entering visitorLog update'
    model = visitorLog
    template_name = "webapp/visitorLog_detail.html"
    form_class = visitorLogForm
    #fields = ['id','Type', 'fname', 'lname', 'email', 'phone', 'employeeId', 'Comments','CreatedOn']
    print 'visitorLog update'
    success_url = '/visitorLog/'

class visitorLogCreateView(CreateView):
    print 'entering visitorLog create'
    model = visitorLog
    template_name = "webapp/visitorLog_detail.html"
    form_class = visitorLogForm
    #fields = ['id','Type', 'fname', 'lname', 'email', 'phone', 'employeeId', 'Comments','CreatedOn']
    print 'visitorLog create'
    success_url = '/visitorLog/add/'

 
##################################### employee
class employeeUpdateView(UpdateView):
    print 'entering employee update'
    model = employee
    template_name = "webapp/employee_detail.html"
    fields = ['employeeName']
    print 'employee update2'
    #success_url = '/employee/'
    
    def get_success_url(self):
        return '/employee/'

class employeeCreateView(CreateView):
    print 'entering employee create'
    model = employee
    template_name = "webapp/employee_detail.html"
    fields = ['employeeId','employeeName']
    print 'employee CreateView2'
    success_url = '/employee/'
    
    def form_valid(self, form):
        print '1 employee CreateView.form_valid()', form.instance
        return super(employeeCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print '2 employee CreateView.form_invalid()', form.instance
        return super(employeeCreateView, self).form_invalid(form)   
    
    def get_form(self, form_class):
        form = super(employeeCreateView, self).get_form(form_class)
        print 'employee CreateView.get_form() form_class=',form_class
        #print 'employee CreateView.post(), form=', form
        #course = get_object_or_404(Class, pk=self.kwargs['employeeId'])
        form.instance.employeeId = employee.objects.count() + 1
        print 'employee CreateView.get_form() employeeId', form.instance.employeeId 
        return form
'''


    @classmethod
    def create(cls, employeeId, employeeName):
        newEmpId = employee.objects.count() + 1
        print "In employee.create() newEmpId=", newEmpId
        emp = cls(employeeId= newEmpId, employeeName=employeeName)
        return emp
'''