#!usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
import string
import math
import wiringpi
import pdb
#GPIO.setmode(GPIO.BCM)

#Pin connected to ST_CP of 74HC595
latchPin = 22
#Pin connected to SH_CP of 74HC595
clockPin = 9
#Pin connected to DS of 74HC595
dataPin = 10


#pdb.set_trace()
#wiringpi.wiringPiSetup
wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(latchPin,1)
wiringpi.pinMode(clockPin,1)
wiringpi.pinMode(dataPin,1)

# Digit value to bitmask mapping:
DIGIT_VALUES = {
	' ': 0x00,
	'-': 0x40,
	'0': 0xC0,
	'1': 0xF9,
	'2': 0xA4,
	'3': 0xB0,
	'4': 0x99,
	'5': 0x92,
	'6': 0x82,
	'7': 0xF8,
	'8': 0x80,
	'9': 0x90,
	'A': 0x8C,
	'B': 0xBF,
	'C': 0xC6,
	'D': 0xA1,
	'E': 0x86,
	'F': 0xFF,
	'L': 0xC7
}

"""Seven segment LED backpack display."""
class SevenSegment:
    def __init__(self, value, pos):
	self.Value = value
	self.Pos = pos
    def display(self):
#	if self.Pos < 0 | self.Pos > 5:
#	    return
	wiringpi.digitalWrite(22, 0)
	wiringpi.shiftOut(10, 9, 1, DIGIT_VALUES.get(str(self.Value).upper()))
	wiringpi.shiftOut(10, 9, 1, self.Pos)
	wiringpi.digitalWrite(22, 1)
    def cleanup(self):
        wiringpi.pinMode(10,0)
        wiringpi.pinMode(9,0)
        wiringpi.pinMode(22,0)

if __name__ == '__main__':
    try:
        while True:    
            C = SevenSegment('C',8)
            C.display()
#            time.sleep(0.5)   
#   C.display('0',3)
#   C.display('0',2)
#   C.display('L',1)
            O3 = SevenSegment('0',4)
            O3.display()
#            time.sleep(0.5)
            O2 = SevenSegment('0',2)
            O2.display()
#            time.sleep(0.5)
            L = SevenSegment('L',1)
            L.display()
            time.sleep(0.00001)
    except KeyboardInterrupt:
        Reset = SevenSegment(' ',15)
        Reset.cleanup()
