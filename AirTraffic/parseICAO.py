import sys, traceback
import urllib                   #https://docs.python.org/2/library/urllib.html
from bs4 import BeautifulSoup   #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree, 
from pip._vendor.requests import structures
                                #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
import MySQLdb

from calculateDistance import *
from mySendmail import sendMail

from datetime import date, datetime
import time
import pytz
import calculateDistance

timeZone = 'US/Pacific'
minAlt = 100
maxAlt = 4500
interval = 60 #seconds

maxTolerantDistance = 5 # miles

def removeHTMLTag(inputStr):
    if (inputStr is None):
        return None
    
    string = "%s"%(inputStr)
    leftIndex = string.find('>')
    #print "leftIndex=", string
    if leftIndex < 0:
        return inputStr
    
    result = string[(leftIndex+1):]   
    #print "result1=", result
    
    rightIndex = result.find("</")
    #print "rightIndex=", rightIndex
    if rightIndex > -1:
        result = result[0:rightIndex]
        
    #print "result2=", result
    return result

def extractHTMLTagAttribute(inputStr, attrName):
    if (inputStr is None or attrName is None):
        return None
    
    string = "%s"%(inputStr)
    leftIndex = string.find(attrName)
    #print "leftIndex=", leftIndex
    if leftIndex < 0:
        return inputStr
    
    result = string[(leftIndex+len(attrName)+2):]   
    #print "result1=", result
    
    rightIndex = result.find("\"")
    #print "rightIndex=", rightIndex
    result = result[0:rightIndex]
        
    #print "result2=", result
    return result

# Lookup the flight details based on the ICAO#:
def lookupICAO(icao):
    
    ICAOurl= "http://flightaware.com/live/modes/" + icao + "/redirect"
    flightDict={}
    
    try:
        opener = urllib.FancyURLopener({})
        f = opener.open(ICAOurl)
        
        html_doc = f.read()
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.title
        if (title is None):
            return None
    
        print "lookupICAO() ******:", title#, titleList
        
        body=soup.body
        table=body.contents[6].table
        #print table
        
        strongs = table.findAll("strong", { })
        flightNo = removeHTMLTag(strongs)
        #print "****** flightNo:", flightNo
    
        spans = table.findAll("span", { })
        flightName = removeHTMLTag(spans[0])
        #print "****** flightName", flightName
        
        spans = table.findAll("span", class_="hint")
        origAirport = extractHTMLTagAttribute(spans[0], "title")
        destAirport = extractHTMLTagAttribute(spans[1], "title")
        #print "****** origAirport:", origAirport.split()[-1]
        #print "****** destAirport:", destAirport.split()[-1]
        
        spans = table.findAll("span", class_="flightStatusGood")
        status = removeHTMLTag(spans[0])
        #print "****** status", status
        
        if (len(spans) > 1):
            onTime = removeHTMLTag(spans[1])
            flightDict['onTime']=onTime
            #print "****** onTime", onTime
        
        #divTracePanelCourse = soup.select("#polling-flight_status")
        #print divTracePanelCourse
        ths = table.findAll("th", class_="secondaryHeader")
        #for th in ths:
        #    print "****** th:", th, " next=[", th.next_sibling.next_sibling
        
        aircraft = ths[1].next_sibling.next_sibling
        aircraftName = aircraft.contents[0]
        aircraft = removeHTMLTag(aircraft.contents[1])
        #print "****** aircraftName:", aircraftName, "-", aircraft
        
        speed = removeHTMLTag(ths[2].next_sibling.next_sibling.contents[0])
        #print "****** speed:", speed
        altitude = removeHTMLTag(ths[3].next_sibling.next_sibling).split("feet")[0]
        #print "****** altitude:",altitude
        distance = removeHTMLTag(ths[4].next_sibling.next_sibling)
        #print "****** distance:",distance
        route = removeHTMLTag(ths[5].next_sibling.next_sibling)
        #print "****** route:", route
        
        flightDict['flightNo']=flightNo
        flightDict['flightName']=flightName
        flightDict['origAirport']=origAirport.split()[-1]
        flightDict['destAirport']=destAirport.split()[-1]
        flightDict['status']=status
        flightDict['aircraft']=aircraft
        flightDict['aircraftName']=aircraftName
        
        flightDict['speed']=speed.split()[0]
        flightDict['altitude']=altitude
        flightDict['distance']=distance
        flightDict['route']=route
        #flightDict['']=
    except:
        print "Something is wrong in parsing ICAO!"
        return None
    return flightDict

