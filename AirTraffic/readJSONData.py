# Array example 
import urllib2 
import json 
import time

url = 'http://savemysky.svcvllc.com:8000/data/aircraft.json'
while True:
	req = urllib2.Request(url) 
	opener = urllib2.build_opener() 
	f = opener.open(req) 
	jsonData = json.loads(f.read()) 
	#print json 
	#print json['aircraft']
	aircraftList = jsonData['aircraft']

	for flit in aircraftList:
		hex = flit.get("hex", "")
		speed = flit.get("speed", "0")
		altitude = flit.get("altitude", "0")
		lat = flit.get("lat", "0.0")
		lon = flit.get("lon", "0.0")
		flight = flit.get("flight", "")
		squawk = flit.get("squawk", "")
		nucp = flit.get("nucp", "")
		seen_pos = flit.get("seen_pos", "")
		vert_rate = flit.get("vert_rate", "")
		track = flit.get("track", "")
		category = flit.get("category", "")
		messages = flit.get("messages", "")
		seen = flit.get("seen", "")
		rssi = flit.get("rssi", "")
		#mlat = flit.get("mlat", "")
		#tisb = flit.get("tisb", "")

		if (float(lat) > 0 and float(lon)!=0):
			print hex, flight, altitude, lat, lon, speed, squawk, seen_pos, vert_rate, track
	time.sleep(10)
