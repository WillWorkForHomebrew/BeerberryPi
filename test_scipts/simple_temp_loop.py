#!/usr/bin/python
#from lights import *
from one_wire_temp import *
from heating_element import *
import time, sys, datetime, select, re
from optparse import OptionParser
import RPi.GPIO as GPIO

def main(argv):
    sensor1 = tempSensor("28-000004e0b909")
    sensor2 = tempSensor("28-000004ce5048")
    regEx = re.compile('^q')
    while True:
	if select.select([sys.stdin], [], [], 0)[0]:
		line = sys.stdin.readline()
		if regEx.match(line) is not None:
			#Make sure the heater is off
			sensor1.stop()
			sensor2.stop()
			sys.exit(0)
	curTemp1 = sensor1.getF()
	curTemp2 = sensor2.getF()
	rightNow = datetime.datetime.now().time()
	print curTemp1, curTemp2, rightNow, "\n"
	
	time.sleep(5)

if __name__ == "__main__":
   main(sys.argv[1:])
