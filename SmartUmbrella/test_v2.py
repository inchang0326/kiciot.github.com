# Import modules
import RPi.GPIO as GPIO		    # GPIO
import time			     # TIME
import urllib			     # URLLIB
import urllib2			     # URLLIB2
import json			     # JSON
import threading             # THREADING
import getWeather as weather	# Weather API
from neopixel import *		     # LED Strip
from adxl345 import ADXL345	 # Acceleration sensor

GPIO.setwarnings(False)

# Global variables
GPIO.setmode(GPIO.BCM)
pir_sensor = 21
pir_state = 0
curr_state = 0
GPIO.setup(pir_sensor, GPIO.IN)

current_weather = ""
future_weather = ""
first_internet_check = 0

potentiometer_adc = 0; # 10k trim pot connected to adc #0
# SPI port on the ADC to the Cobbler
SPICLK = 5
SPIMISO = 6
SPIMOSI = 13
SPICS = 19
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# LED strip configuration:
LED_COUNT      = 13                  # Number of LED pixels.
LED_PIN        = 18                  # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10                 # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000              # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5                   # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255                 # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False               # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0                   # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB # Strip type and colour ordering

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
    
def measureForce() :
        # read the analog pin
        trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        return trim_pot
        
# Define a function which animates LEDs according to a color.
def colorWipe(strip, color, wait_ms=50):
	print "colorWipe()"
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

# Define a function which checks the gravity of z axis 
def isUsed() :
        print "isUsed()"
        adxl345 = ADXL345()
        axes = adxl345.getAxes(True)
        forces = measureForce()
        print "isUsed()\t[ Z Acceleration : %.3fG ]" % ( axes['z'] )
        print "isUsed()\t[ F sensitivity  : %d ]" % ( forces )
        if float(axes['z']) > 0.8 and forces < 10 :
            return False
        else : return True
    
# Define a function which checks if motion is detected or not
def isDetected() :
        global pir_state
        while True :
                print "isDetected()"
                pir_state = GPIO.input(pir_sensor)
                time.sleep(2)
    
# function1 thread starts as a daemon
function1 = threading.Thread(target= isDetected)
function1.daemon = True
function1.start()        
    
# Define a function which checks if the internet is connected or not
def isConnected() :
        print "isConnected()"
        try :
            urllib2.urlopen("http://goole.com")
            return True
        except urllib2.URLError as err :
            return False
        
# Define a function which gets the weather condtion
def getWeather() :
        print "getWeather()"
        global current_weather
        global future_weather
        status = weather.getWeather()
        current_weather = status['current_weather']
#        future_weather = status['future_weather']

# Define a function which gets the weather constantly in a thread
def weatherForecast() :
        global first_internet_check
        print "weatherForecast()"
        while True :
            global first_internet_check
            # Check the internet connction
            if isConnected() :
                # If it's connected then get the weather status
                getWeather()
                # In addtion, sleep for an hour
                first_internet_check = 1
                time.sleep(3600)
                print "weatherForecast() : Escaped!"
            else :
                # If it's not connected then constantly find the connection every 1 seconds
                print "weatherForecast() : No internet connection!"
                time.sleep(1)
            
# function1 thread starts as a daemon
function2 = threading.Thread(target= weatherForecast)
function2.daemon = True
function2.start()

# Main program logic follows:
if __name__ == '__main__':
        try :
            print "main()"
            # Create NeoPixel object with appropriate configuration.
            strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
            # Intialize the library (must be called once before other functions).
            strip.begin()
            time.sleep(2)
            
            while True:
                taken = isUsed()
		if taken == True : 
			print "main()\t\t[ Umbrella is being moved ]"
			time.sleep(0.5)
                else :
                    print "main()\t\t[ Motion detecting.. ]"
                    time.sleep(0)
                    # print curr_state # log
                    if pir_state and first_internet_check :
                        print "main()\t\t[ Motion detected! ]"
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
                        if curr_state == 0 :
                            curr_state = 1       
                    else :
                        if curr_state == 1 :
                            print "main()\t\t[ Motion ended! ]"
                            curr_state = 0
        except KeyboardInterrupt :
	    print "Finished!"
            GPIO.cleanup()
        