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
from serial import Serial
from rdm880 import *
import threading

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

baseUrl = 'http://foosball.vicompany.local/'
goal = 0
buttonDown = 0

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def HTTPServer():
	Handler = MyRequestHandler
	SocketServer.TCPServer.allow_reuse_address = True
	server = SocketServer.TCPServer(('0.0.0.0', 80), Handler, bind_and_activate=True)
	server.serve_forever()

t1 = threading.Thread(target=HTTPServer, args=[])
t1.start()

def GetRFID ():
	io = Serial('/dev/ttyAMA0', 9600, timeout=1)
	p = Packet(0x25, [0x26, 0x00]) # OV-chipkaart
	reply = p.execute(io)
	cardid = reply.data
	cardid_hex = "".join(map(lambda x: "%.2X" % x , cardid))
	return cardid_hex

def SensorFired(hot, sensorNumber):
	global goal

	if hot:
		goal = 0
	else:
		goal = goal+1

	if goal == 1:
		url = 'points/add/' + str(venue) + '/' + str(sensorNumber)
		DoWebRequest(url)	

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
		ID = GetRFID ()
		if ID:
			print 'ID found: ' + ID

		else:
			print "Goal claimed using button " + str(buttonNumber)
			logger.info("Button player " + str(buttonNumber) + " pressed")
			url = 'points/claim/' + str(venue) + '/' + str(buttonNumber)
			DoWebRequest(url)

		time.sleep(0.5)



def DoWebRequest(url):
	try:
		fullUrl = baseUrl + url
		req = urllib2.Request(fullUrl, '')
		response = urllib2.urlopen(req)
		the_page = response.read()
		logThatShit('Web request made to ' + fullUrl)
	except urllib2.HTTPError, e:
		print e
		logThatShit(e, 'error')


def logThatShit(text, type = 'info'):
	if type == 'error':
		logger.error(text)
	else:
		logger.info(text)

	print text


def main():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button
    #GPIO.setup(23, GPIO.IN)
    #GPIO.add_event_detect(23,GPIO.FALLING, callback=ButtonPlayer1)
    #GPIO.add_event_detect(24,GPIO.RISING, callback=SensorSide1)
    
    while True:
	#SensorFired(GPIO.input(24), 1)
	#ButtonFired(GPIO.input(23), 1)
	ButtonFired(GPIO.input(24), 2)
	
	# for other sensors, add if statement below with sensornumber as second parameter
	# SensorFired(true, 2)



    print "cleanup"	
    GPIO.cleanup()



if __name__=="__main__":
    main()
