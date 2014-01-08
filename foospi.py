#!/usr/bin/env python

import os
import time
import RPi.GPIO as GPIO
import sys
import urllib
import urllib2

os.system('clear')
venue = raw_input("Which venue is this? ")
os.system('clear')
print "Chosen venue is " + venue

webserver = 'foosball.vicompany.local'

def buttonEventHandler (pin):
	print "Button pressed!"
	try:
		url = 'http://' + webserver + '/goals/add/' + venue + '/1'
		values = {'key' : 'value' }
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
	except urllib2.HTTPError, e:
		print e

def main():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.remove_event_detect(23)
    GPIO.add_event_detect(23,GPIO.RISING)
    GPIO.add_event_callback(23,buttonEventHandler,1000)
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
