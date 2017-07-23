# Import modules
import RPi.GPIO as GPIO		# GPIO
import time			# TIME
import urllib			# URLLIB
import urllib2			# URLLIB2
import json			# JSON
import threading        # THREADING
import getWeather as weather	# Weather API
from neopixel import *		# LED Strip
from adxl345 import ADXL345	# Acceleration sensor

# Global variables
GPIO.setmode(GPIO.BCM)
pir_sensor = 21
pir_state = 0
GPIO.setup(pir_sensor, GPIO.IN)
current_weather = ""
future_weather = ""

# LED strip configuration:
LED_COUNT      = 13       # Number of LED pixels.
LED_PIN        = 18       # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5        # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0        # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Define a function which animates LEDs according to a color.
def colorWipe(strip, color, wait_ms=50):
	print "colorWipe()\n"
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

# Define a function which checks if motion is detected or not
def isDetected(curr_state) :
    print "isDetected()\n"
    if curr_state : return True
    else : return False

# Define a function which checks if the internet is connected or not
def isConnected() :
    print "isConnected()\n"
    try :
        urllib2.urlopen("http://goole.com")
        return True
    except urllib2.URLError as err :
        return False

# Define a function which checks the gravity of z axis 
def isUsed() :
    print "isUsed()\n"
    adxl345 = ADXL345()
    axes = adxl345.getAxes(True)
    print "isUsed() : Gravitional Acceleration(Z axis) : %.3fG" % ( axes['z'] )
    if float(axes['z']) > 0.8 :
	return False
    else : return True

# Define a function which gets the weather condtion
def getWeather() :
    print "getWeather()\n"
    global current_weather
    global future_weather
    status = weather.getWeather()
    current_weather = status['current_weather']
    future_weather = status['future_weather']

# Define a function which gets the weather constantly in a thread
def weatherForecast() :
    print "weatherForecast()"
    while True :
        # Check the internet connction
        if isConnected() :
            # If it's connected then get the weather status
            getWeather()
            # In addtion, sleep for an hour
            time.sleep(3600)
            print "weatherForecast() : Escaped!"
        else :
            # If it's not connected then constantly find the connection every 2 seconds
            print "weatherForecast() : No internet connection!"
            time.sleep(2)

# function1 thread starts as a daemon
stop_event = threading.Event()
function1 = threading.Thread(target= weatherForecast)
function1.daemon = True
function1.start()

# Main program logic follows:
if __name__ == '__main__':
        try :
            print "main()\n"
            # Create NeoPixel object with appropriate configuration.
            strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
            # Intialize the library (must be called once before other functions).
            strip.begin()
            time.sleep(2)
            
            while True:
                print current_weather + ', ' + future_weather
		taken = isUsed()
		if taken == True : 
			print "main() : This umbrella is being moved.."
			time.sleep(2)
		else :
			print "main() : Motion detecting.."
                        curr_state = GPIO.input(pir_sensor)
                        # print curr_state # log
                        if isDetected(curr_state) :
                            print "main() : Motion detected!"
                            # if it rains at the moment
                            if current_weather == str(1) :
                                for i in range(1, 6) :
                                    colorWipe(strip, Color(255, 0, 0))
                                    time.sleep(0.2)
                                    colorWipe(strip, Color(0, 0, 0))
                            else :
                            # it doesn't rain at the moment but if it rains later
                                if future_weather == str(1) :
                                    for i in range(1, 6) :
                                        colorWipe(strip, Color(255, 255, 0))
                                        time.sleep(0.2)
                                        colorWipe(strip, Color(0, 0, 0))
                                else :
                                    # if it doesn't rain all day
                                    for i in range(1, 6) :
                                        colorWipe(strip, Color(0, 255, 0))
                                        time.sleep(0.2)
                                        colorWipe(strip, Color(0, 0, 0))
                            if pir_state == 0 :
                                print "main() : Motion detected!"
                                pir_state = 1
                        else :
                            colorWipe(strip, Color(0, 0, 0))
                            if pir_state == 1 :
                                print "main() : Motion ended!"
                                pir_state = 0
                        time.sleep(1)
        except KeyboardInterrupt :
	    print "Finished!"
	    stop_event.set()
            GPIO.cleanup()
