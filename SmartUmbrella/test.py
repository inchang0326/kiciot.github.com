import time
import threading
import urllib2
import getWeather as weather

current_weather = ''
future_weather = ''

def getWeather() :
    print "getWeather()"
    global current_weather
    global future_weather
    status = weather.getWeather()
    current_weather = status['current_weather']
    future_weather = status['future_weather']
    
def isConnected() :
    print "isConnected()"
    try :
        urllib2.urlopen("http://goole.com")
        return True
    except urllib2.URLError as err :
        return False

def weatherForecast() :
    print "weatherForecast()"
    while True :
        if isConnected() :
            getWeather()
            print current_weather + ', ' + future_weather
            time.sleep(10)
            print "weatherForecast() : Escaped!"
        else :
            print "weatherForecast() : No internet connection!"
            time.sleep(2)
    
t1 = threading.Thread(target= weatherForecast)
# Thread starts as a daemon
t1.daemon = True
t1.start()
                     
def weatherForecast2() :
    print "weatherForecast()2"
    while True :
        print "test!"
        time.sleep(1.5)
        
t2 = threading.Thread(target= weatherForecast2)
# Thread starts as a daemon
t2.daemon = True
t2.start()

try :
    while True :
        if current_weather == str(1) :
            print "Hey!"
        time.sleep(2)
        
except KeyboardInterrupt :
    print "Finished!"