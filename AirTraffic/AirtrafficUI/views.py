# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import   User
from django.db.models import Q
from datetime import date
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
    print "showRoutes at ", date.today()
    
    qname = Q() 
    qname &= Q(date__gte = (str(date.today()) + "T00:00:00Z"))
    qname &=  Q(altitude__gte =50)
    flight_list = positionJSONHistory.objects.all().filter(qname).order_by('ICAO','id')
    print len(flight_list)
    
    flightDictionary ={}
    singleFlightDataList=[]
    counter = 0
    icao = ""
    for flight in flight_list:
        if icao != flight.ICAO:
            print flight.ICAO, flight.Flight, flight.date, flight.altitude, flight.latitude, flight.longititude
            icao = flight.ICAO
            counter+=1
            print counter
            singleFlightDataList=[]

        #if counter > 250:
            #break;

        singleFlightDataList.append({"id":flight.id, "ICAO":flight.ICAO, "Flight":flight.Flight, "Date":flight.date, "alt":flight.altitude, "lat":flight.latitude, "lon":flight.longititude} )
        flightDictionary[flight.ICAO] = singleFlightDataList


    #print 'flightDictionary=[', flightDictionary
    return JsonResponse(flightDictionary.items(), safe=False)
    #return JsonResponse(serializers.serialize("json",flightDictionary),safe=False  )

def showRoutes(request):
    return render(request, 'showGMaps.html',{})
    
# BLUE, 7000-8000
# cyan, 6000-6999
# yellow, 5000-5999
# orange, 4000-4999
# chocolate, 3000-3999
# red/crimson/magenta,2000-2999
# brown, 1000-1999
# black, 50 - 999

