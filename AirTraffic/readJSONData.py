# Array example 
import urllib2 
import json 
import time
from datetime import datetime
import MySQLdb

# Open database connection
db = MySQLdb.connect("lab2.svcvllc.com","datafeed","Sunnyva1e","AirTraffic" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

#url = 'http://savemysky.svcvllc.com:8000/data/aircraft.json'
url = 'http://localhost:8080/data/aircraft.json'
minimumHeight=8000
interval=10
noGPSInterval= interval *3
noGPSAltDiff = 200

while True:
	req = urllib2.Request(url) 
	opener = urllib2.build_opener() 
	f = opener.open(req) 
	jsonData = json.loads(f.read()) 
	#print json 
	#print json['aircraft']
	aircraftList = jsonData['aircraft']
	now = str(datetime.now())
	
	for flit in aircraftList:
		hex = flit.get("hex", "")
		speed = flit.get("speed", "0")
		altitude = flit.get("altitude", "0")
		if str(altitude).lower() == "ground":
			altitude = "0";
		lat = flit.get("lat", "0.0")
		lon = flit.get("lon", "0.0")
		flight = flit.get("flight", "null")
		squawk = flit.get("squawk", "null")
		nucp = flit.get("nucp", "0")
		seen_pos = flit.get("seen_pos", "0.00")
		vert_rate = flit.get("vert_rate", "0")
		track = flit.get("track", "0")
		category = flit.get("category", "")
		messages = flit.get("messages", "0")
		seen = flit.get("seen", "0.0.")
		rssi = flit.get("rssi", "0.0")
		#mlat = flit.get("mlat", "")
		#tisb = flit.get("tisb", "")
		sql = ""
		if (altitude < 50 and int(speed) < 20):
			continue;
 
		if (float(lat) > 0 and float(lon)!=0 and int(altitude) < minimumHeight):
		#	print hex, flight, altitude, lat, lon, speed, squawk, seen_pos, vert_rate, track
			sql += "INSERT INTO AirtrafficUI_positionjsonhistory VALUES(null,'" + hex +"','" +flight + "', '"
			sql += now[0:19] + "', " + str(altitude) + ", " + str(lat) + ", "+ str(lon) + ", '" + squawk + "', " + str(nucp) + ", "
			sql += str(seen_pos) + ", " + str(vert_rate) + ", "+ str(track) + ", " + str(speed)+ ", '" + category + "', " 
			sql += str(messages) + ", " + str(seen) + ", " + str(rssi) + ")"
			#
			#print "SQL=", sql
			try:
				cursor.execute(sql)
				# Commit your changes in the database
				db.commit()
			except:
				# Rollback in case there is any error
				print "MySQL Insert errort time=[", time, "], SQL=", sql
				db.rollback()

	time.sleep(interval*1)
#http://naelshiab.com/tutorial-send-email-python/
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
fromaddr = "redbiglobster@gmail.com"
toaddr = "smmeng@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Flight DataFeed Crashed!"
 
body = "Please rescue me!"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "gong0425")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
