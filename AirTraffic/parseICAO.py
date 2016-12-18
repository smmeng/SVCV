import sys, traceback
import urllib                   #https://docs.python.org/2/library/urllib.html
from bs4 import BeautifulSoup   #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree, 
from pip._vendor.requests import structures
                                #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
import MySQLdb

from calculateDistance import *
from mySendmail import sendMail
from parseLib import *

from datetime import date, datetime
import time
import pytz
import calculateDistance

timeZone = 'US/Pacific'
minAlt = 100
maxAlt = 4500
interval = 60 #seconds

maxTolerantDistance = 5 # miles

def findNewICAOs4Today():
    flightSql = ""
    sql = ""
    icaoDict = {}
    #MySQL lookup & update
    '''
    tday =  datetime.now(pytz.timezone(timeZone))
    dateStr = "%s-%02d-%02d"%(tday.year, tday.month,tday.day)
    print "dateStr=[",dateStr, "(%f,%f)"%( calculateDistance.origLat,calculateDistance.origLong)
    sql="SELECT icao,  max(date) datetm, min(altitude) alt, avg(latitude) lat, avg(longititude) lon, avg(speed) speed, flight "\
            "FROM AirTraffic.AirtrafficUI_positionjsonhistory "\
            "WHERE date LIKE '" + dateStr + "%' and altitude > " + str(minAlt) + " and altitude < " + str(maxAlt) + " "\
                " AND icao NOT IN (SELECT distinct icao "\
                                    "FROM AirTraffic.AirtrafficUI_flights "\
                                    "WHERE date LIKE '" + dateStr + "%') "\
            "GROUP BY icao "\
            "ORDER BY  datetm  DESC; "
    '''
        # Or don't use GROUP BY, scan all coordinates for a flight to see if it's over our head. radius of 3 miles
        # library: https://pypi.python.org/pypi/geopy/1.11.0
    
    # http://www.mysqltutorial.org/python-mysql-query/
    db = None
    cursor = None
    
    try:        
        while True:
            tday =  datetime.now(pytz.timezone(timeZone))
            dateStr = "%s-%02d-%02d"%(tday.year, tday.month,tday.day)
            #print "dateStr=[",dateStr, "(%f,%f)"%( calculateDistance.origLat,calculateDistance.origLong)
            sql = "SELECT distinct icao, flight "\
                    "FROM AirTraffic.AirtrafficUI_positionjsonhistory "\
                    "WHERE date LIKE '" + dateStr + "%'  "\
                    "and altitude > " + str(minAlt) + " and altitude < " + str(maxAlt) + " "\
                    "AND icao NOT IN  "\
                    "(SELECT distinct icao "\
                    "FROM AirTraffic.AirtrafficUI_flights WHERE date LIKE  '" + dateStr + "%') ORDER BY icao; " 
            #print sql

            db = MySQLdb.connect("lab2.svcvllc.com","httpuser","Save3ySky","AirTraffic" )
            #db = MySQLdb.connect("localhost","httpuser","Save3ySky","AirTraffic" )
            
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            
            cursor.execute(sql)
            print "EXE main sql=[", sql
            rows = cursor.fetchall()
     
            print('findNewICAOs4Today() Total New ICAO Row(s):', cursor.rowcount)
            noneCounter = 0
            for row in rows:
                newIcao=row[0]
                #datetm=row[1]
                flightNo = row[1]
                print "\n new ICAO=[", newIcao, "] flight=[",flightNo, "] counter=", noneCounter
                if (flightNo is not None and str(flightNo)!= 'null'):
                    flightDict = lookupFlightNoVer2(flightNo.rstrip())
                    icaoDict[newIcao] = flightNo
                    
                    updateICAOmap(db, cursor, newIcao, flightNo) #update the mapping table for this icao
                else:
                    flightNo = icaoDict.get(newIcao, "null")
                    print 'icaoDict[newIcao]=',flightNo
                    if (flightNo is not None and flightNo != "null"):
                        continue    # skip this because I just processed it
                    
                    flightDict = lookupICAO(newIcao)
                    if (flightDict is not None and flightDict['flightNo'] is not None):
                        updateICAOmap(db, cursor, newIcao, flightNo) #update the mapping table for this icao
                    else: # Finally we must look up the flight # from the mapping table
                        sqlJoinMap = "SELECT TailPin FROM AirTraffic.ICAOmap "\
                            "WHERE icao = '"+ newIcao+"';"
                        
                        cursor.execute(sqlJoinMap)
                        mapRows = cursor.fetchall()
    
                        if (len(mapRows)==1):
                            TailPin = mapRows[0][0]
                            print "In ICAOmap, icao=[", newIcao, "] TailPin=[", TailPin
                            flightDict = lookupFlightNoVer2(TailPin.rstrip())
                            #print "In ICAOmap, flightDict=[",flightDict
                            
                    #time.sleep(interval*10)
                if (flightDict is None or bool(flightDict) == False):
                    noneCounter +=1
                    #print noneCounter, flightDict
                else:
                    noneCounter =0 #reset the counter
                    print noneCounter, flightDict
                    coordinate = isInsideMaxTolerantDistance(cursor, newIcao, dateStr)
                    
                    if coordinate is not None: #insert the flight info to flights table
                        try:
                            flightSql = "INSERT INTO AirtrafficUI_flights VALUES(null,'" + newIcao + "', '" + flightDict['flightNo'] + "', " \
                                        " '" + str(coordinate['date']) + "', " + str(coordinate['alt']) + ", " + str(coordinate['lat']) + ", " + \
                                        str(coordinate['long']) + ", '" +  flightDict['aircraft'] + "', '" + flightDict['origAirport'] + "', '" + \
                                        flightDict['destAirport'] + "', " + str(coordinate['speed']) + ");"
                            
                            print "INSERTing flightSql=[" , flightSql
                            # Commit your changes in the database
                            cursor.execute(flightSql)
                            db.commit()
                        except :
                            print "findNewICAOs4Today() Something is wrong Insert=[",  flightSql
                            ex = traceback.print_stack()
                            print ex
                            sendMail("findNewICAOs4Today() Failed Insert=[", ex)
                            db.rollback()


                if (noneCounter > 50):
                    #stop processing obsolete ICAO further
                    break;
            
            if cursor is not None:
                cursor.close()
            if db is not None:
                db.close()
                
            print "Sleep ", interval*6, "\n\n\n"
            time.sleep(interval*6)
    
    except :
        print "findNewICAOs4Today() Something is wrong sql=[", sql
        ex = traceback.print_stack()
        print ex
        sendMail("parseICAO Failed findNewICAOs4Today()", ex)
        db.rollback()
        traceback.print_exc(file=sys.stdout)
    
    if cursor is not None:
        cursor.close()
    if db is not None:
        db.close()
    
    return None

    
    
findNewICAOs4Today()

