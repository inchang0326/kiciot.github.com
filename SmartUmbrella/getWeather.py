import urllib
import json
import re

# Global variables
lat = ""
lon = ""
address = ""
current_weather = ''
future_weather = ''

# Get GPS
def getGPSInfo() :
    global lat
    global lon
    url = "http://jhy753.dothome.co.kr/getGPS.php"
    request = urllib.urlopen(url)
    data = json.loads(request.read().decode('utf-8'))
    lat = data['latitude']
    lon = data['longitude']
    return {'latitude':lat, 'longitude':lon}

# Get Address
def getAddress() :
    global lat
    global lon
    global address
    getGPSInfo()
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lon+"&key=AIzaSyAFntqBb_gbIBUD53XIKk40XT6jzZkWhYk&language=ko"
    request = urllib.urlopen(url)
    data = json.loads(request.read().decode('utf-8'))
    address = data["results"][2]["formatted_address"]
    return address

# Get Weather
def getWeather() :
    global lat
    global lon
    global current_weather
    global future_weather
    getGPSInfo()
    url = "http://apis.skplanetx.com/weather/current/minutely?version=1&lat="+lat+"&lon="+lon+"&appKey=0416be7c-5761-3931-8698-e95845d8f850"
    request = urllib.urlopen(url)
    data = json.loads(request.read().decode('utf-8'))
    current_weather = data["weather"]["minutely"][0]["sky"]["code"]
    url = "http://apis.skplanetx.com/weather/forecast/3days?version=1&lat="+lat+"&lon="+lon+"&appKey=0416be7c-5761-3931-8698-e95845d8f850"
    request = urllib.urlopen(url)
    data = json.loads(request.read().decode('utf-8'))
    future_weather = data["weather"]["forecast3days"][0]["fcst3hour"]["sky"]["code10hour"]
    return {'current_weather': str(currentSkyCodeFilter(current_weather)), 'future_weather': str(futureSkyCodeFilter(future_weather))}
    
# Filter current sky code
def currentSkyCodeFilter(x) :
    return {
        'SKY_A01' : 0,
        'SKY_A02' : 0,
        'SKY_A03' : 0,
        'SKY_A04' : 1,
        'SKY_A05' : 1,
        'SKY_A06' : 1,
        'SKY_A07' : 1,
        'SKY_A08' : 1,
        'SKY_A09' : 1,
        'SKY_A10' : 1,
        'SKY_A11' : 1,
        'SKY_A12' : 1,
        'SKY_A13' : 1,
        'SKY_A14' : 1
        }.get(x, 2) #defalut

# Filter future sky code
def futureSkyCodeFilter(x) :
    return {
        'SKY_S01' : 0,
        'SKY_S02' : 0,
        'SKY_S03' : 0,
        'SKY_S04' : 1,
        'SKY_S05' : 1,
        'SKY_S06' : 1,
        'SKY_S07' : 1,
        'SKY_S08' : 1,
        'SKY_S09' : 1,
        'SKY_S10' : 1,
        'SKY_S11' : 1,
        'SKY_S12' : 1,
        'SKY_S13' : 1,
        'SKY_S14' : 1
        }.get(x, 2) #defalut
        
if __name__ == '__main__':
    getGPSInfo()
    getAddress()
    getWeather()
    print "latitude  : "+lat+"\n"+"longitude : "+lon
    print "Address   : " + address
    print "Weather(For now)          : " + current_weather
    print "Weather(7~10 hours later) : " + future_weather
