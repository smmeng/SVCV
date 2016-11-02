import sys
import telnetlib

tn_ip = "localhost"
tn_port = "30003"

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
		if (len(tokens)) < 17:
			continue
		if (len(tokens[14]) == 0 or len(tokens[15]) == 0 ):
			continue
		print  "=>", tokens[0], tokens[1], tokens[4], tokens[6], tokens[7], tokens[8],tokens[9], tokens[11], tokens[14], tokens[15]


telnet()
