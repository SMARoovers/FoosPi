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
goal = 0
buttonDown = 0

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 80), Handler)

#server.serve_forever()

def ButtonPlayer1 (pin):
	print GPIO.input(23)
	if GPIO.input(23) == 0:
		#print "Button player 1 pressed"
		logger.info("Button player 1 pressed")
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


def SensorFired(hot, sensorNumber):
	global goal

	if hot:
		goal = 0
	else:
		goal = goal+1

	if goal == 1:
		print "Made web request for goal @ sensor"
		url = 'http://' + webserver + '/points/add/' + venue + '/' + str(sensorNumber)
		print url
		values = {'key' : 'value' }
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		time.sleep(1)


def ButtonFired(hot, buttonNumber):
	global buttonDown

	if hot:		
		#if hot > 1
		#	print "button losgelaten"
		buttonDown = 0
	else:
		buttonDown = buttonDown+1

	if buttonDown == 1:
		print "Goal claimed using button " + str(buttonNumber)
		time.sleep(0.5)


def main():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN)
    #GPIO.add_event_detect(23,GPIO.FALLING, callback=ButtonPlayer1)
    #GPIO.add_event_detect(24,GPIO.RISING, callback=SensorSide1)
    
    while True:
	SensorFired(GPIO.input(24), 1)
	ButtonFired(GPIO.input(23), 1)
	
	# for other sensors, add if statement below with sensornumber as second parameter
	# SensorFired(true, 2)



    print "cleanup"	
    GPIO.cleanup()



if __name__=="__main__":
    main()
