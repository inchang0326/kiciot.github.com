#-*- coding: utf-8 -*-

import math
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import getGPS as gps
from pyproj import Proj, transform

# Raspberry Pi pin configuration:
RST = 24

# Note the followings are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 20
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding


# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype("gulim.ttc", 14, encoding="unic")
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font20 = ImageFont.truetype('malgun.ttf', 12)
#font = ImageFont.truetype('Minecraftia.ttf', 8)

# A function for getting calculated distance with two GPS info
def getDistanceFromLatLonInKm(lonlat1, lonlat2) :
	def deg2rad(deg) :
		return float(deg)*(3.14/180.0)
			
	R = 6371
	
	dLat = deg2rad(lonlat2[1]-float(lonlat1[1]))
	dLon = deg2rad(lonlat2[0]-float(lonlat1[0]))
	
	a = math.sin(dLat/2.0)*math.sin(dLat/2.0)+math.cos(deg2rad(float(lonlat1[1]))) * math.cos(deg2rad(lonlat2[1]-float(lonlat1[1]))) * math.sin(dLon/2.0)*math.sin(dLon/2.0)
	c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))	
	dist = R*c

	return dist

# A function for getting claculated bearing with to GPS info
def bearingP1toP2(lonlat1, lonlat2):

	Cur_Lat_radian = float(lonlat1[1])*(3.141592/180.0)
	Cur_Lon_radian = float(lonlat1[0])*(3.141592/180.0)
	
	Dest_Lat_radian = lonlat2[1]*(3.141592/180.0)
	Dest_Lon_radian = lonlat2[0]*(3.141592/180.0)
	
	radian_distance = 0
	radian_distance = math.acos(math.sin(Cur_Lat_radian)*math.sin(Dest_Lat_radian)+math.cos(Cur_Lat_radian)*math.cos(Dest_Lat_radian)*math.cos(Cur_Lon_radian-Dest_Lon_radian ))
	radian_bearing = math.acos((math.sin(Dest_Lat_radian)-math.sin(Cur_Lat_radian)*math.cos(radian_distance))/(math.cos(Cur_Lat_radian)*math.sin(radian_distance)))
	
	true_bearing = 0
	
	if math.sin(Dest_Lon_radian - Cur_Lon_radian ) < 0:
		true_bearing = radian_bearing*(180.0/3.141592)
		true_bearing = 360 - true_bearing
	else:
		true_bearing = radian_bearing*(180.0/3.141592)
	
	if true_bearing > 0 :
		print(true_bearing)	
	if true_bearing > 20 and true_bearing <=70 :
		#print("북동쪽")
		draw.text((x,top+30),u"    <<북동쪽>",font=font, fill=255)
	elif true_bearing > 70 and true_bearing < 110 :
		#print("동쪽")
		draw.text((x,top+30),u"    <<동쪽>>",font=font, fill=255)
	elif true_bearing >= 110 and true_bearing <= 160 :
		#print("동남쪽")
		draw.text((x,top+30),u"    <<동남쪽>>",font=font, fill=255)
	elif true_bearing > 160 and true_bearing < 200 :
		#prit("남쪽")
		draw.text((x,top+30),u"    <<남쪽>>",font=font, fill=255)
	elif true_bearing > 200 and true_bearing <= 250 :
		#print("남서쪽")
		draw.text((x,top+30),u"    <<남서쪽>>",font=font, fill=255)
	elif true_bearing > 250 and true_bearing < 290 :
		#print("서쪽")
		draw.text((x,top+30),u"    <<서쪽>>",font=font, fill=255)
	elif true_bearing >= 290 and true_bearing <= 340 :
		#print("북서쪽")
		draw.text((x,top+30),u"    <<북서쪽>>",font=font, fill=255)
	else:
		#print("북쪽")
		draw.text((x,top+30),u"    <<북쪽>>",font=font, fill=255)
	

# Size of the set includes all info such as GPS and desc
allThings_size = 0

# A function for printing navigation description and bearing value on the display
def navigation(i) :
	global allThings_size
	# 현재 좌표
	current_GPS = gps.getGPSInfo()
	current_lat = current_GPS['latitude']
	current_lon = current_GPS['longitude']

	# 전체 좌표
	allThings = gps.getAllInfo()
	accumulated_lat = allThings['latitude'][i]
	accumulated_lon = allThings['longitude'][i]
        allThings_size = allThings['size'][0]
        
	# 전체 좌표 변환
	inProj = Proj(init = 'epsg:3857')
	outProj = Proj(init = 'epsg:4326')
	transformed_lon, transformed_lat = transform(inProj, outProj, accumulated_lon, accumulated_lat)

	lonlat1 = (current_lon, current_lat)
	lonlat2 = (transformed_lon, transformed_lat)
	#print lonlat1[0], lonlat1[1]
	#print lonlat2[0], lonlat2[1]
	distance = getDistanceFromLatLonInKm(lonlat1, lonlat2)*1000

	if distance > 0.005 :
  		#print str(distance) + "m\n"
  		#print allThings['description'][i] + "\n"
  		length = len(allThings['description'][i])
  		original = allThings['description'][i]
  		part1 = original[0:length/2]
  		part2 = original[length/2:length]
  		
  		draw.text((x,top),unicode(part1), font=font, fill=255)
                draw.text((x, top+15), unicode(part2), font=font, fill=255)
               
                # Display image.
                disp.image(image)
                disp.display()
  		bearingP1toP2(lonlat1, lonlat2)
  		return 1
  	
  	else : return 0

# A function for looping the navigation function
def looper(i):
        global allThings_size
	time.sleep(2)
	
	d = 0
	d = navigation(i)
	
	if allThings_size > i :
		if d == 1 :
                    nothing = 0
		
		else:
		    i=i+1
		
		looper(i)

# A main function to start looper method
def main() :
	looper(0)

if __name__ == "__main__":
	main()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
