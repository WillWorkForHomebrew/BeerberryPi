#!/usr/bin/python
from heating_element import *
import time, sys, datetime

def main(argv):
	heater = heatingElement(11,.75,4)

	heater.cycle()
	for count in range(1,10):
		time.sleep(1)
		print "Main THREAD!!\n"
	heater.stopCycle()

if __name__ == "__main__":
	main(sys.argv[1:])
