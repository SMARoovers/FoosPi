#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import urllib
import urllib2

def main():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17,GPIO.IN)
    GPIO.setup(18,GPIO.IN)

    goal17 = 0
    goal18 = 0

    webserver = 'ip-address or domain'

    while True:
	if GPIO.input(17):
		goal17 = 0
	else:
		goal17 = goal17+1
		if goal17 == 1:
			print "Made web request for goal 1"
			url = 'http://'webserver'/goals/add/1'
			values = {'key' : 'value' }
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
			time.sleep(2.0)
			
	if GPIO.input(18):
		goal18 = 0
	else:
		goal18 = goal18+1
		if goal18 == 1:
			print "Made web request for goal 2"
			url = 'http://'webserver'/goals/add/2'
			values = {'key' : 'value' }
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
			time.sleep(2.0)

    print "button pushed"

    GPIO.cleanup()



if __name__=="__main__":
    main()
