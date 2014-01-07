#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

def buttonEventHandler (pin):
    print "Button pressed!"

def main():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.remove_event_detect(23)
    GPIO.add_event_detect(23,GPIO.RISING)
    GPIO.add_event_callback(23,buttonEventHandler,1000)
    # time.sleep(5)

    while True:
        pass


    GPIO.cleanup()



if __name__=="__main__":
    main()
