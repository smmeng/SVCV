from datetime import datetime,date
from django.utils.timezone import get_current_timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, render, HttpResponse
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
    oldOrderBy=""
    template_name = "webapp/visitorLog_list.html"
    paginate_by = 10
    print 'Calling visitorLog ListView()  '
  
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        print 'Calling ListView().get() self.object_list=[%s]'%( self.object_list.count())
        request.session["visitorLog"] = self.object_list.values_list('Type', 'fname', 'lname', 'email', 'phone', 'employeeId','Comments', 'CreatedOn')
        print "ListView().get()  request.session['visitorLog']=", request.session, ' type=', type(request.session["visitorLog"])
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)
        
    def get_queryset(self):
        queryset = super(visitorLogListView, self).get_queryset()
        print 'Calling visitorLog ListView().get_queryset()  current_orderby[' ,
        print self.oldOrderBy

        orderBy = self.request.GET.get('orderBy')
        
        firstDate = self.request.GET.get('firstDate')
        lastDate = self.request.GET.get('lastDate')
            
        print 'input param orderBy=[%s], fdate=[%s], ldate=[%s]'%(orderBy, firstDate, lastDate)
        
        if orderBy is not None:
            return queryset.order_by(orderBy)
        return queryset
    
class visitorLogFilteredListView(ListView):
    print 'entering visitorLogFiltered ListView'
    model = visitorLog
    oldOrderBy=""
    template_name = "webapp/visitorLog_list.html"
    paginate_by = 10
    print 'Calling visitorLogFiltered ListView()  '
    
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        #form_class = self.get_form_class()
        #self.form = self.get_form(form_class)

        # From BaseListView
        
        self.object_list = self.get_queryset()
        print 'Calling Filtered ListView().get() self.object_list=[%s]'%( self.object_list.count())
        request.session["visitorLog"] = self.get_queryset().values_list('Type', 'fname', 'lname', 'email', 'phone', 'employeeId','Comments', 'CreatedOn')
        print " Filtered ListView().get()  request.session['visitorLog'] type=", type(request.session["visitorLog"])
        
        allow_empty = self.get_allow_empty()
        #if not allow_empty and len(self.object_list) == 0:
        #    raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
        #                  % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        firstDate = self.request.POST.get('firstDate')
        lastDate = self.request.POST.get('lastDate')
        tz = get_current_timezone()
        
        fDate= tz.localize(datetime.strptime(firstDate, "%Y-%m-%d %H:%M:%S") )
        lDate= tz.localize(datetime.strptime(lastDate, "%Y-%m-%d %H:%M:%S") )
        print 'Calling Filtered ListView().post() fdate=[%s], ldate=[%s]'%( fDate, lDate)

        qs=self.get_queryset()
        print([r.CreatedOn for r in qs])

        for row in qs:
            rdate= tz.localize(row.CreatedOn)
            print fDate, rdate, lDate, "result: ", fDate < rdate, rdate <lDate
            
        #qs.filter(CreatedOn__range=(fDate, lDate))
        qs=self.get_queryset()
        print([r.CreatedOn for r in qs])
        
        print "after filter, qs count = ", qs.count()
        return self.get(request, *args, **kwargs)
   
    def get_queryset(self):
        queryset = super(visitorLogFilteredListView, self).get_queryset()
        print 'Calling Filtered ListView().get_queryset()  current_orderby[' ,
        firstDate = self.request.POST.get('firstDate')
        lastDate = self.request.POST.get('lastDate')
        tz = get_current_timezone()
        
        fDate= tz.localize(datetime.strptime(firstDate, "%Y-%m-%d %H:%M:%S") )
        lDate= tz.localize(datetime.strptime(lastDate, "%Y-%m-%d %H:%M:%S") )
        #print 'get_queryset() Calling Filtered ListView().get_queryset() fdate=[%s], ldate=[%s]'%( fDate, lDate)

        qs=queryset.filter(CreatedOn__range=(fDate, lDate))
                    
        print 'get_queryset() input param ,  final row count=%d'%(   qs.count())
        
        return qs

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
    
############################# Export the queryset to excel   
import xlwt
def create_excel(request):
    visitorLog = request.session["visitorLog"]
    print "In create_excel() ", type(visitorLog)
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('visitorLog')

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='YYYY-MM-DD hh:mm')
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

    headers = ['Type', 'First Name', 'Last Name', 'Email', 'Phone', 'Destinations','Comments', 'Created On']
    
    values_list = [headers] + list(visitorLog)

    for row, rowdata in enumerate(values_list):
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                style = datetime_style
            elif isinstance(val, date):
                style = date_style
            else:
                style = default_style
            sheet.write(row, col, val, style=style)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=example.xls'
    book.save(response)
    return response