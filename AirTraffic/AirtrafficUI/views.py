# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import   User
from django.db.models import Q
from datetime import date, datetime
import pytz
import json
from django.http import JsonResponse
from django.core import serializers

#from django.views.generic import   ListView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.core.mail import EmailMessage
from models import *
from django.db.models import Q

flightDetailURL="https://flightaware.com/live/flight/" 
weatherRESTws= "https://home.openweathermap.org/api_keys" #key=649dad5b960b03ef0403da84b1a2c9a8

#@login_required
def showRouteData(request):
    #today =  str(datetime.now(pytz.timezone('US/Pacific')))[0:10] 
    tday =  datetime.now(pytz.timezone('US/Pacific'))
    print "showRouteData at ",pytz.timezone('US/Pacific'), ",today[", tday, "]"
 
    qname = Q() 
    #qname &= Q(date__gte = (str(date.today()) + "T00:00:00Z"))
    qname &= Q(date__year =  tday.year)
    qname &= Q(date__month=  tday.month)
    qname &= Q(date__day=  tday.day)
    #qname &= Q(date__date= datetime.now(pytz.timezone('US/Pacific')).date())
    qname &=  Q(altitude__gte =50)
    qname &=  Q(altitude__lte =2000)
    flight_list = positionJSONHistory.objects.filter(qname).values_list('ICAO', 'Flight', 'date', 'altitude', 'latitude', 'longititude', 'speed').order_by('ICAO','id')
    print len(flight_list), datetime.now(pytz.timezone('US/Pacific')).date()
    
    flightDictionary ={}
    singleFlightDataList=[]
    counter = 0
    icao = ""
    for flightTuple in flight_list:
        flight = {}
        flight['ICAO']=flightTuple[0]
        flight['Flight']=flightTuple[1]
        flight['date']=flightTuple[2]
        flight['altitude']=flightTuple[3]
        flight['latitude']=flightTuple[4]
        flight['longititude']=flightTuple[5]
        flight['speed']=flightTuple[6]
        #flight['']=flightTuple[]
        #print flight
                
        if icao != flight['ICAO']:
            icao = flight['ICAO']
            counter+=1
            #print flight['ICAO'], flight['Flight'], flight['date'], flight['altitude'], flight['latitude'], flight['longititude']
            singleFlightDataList=[]

        if (counter %100==0):
            print flight['ICAO'], flight['Flight'], flight['date'], flight['altitude'], flight['latitude'], flight['longititude']

        if  flight['altitude'] > 5000:
            print flight['ICAO'], flight['Flight'], flight['date'], flight['altitude'], flight['latitude'], flight['longititude']
            #break;

        singleFlightDataList.append({ "ICAO":flight['ICAO'], "Flight":flight['Flight'], "Date":flight['date'], "alt":flight['altitude'], "lat":flight['latitude'], "lon":flight['longititude']} )
        flightDictionary[flight['ICAO']] = singleFlightDataList


    #print 'flightDictionary=[', flightDictionary
    return JsonResponse(flightDictionary.items(), safe=False)
    #return JsonResponse(serializers.serialize("json",flightDictionary),safe=False  )

def showRoutes(request):
    return render(request, 'showGMaps.html',{})
    
def showRoutes0(request):
    return render(request, 'showGMaps0.html',{})
    
# BLUE, 7000-8000
# cyan, 6000-6999
# yellow, 5000-5999
# orange, 4000-4999
# chocolate, 3000-3999
# red/crimson/magenta,2000-2999
# brown, 1000-1999
# black, 50 - 999

