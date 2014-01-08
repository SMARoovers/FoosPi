#!/usr/bin/env python

import os
import time
import RPi.GPIO as GPIO
print "Loaded RPi.GPIO version" + GPIO.VERSION
import sys
import urllib
import urllib2
import SimpleHTTPServer
import SocketServer

#prepare log
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

os.system('clear')
venue = raw_input("Which venue is this? ")
os.system('clear')
print "Chosen venue is " + venue
logger.info("Chosen venue is " + venue)

webserver = 'foosball.vicompany.local'

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 80), Handler)

server.serve_forever()

def ButtonPlayer1 (pin):
	print "Button player 1 pressed"
	logger.info("Button player 1 pressed")
	#Ignore debounce effect
	global time_stamp
	time_now = time.time()
	if (time_now - time_stamp) >= 1.0:
		print "Ready to scan."
	time_stamp = time_now
	#Claim point
	try:
		url = 'http://' + webserver + '/points/claim/' + venue + '/1'
		values = {'key' : 'value' }
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
	except urllib2.HTTPError, e:
		print e
		logger.error(e)

def SensorSide1 (pin):
	print "Sensor side 1 detected movement"
	#Add goal
	try:
		url = 'http://' + webserver + '/goals/add/' + venue + '/1'
		values = {'key' : 'value' }
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
	except urllib2.HTTPError, e:
		print e
		logger.error(e)

def main():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    time_stamp = time.time()
    GPIO.remove_event_detect(23)
    GPIO.remove_event_detect(24)
    GPIO.add_event_detect(23,GPIO.RISING, callback=ButtonPlayer1, bouncetime=200)
    GPIO.add_event_detect(24,GPIO.RISING, callback=ButtonPlayer1, bouncetime=200)
    # time.sleep(5)

    while True:
	os.system('clear')
        print "Waiting for event."
	time.sleep(1)
	os.system('clear')
        print "Waiting for event.."
	time.sleep(1)
	os.system('clear')
        print "Waiting for event..."
	time.sleep(1)



    GPIO.cleanup()



if __name__=="__main__":
    main()
