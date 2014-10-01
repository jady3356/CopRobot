#!usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
import getopt
import string
from distance import measure_average
GPIO.setmode(GPIO.BCM)

L1 = 5
R1 = 6
L2 = 23
R2 = 24 
recoveryCount = 0

GPIO.setup(L1,GPIO.OUT)
GPIO.setup(R1,GPIO.OUT)
GPIO.setup(L2,GPIO.OUT)
GPIO.setup(R2,GPIO.OUT)

def forward():
    GPIO.output(L1,GPIO.LOW)
    GPIO.output(R1,GPIO.HIGH)
    GPIO.output(L2,GPIO.HIGH)
    GPIO.output(R2,GPIO.LOW)
    
def backward():
    GPIO.output(L1,GPIO.HIGH)
    GPIO.output(R1,GPIO.LOW)
    GPIO.output(L2,GPIO.LOW)
    GPIO.output(R2,GPIO.HIGH)
 
def turn_right():
    GPIO.output(L1,GPIO.LOW)
    GPIO.output(R1,GPIO.LOW)
    GPIO.output(L2,GPIO.HIGH)
    GPIO.output(R2,GPIO.LOW)
    
def turn_left():
    GPIO.output(L1,GPIO.LOW)
    GPIO.output(R1,GPIO.HIGH)
    GPIO.output(L2,GPIO.LOW)
    GPIO.output(R2,GPIO.LOW)
    
def stop():
    GPIO.output(L1,GPIO.LOW)
    GPIO.output(R1,GPIO.LOW)
    GPIO.output(L2,GPIO.LOW)
    GPIO.output(R2,GPIO.LOW)

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "a:t:")
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    for op,value in opts:
        if op == "-a":
            if value == "f":
                print "Foward..."
                stop()
                forward()
            if value == "b":
                print "Backward..."
                stop()
                backward()
            if value == "l":
                print "Turn left..."
                stop()
                turn_left()
            if value == "r":
                print "Turn right..."
                stop()
                turn_right()
            if value == "s":
                print "Stop..."
                stop()
        if op == "-t":
            time.sleep(string.atoi(value))    
            
def autoMove():
    try:
        while True:
            distance = measure_average()
	    if distance > 35:
	        print "Distance : %.1fcm, forward" % distance
                forward()
	    if distance <= 35:
                global recoveryCount
                recoveryCount = recoveryCount + 1
                if recoveryCount < 4: 
                    stop()
                    time.sleep(0.5)
                    print "Distance : %.1fcm < 35cm , need turn left " % distance
	            turn_left()
                    time.sleep(1.45)
	            stop()
                if recoveryCount >= 4:
                    print "Recovery count = %.1f, need to backward" % recoveryCount
                    backward()
                    recoveryCount = 0
                    time.sleep(1)
                    turn_right()
                    time.sleep(1.45)
            time.sleep(0.5)
    except KeyboardInterrupt:    
        GPIO.cleanup()
        recoveryCount = 0

if __name__ == '__main__':
    print "Hi,I'm coprobot, ready to go"
    main(sys.argv)
    autoMove()
#    forward()
#    time.sleep(2220)
#    print "Turn right..."
#    turn_right()
#    time.sleep(200)
#    print "Turn left..."
#    turn_left()
#    time.sleep(200)
#    print "Forward..."
#    backward()
#    time.sleep(100)    
    print "Byebye!"
    stop()
    GPIO.cleanup()
    recoveryCount = 0
