# Import modules
import RPi.GPIO as GPIO		    # GPIO
import time			     # TIME
import sys

GPIO.setwarnings(False)

# Global variables
GPIO.setmode(GPIO.BCM)
button = 10
cnt = 0
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# A function for looping the navigation function
def looper():
    global cnt
    if cnt == 1 :
        time.sleep(2)
        cnt = cnt + 1
    else :
        time.sleep(0.1)
    print "haha"
    if 5 > 3 :
        nothing = 1
    else :
        print "fuck"
    if GPIO.input(button) == False :
        print "hehe"
        return 0
    time.sleep(1)
    looper()	
		
# A main function to start looper method
def main() :
    global cnt
    while True :
        if GPIO.input(button) == False :
            print "Button Pressed"
            cnt = cnt + 1
            looper()        
        
if __name__ == "__main__":
	main()

        