from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

from django.shortcuts import render
from models  import vistorType
# Create your views here.

from mongogeneric import ListView, CreateView, DetailView, UpdateView
from mongoengine import queryset
    
def index(request):
    return render_to_response('index.html')    
###
class visitorTypeListView(ListView):
    print 'entering visitorTypeListView'
    #model = vistorType
    queryset = vistorType.objects
    #context_object_name = "vistorType_list"
    #document = vistorType.objects
    template_name = "visitorList.html"
    #paginate_by = 10
    print 'CallingvisitorTypeListView()  ['

    #def get_queryset(self):
    #    return vistorType.objects


def visitorTypeForm(request):
    print 'entering visitorTypeForm'
    '''
    if request.method == 'POST':
       # save new post
       type = request.POST['Type']
       description = request.POST['Description']

       visitorType = vistorType( )
       visitorType.Type = type
       visitorType.Description = description
       visitorType.save()
'''
    # Get all posts from DB
    vType = vistorType()
    vType.Type="Employee2"
    vType.Description="Company Employees"
    vType.save(force_insert=True)
    print 'visitorType=  [', vType
    return render_to_response('webapp/vistortype_detail.html', {'visitorType': vType},
                              context_instance=RequestContext(request))
