#!/usr/bin/python
import sys
import telnetlib
import MySQLdb

# Open database connection
db = MySQLdb.connect("lab2.svcvllc.com","datafeed","Sunnyva1e","AirTraffic" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

tn_ip = "localhost"
tn_port = "30003"
minimumHeight=8000
interval=5
noGPSInterval= interval *3

flightMap = {}
#Access the local port`
def telnet():
    try:
        tn = telnetlib.Telnet(tn_ip, tn_port, 15)
    except:
        print "Unable to connect to Telnet server: " + tn_ip
        return
    #tn.set_debuglevel(100)
    while True:
		line = tn.read_until("\r\n")
		#print "=>", line
		tokens = line.split(',')
		#skip various conditions
		if (len(tokens)) < 17:
			continue
		if (len(tokens[11]) > 0 and int(tokens[11])> minimumHeight):   #skip the high fliers
			continue
		#if (len(tokens[14]) == 0 or len(tokens[15]) == 0 or len(tokens[11]) == 0 ): #skip one has no 3D 
		#	continue
		#print  "=>", tokens[0], tokens[1], tokens[4], tokens[6], tokens[7], tokens[8],tokens[9], tokens[10], tokens[11], tokens[14], tokens[15]	
		icao = tokens[4]
		#if (flightMap[icao] is None):
			#flightMap[icao] = tokens[7]
		time = tokens[6] + " " + tokens[7]
		sql=""
		try:
			# Execute the SQL command
			if (int(tokens[1]) ==3):
				alt="0"
				if (len(tokens[11]) > 0):
					alt = tokens[11]

				lat="0.00"
				if (len(tokens[14]) > 0):
					lat = tokens[14]

				long="0.00"
				if (len(tokens[15]) > 0):
					long = tokens[15]
					
				sql = "INSERT INTO positionHistory VALUES(null,'" + tokens[4] +"','" + time + "', " 
				#print "SQL=", sql
				sql = sql +alt + ", " + lat + ", " + long +  "," + tokens[1] + ")"
				#print "SQ2L=", sql
				cursor.execute(sql)
			# Commit your changes in the database
			db.commit()
		except:
			# Rollback in case there is any error
			print "MySQL Insert errort time=[", time, "], SQL=", sql
			db.rollback()

telnet()

db.close()

