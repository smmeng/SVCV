import urllib                   #https://docs.python.org/2/library/urllib.html
from bs4 import BeautifulSoup   #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree, 
                                #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all

#icao1="a720eb"
icao1="a904e1"


#def lookupICAO(icao):
def lookupICAO(icao):
    
    ICAOurl= "http://flightaware.com/live/modes/" + icao + "/redirect"
    
    opener = urllib.FancyURLopener({})
    f = opener.open(ICAOurl)
    
    html_doc = f.read()
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    title = soup.title
    print "******:", title#, titleList
    #titleList = title.split("-")
    body=soup.body
    table=body.contents[6].table
    #print table
    
    strongs = table.findAll("strong", { })
    flightNo = strongs
    print "****** strongs:", strongs
    spans = table.findAll("span", { })
    flightName = spans[0]
    
    print "****** flightName", flightName
    
    spans = table.findAll("span", class_="hint")
    origAirport = spans[0]
    destAirport = spans[1]
    print "****** origAirport", origAirport
    print "****** destAirport", destAirport
    
    spans = table.findAll("span", class_="flightStatusGood")
    status = spans[0]
    print "****** status", status
    
    if (len(spans) > 1):
        onTime = spans[1]
        print "****** onTime", onTime
    
    #divTracePanelCourse = soup.select("#polling-flight_status")
    #print divTracePanelCourse
    ths = table.findAll("th", class_="secondaryHeader")
    #for th in ths:
    #    print "****** th:", th, " next=[", th.next_sibling.next_sibling
    
    aircraft = ths[1].next_sibling.next_sibling
    print "****** aircraft:", aircraft.contents[0], aircraft.contents[1]
    
    speed = ths[2].next_sibling.next_sibling
    print "****** speed", speed
    altitude = ths[3].next_sibling.next_sibling
    print "****** altitude", altitude
    distance = ths[4].next_sibling.next_sibling
    print "****** distance",distance
    route = ths[5].next_sibling.next_sibling
    print "****** route", route
    
    return None



result = lookupICAO(icao1)