import urllib                   #https://docs.python.org/2/library/urllib.html
from bs4 import BeautifulSoup   #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree, 
from pip._vendor.requests import structures
                                #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
import MySQLdb

from calculateDistance import *
from mySendmail import sendMail

from datetime import date, datetime
import pytz
import calculateDistance

timeZone = 'US/Pacific'
minAlt = 100
maxAlt = 4500

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
    
        print "******:", title#, titleList
        
        body=soup.body
        table=body.contents[6].table
        #print table
        
        strongs = table.findAll("strong", { })
        flightNo = removeHTMLTag(strongs)
        print "****** flightNo:", flightNo
    
        spans = table.findAll("span", { })
        flightName = removeHTMLTag(spans[0])
        print "****** flightName", flightName
        
        spans = table.findAll("span", class_="hint")
        origAirport = extractHTMLTagAttribute(spans[0], "title")
        destAirport = extractHTMLTagAttribute(spans[1], "title")
        print "****** origAirport:", origAirport.split()[-1]
        print "****** destAirport:", destAirport.split()[-1]
        
        spans = table.findAll("span", class_="flightStatusGood")
        status = removeHTMLTag(spans[0])
        print "****** status", status
        
        if (len(spans) > 1):
            onTime = removeHTMLTag(spans[1])
            flightDict['onTime']=onTime
            print "****** onTime", onTime
        
        #divTracePanelCourse = soup.select("#polling-flight_status")
        #print divTracePanelCourse
        ths = table.findAll("th", class_="secondaryHeader")
        #for th in ths:
        #    print "****** th:", th, " next=[", th.next_sibling.next_sibling
        
        aircraft = ths[1].next_sibling.next_sibling
        aircraftName = aircraft.contents[0]
        aircraft = removeHTMLTag(aircraft.contents[1])
        print "****** aircraftName:", aircraftName, "-", aircraft
        
        speed = removeHTMLTag(ths[2].next_sibling.next_sibling.contents[0])
        print "****** speed:", speed
        altitude = removeHTMLTag(ths[3].next_sibling.next_sibling).split("feet")[0]
        print "****** altitude:",altitude
        distance = removeHTMLTag(ths[4].next_sibling.next_sibling)
        print "****** distance:",distance
        route = removeHTMLTag(ths[5].next_sibling.next_sibling)
        print "****** route:", route
        
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

def findNewICAOs4Today():
    tday =  datetime.now(pytz.timezone(timeZone))
    dateStr = "%s-%s-%s"%(tday.year, tday.month,tday.day)
    print "dateStr=[",dateStr, "(%f,%f)"%( calculateDistance.origLat,calculateDistance.origLong)
    
    #MySQL lookup & update
    sql="SELECT icao,  max(date) datetm, min(altitude) alt, avg(latitude) lat, avg(longititude) lon, avg(speed) speed "\
            "FROM AirTraffic.AirtrafficUI_positionjsonhistory "\
            "WHERE date LIKE '" + dateStr + "%' and altitude > " + str(minAlt) + " and altitude < " + str(maxAlt) + " "\
                "AND icao NOT IN (SELECT distinct icao "\
                                    "FROM AirTraffic.AirtrafficUI_flights "\
                                    "WHERE date LIKE '" + dateStr + "%') "\
            "GROUP BY icao "\
            "ORDER BY  datetm  DESC; "

        # Or don't use GROUP BY, scan all coordinates for a flight to see if it's over our head. radius of 3 miles
        # library: https://pypi.python.org/pypi/geopy/1.11.0
    
    # http://www.mysqltutorial.org/python-mysql-query/
    db = None
    cursor = None
    try:

        db = MySQLdb.connect("lab2.svcvllc.com","httpuser","Save3ySky","AirTraffic" )
        
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchall()
 
        print('Total Row(s):', cursor.rowcount)
        noneCounter = 0
        for row in rows:
            newIcao=row[0]
            datetm=row[1]
            #print "\n new ICAO=[", newIcao, "] tm=[", datetm, "] counter=", noneCounter
            flightDict = lookupICAO(newIcao)
            if (flightDict is None):
                noneCounter +=1
                #print noneCounter, flightDict
            else:
                noneCounter =0 #reset the counter
                print noneCounter, flightDict
                coordinate = isInsideMaxTolerantDistance(cursor, newIcao, dateStr)
                
                if coordinate is not None: #insert the flight info to flights table
                    flightSql = "INSERT INTO AirtrafficUI_flights VALUES(null,'" + newIcao + "', '" + flightDict['flightNo'] + "', " \
                                " '" + str(coordinate['date']) + "', " + str(coordinate['alt']) + ", " + str(coordinate['lat']) + ", " + \
                                str(coordinate['long']) + ", '" +  flightDict['aircraft'] + "', '" + flightDict['origAirport'] + "', '" + \
                                flightDict['destAirport'] + "', " + str(coordinate['speed']) + ");"
                    
                    print "INSERTing flightSql=[" , flightSql
                    cursor.execute(flightSql)
                    
            if (noneCounter > 20):
                #stop processing obsolete ICAO further
                break;
        
        # Commit your changes in the database
        db.commit()
    
    except :
        print "Something is wrong sql=[", sql
        db.rollback()
    
    if cursor is not None:
        cursor.close()
    if db is not None:
        db.close()
    
    return None

    
    
findNewICAOs4Today()


#icao1="a720eb"
icao1="780a6e"

result = lookupICAO(icao1)

