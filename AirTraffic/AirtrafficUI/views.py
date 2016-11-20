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
timeZone = 'US/Pacific'
minAlt = 100
maxAlt = 4000
datefilter=None
#@login_required
def showRouteData(request):
    #today =  str(datetime.now(pytz.timezone(timeZone)))[0:10] 
    tday =  datetime.now(pytz.timezone(timeZone))
    print "showRouteData() at ",pytz.timezone(timeZone), ",today[", tday, "] request.method=", request.method
    print "datefilter=[", request.session.get('datefilter'), "] minAlt=", request.session.get('minAlt', minAlt), " maxAlt=", request.session.get('maxAlt', maxAlt)
 
    if (request.session.get('datefilter') != None):
        firstDate = convert2DateTime(request.session.get('datefilter')[0:20])
        nextDate = convert2DateTime(request.session.get('datefilter')[22:42])
        
    qname = Q() 
    if (firstDate != None):
        qname &= Q(date__range = (firstDate, nextDate))
        #qname &= Q(date__lte = nextDate)
        
    #qname &= Q(date__year =  tday.year)
    #qname &= Q(date__month=  tday.month)
    #qname &= Q(date__day=  tday.day)
    ####qname &= Q(ICAO = 'c01c02')
    qname &=  Q(altitude__gte = request.session.get('minAlt', minAlt) )
    qname &=  Q(altitude__lte = request.session.get('maxAlt', maxAlt) )
    flight_list = positionJSONHistory.objects.filter(qname).values_list('ICAO', 'Flight', 'date', 'altitude', 'latitude', 'longititude', 'speed').order_by('ICAO','id')
    print len(flight_list), datetime.now(pytz.timezone(timeZone)).date()
    
    flightDictionary ={}
    singleFlightDataList=[]
    counter = 0
    icao = ""
    skipICAO=""     # skip ICAO if it's taking off
    oldAlt=99999    # initial starts at high altitude
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
                
        if icao != flight['ICAO']: # new ICAO found??
            icao = flight['ICAO']
            counter+=1
            #print flight['ICAO'], flight['Flight'], flight['date'], flight['altitude'], flight['latitude'], flight['longititude']
            singleFlightDataList=[]
            skipICAO=flight['ICAO']
            oldAlt = flight['altitude']
            
        if (flight['ICAO'] == skipICAO and flight['altitude'] > oldAlt):
            flightDictionary.pop(skipICAO, None)
            oldAlt = flight['altitude']
            #print 'Skipping ascending flight [', flight
            continue;
        #else:
            #print flight

        if (counter %10==0):
            print flight['ICAO'], flight['Flight'], flight['date'], flight['altitude'], flight['latitude'], flight['longititude']

        #if (counter >50):
            #break;
        
        #if  flight['altitude'] > 5000:
            #print flight['ICAO'], flight['Flight'], flight['date'], flight['altitude'], flight['latitude'], flight['longititude']
           

        singleFlightDataList.append({ "Flight":flight['Flight'], "Date":flight['date'], "alt":flight['altitude'], "lat":flight['latitude'], "lon":flight['longititude']} )
        flightDictionary[flight['ICAO']] = singleFlightDataList


    #print 'flightDictionary=[', flightDictionary
    return JsonResponse(flightDictionary.items(), safe=False)
    #return JsonResponse(serializers.serialize("json",flightDictionary),safe=False  )
def convert2DateTime(str):
    local_tz = pytz.timezone(timeZone)
    dateStr = str.split("/")
    monthStr =dateStr[0]
    dtStr =dateStr[1]
    year=dateStr[2]
    #print 'Date =[', dtStr, "]-[",monthStr, "]-[",year, "]"
    
    timeStr=year[5:].split(":")
    yearStr=year[0:4]
    #print 'year =[', yearStr, "]-time=[", timeStr
    
    hourStr= timeStr[0]
    if (timeStr[1].count("PM")>0):
        hr = int(timeStr[0])+12
        print hr
        hourStr = '%2d'%hr
    

    #print 'Date str=[', str, "]-[", (str[0:1]+ str[3:4]+ str[5:8]+ "T"+ str[9:10]+ str[11:12]+"00") +"]"
    #finalDate= datetime(int(yearStr), int(monthStr), int(dtStr), int(timeStr[0]), int(timeStr[1][0:1]), 0)
    finalDate=datetime.strptime(yearStr + "-" + monthStr + "-" + dtStr +" " + hourStr + ":" + timeStr[1][0:2]+ ":00", "%Y-%m-%d %H:%M:%S")
    finalDateStr=yearStr + "-" + monthStr + "-" + dtStr +"T" + hourStr + ":" + timeStr[1][0:2]+ ":00Z"
    datetime_with_tz = local_tz.localize(finalDate, is_dst=None) # No daylight saving time
    print 'finalDate=[', finalDateStr, "] Add TZ=[", datetime_with_tz, "] for TZ[", local_tz
    return finalDateStr
    #return datetime_with_tz

def showRoutes(request):
    if request.method == 'POST':
        datefilter = request.POST.get('datefilter')
        request.session['datefilter'] = datefilter
        minAlt = request.POST.get('minAlt')
        maxAlt = request.POST.get('maxAlt')
        request.session['minAlt'] = minAlt
        request.session['maxAlt'] = maxAlt
        
        print "in showRoutes() POST recvd with datefilter=[", datefilter, "] minAlt=", minAlt, " maxAlt=", maxAlt
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

