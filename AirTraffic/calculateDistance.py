#https://gist.github.com/rochacbruno/2883505
import math

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    #radius = 6371 # km
    radius = 3959 # mile

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

origLat = 37.3522374; 
origLong = -122.052706; 
'''
lat2 = 37.42352292
long2 = -122.03399748000001
print distance((origLat, origLong), (lat2, long2)) 
'''