# 2nd approach with known flight#
def lookupFlightNo(flightNo):
    
    #ICAOurl= "http://flightaware.com/live/modes/" + icao + "/redirect"
    ICAOurl= "http://flightaware.com/live/flight/"+flightNo
    flightDict={}
    
    #store default values 
    flightDict['flightNo']= flightNo
    flightDict['flightName']=" "
    flightDict['origAirport']=" "
    flightDict['destAirport']=" "
    flightDict['onTime']=" "
    flightDict['status']=" "
    flightDict['aircraft']= " "
    flightDict['aircraftName']=" "
    flightDict['speed']=" "
    flightDict['altitude']=" "
    flightDict['distance']=" "
    flightDict['route']=" "
    
    try:
        opener = urllib.FancyURLopener({})
        f = opener.open(ICAOurl)
        
        html_doc = f.read()
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.title
        if (title is None):
            return None
    
        #print "******:", title#, titleList
        
        body=soup.body
        table= body.findAll("table", class_="track-panel-course")
        #print table, len(table)
        
        origAirportTD = table[0].findAll("td", class_="track-panel-departure")
        #print "origAirportTD=[", origAirportTD
        origAirportA = origAirportTD[0].findAll("a", { })
        #print "origAirportA=[", origAirportA
        origAirport = removeHTMLTag(origAirportA[0])
        #print "origAirport=[", origAirport

        destAirportTD = table[0].findAll("td", class_="track-panel-arrival")
        #print "destAirportTD=[", destAirportTD
        destAirportA = destAirportTD[0].findAll("a", { })
        #print "destAirportA=[", destAirportA
        destAirport = removeHTMLTag(destAirportA[0])
        #print "destAirport=[", destAirport
        
        flightDict['flightNo']=flightNo
        #flightDict['flightName']=flightName
        flightDict['origAirport']=origAirport
        flightDict['destAirport']=destAirport

        ths = body.findAll("th", class_="secondaryHeader")
        #print "How many secondaryHeader[", len(ths)
        spans = ths[0].next_sibling.next_sibling.findAll("span", class_="flightStatusGood")
        status = removeHTMLTag(spans[0])
        #print "****** status:", status, len(spans)
        
        if (len(spans) > 1):
            onTime = removeHTMLTag(spans[1])
            flightDict['onTime']=onTime
            #print "****** onTime", onTime
        
        aircraft = ths[1].next_sibling.next_sibling
        #print ths[1].next_sibling.next_sibling
        aircraftName = ths[1].next_sibling.next_sibling
        aircraft = aircraftName.findAll("a", {})
        aircraft = removeHTMLTag(aircraft[0])
        aircraftName = aircraftName.findAll("td", {})
        aircraftName = removeHTMLTag(aircraftName[0])
        #print "****** aircraftName:", aircraftName, "-", aircraft
        #print "****** aircraft:", aircraft
        flightDict['status']=status
        flightDict['aircraft']=aircraft
        flightDict['aircraftName']=aircraftName
        
        speed = ths[2].next_sibling.next_sibling
        speed = speed.findAll("span", {})
        speed = removeHTMLTag(speed[0])
        #print "****** speed:", speed
        flightDict['speed']=speed.split()[0]
        
        altitude = removeHTMLTag(ths[3].next_sibling.next_sibling)
        #print "****** altitude:",altitude
        flightDict['altitude']=altitude
        
        distance = removeHTMLTag(ths[4].next_sibling.next_sibling)
        #print "****** distance:",distance
        flightDict['distance']=distance
        
        route = removeHTMLTag(ths[5].next_sibling.next_sibling)
        #print "****** route:", route
        flightDict['route']=route

        #flightDict['']=
    except:
        print "Something is wrong in parsing Flight !"
    return flightDict

def isInsideMaxTolerantDistance(cursor, icao, dateStr):
    
    sql="SELECT icao,  date, altitude, latitude, longititude, speed "\
            "FROM AirTraffic.AirtrafficUI_positionjsonhistory "\
            "WHERE icao='" + icao + "' AND date LIKE '" + dateStr + "%' AND altitude > " + str(minAlt) + " and altitude < " + str(maxAlt) + " "\
            "ORDER BY  date  DESC; "
            
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
 
        print('isInsideMaxTolerantDistance() Total Row(s):', cursor.rowcount)
        noneCounter = 0
        for row in rows:
            distance = calculateDistance.distance((origLat, origLong), (row[3], row[4]))
            #print  'point1=[', (origLat, origLong), "] pt2=[" ,(row[3], row[4]), "] distance=", distance
            
            if (distance <=maxTolerantDistance):
                print  'point1<=', maxTolerantDistance
                coordinate = {}
                coordinate['date'] = row[1]
                coordinate['alt'] = row[2]
                coordinate['lat'] = row[3]
                coordinate['long'] = row[4]
                coordinate['speed'] = row[5]
                return coordinate
    except :
        print "isInsideMaxTolerantDistance() Something is wrong sql=[", sql
    return None

def updateICAOmap(db, cursor, icao, tailPin):
    
    sql="SELECT icao,  tailpin "\
            "FROM  AirTraffic.ICAOmap "\
            "WHERE icao='" + icao + "';"
            
    try:
        tday =  datetime.now(pytz.timezone(timeZone))
        dateStr = "%s-%s-%s"%(tday.year, tday.month,tday.day)
        
        cursor.execute(sql)
        rows = cursor.fetchall()
 
        print('updateICAOmap() Total Row(s):', cursor.rowcount)
        if cursor.rowcount == 0: #insert it as a new icao map
            sql = "INSERT INTO  AirTraffic.ICAOmap VALUES ('" + icao + "', '" + tailPin +"', '" + dateStr + "');"
        else:
            sql = "UPDATE AirTraffic.ICAOmap SET tailpin = '" + tailPin +"', date = '"  + dateStr + "' WHERE icao='" + icao + "';"

        print('updateICAOmap() sql=[', sql)

        cursor.execute(sql)
        db.commit()
            
    except :
        print "updateICAOmap() Something is wrong sql=[", sql
        ex = traceback.print_stack()
        print ex
        sendMail("parseICAO Failed updateICAOmap()", ex)
        db.rollback()
    return None

def findNewICAOs4Today():
    flightSql = ""
    sql = ""
    icaoDict = {}
    #MySQL lookup & update
    '''
    tday =  datetime.now(pytz.timezone(timeZone))
    dateStr = "%s-%s-%s"%(tday.year, tday.month,tday.day)
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
            dateStr = "%s-%s-%s"%(tday.year, tday.month,tday.day)
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
                    flightDict = lookupFlightNo(flightNo.rstrip())
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
                            flightDict = lookupFlightNo(TailPin.rstrip())
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


#icao1="a720eb"
icao1="780a6e"

result = lookupICAO(icao1)

