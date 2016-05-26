from django.shortcuts import render
from models  import vistorType
# Create your views here.

from mongogeneric import ListView, CreateView, DetailView, UpdateView
from mongoengine.queryset import queryset

###
class visitorTypeListView(ListView):
    print 'entering visitorTypeListView'
    model = vistorType
    #queryset = vistorType.objects
    context_object_name = "vistorType_list"
    document = vistorType
    template_name = "visitorList.html"
    #paginate_by = 10
    print 'CallingvisitorTypeListView() [', queryset

    #def get_queryset(self):
    #    return vistorType.objects