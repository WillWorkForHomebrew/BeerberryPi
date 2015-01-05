#!/usr/bin/python
#from lights import *
from one_wire_temp import *
from heating_element import *
import time, sys, datetime, select, re
from optparse import OptionParser
import RPi.GPIO as GPIO

def main(argv):
    sensor = tempSensor("28-000004e0b909")
    relayGPIO = 8

    # Get the arguments
    parser = OptionParser()
    parser.add_option("-t", "--temp", type="float", dest="setTemp")
    parser.add_option("-d", "--dutycycle", type="float", dest="dutyCycle")
    parser.add_option("-c", "--cyclelength", type="int", dest="cycleLength", default=4)
    (opts, args) = parser.parse_args()

    # create the heating element
    heater = heatingElement(relayGPIO,opts.dutyCycle,opts.cycleLength) 
    # run the loop
    print "Set Temp is:", opts.setTemp, "\n"
    #print "Duty Cycle is:", opts.dutyCycle, " Cycle Time is:", opts.cycleLength, "\n", "Starting loop", "\n" 

    regEx = re.compile('^q')
    while True:
	if select.select([sys.stdin], [], [], 0)[0]:
		line = sys.stdin.readline()
		if regEx.match(line) is not None:
			#Make sure the heater is off
			heater.stopCycle()
			sys.exit(0)
	curTemp = sensor.getF()
	#curTemp = 70
	rightNow = datetime.datetime.now().time()
	print curTemp, rightNow, "\n"
	
	if curTemp >= opts.setTemp:
	    #Stop heater from cycling, if necessary
	    heater.stopCycle()
	elif curTemp < opts.setTemp:
	    # Cycle the heater, if necessary
    	    heater.cycle()
 	# Sleep a second before re-checking the temp
	time.sleep(1)

if __name__ == "__main__":
   main(sys.argv[1:])
