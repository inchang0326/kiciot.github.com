import urllib
import json

curr_lat = ""
curr_lon = ""
all_lat = []
all_lon = []
all_desc = []
size = 0

# Get current GPS info
def getGPSInfo() :
    global curr_lat
    global curr_lon
    url = "http://jhy753.dothome.co.kr/getGPS.php"
    request = urllib.urlopen(url)
    data = json.loads(request.read().decode('utf-8'))
    curr_lat = data['latitude']
    curr_lon = data['longitude']
    return {'latitude':curr_lat, 'longitude':curr_lon}

# Get all GPS info and description
def getAllInfo() :
    global all_lat
    global all_lon
    global all_desc
    global size
    url = "http://jhy753.dothome.co.kr/getAll.php"
    request = urllib.urlopen(url)
    data = json.loads(request.read().decode('utf-8'))
    all_lon = data[0]
    all_lat = data[1]
    all_desc = data[2]
    size = data[3]
    return {'latitude':all_lat, 'longitude':all_lon, 'description':all_desc, 'size':size}

if __name__ == '__main__':
    currentGPS = getGPSInfo()
    print "Current Latitude : " + currentGPS['latitude'] + "\n" + "Current Longitude : " + currentGPS['longitude']
#    allThings = getAllInfo()
#    print "All Latitude : " + str(allThings['latitude'][0]) + "\n" + "All Longitude : " + str(allThings['longitude'][0]) + "\n" + "All description : " + str(allThings['description'][0]) + "\n" + "Size : " + str(allThings['size'][0])
#    hi = getAllInfo()
#    print hi['latitude'][0]