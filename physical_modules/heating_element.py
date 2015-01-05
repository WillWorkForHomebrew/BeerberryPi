import threading
import time, datetime
import RPi.GPIO as GPIO

class heatingElement:

	def __init__(self,num,cycle,time,logger):
		self.gpio = num
		self.dutyCycle = cycle
		self.cycleTime = time
		self.logger = logger
		self.statusB = 0
		self.cycling = 0
		self.numCycles = 0
		self.setTemp = ''

		# Set up the Relay GPIO
		GPIO.setup(self.gpio, GPIO.OUT)
		GPIO.output(self.gpio, False)
		self.voltage = 240
		self.recalcCycle()
		msg = "Duty Cycle:" + str(self.dutyCycle) + "\t  Cycle Time:" + str(self.cycleTime) + "\t  On Cycle Time:" + str(self.onCycle) + "\t  Off cycle time:" + str(self.offCycle)
		self.logger.debug(msg)

	def recalcCycle(self):
		self.onCycle = self.dutyCycle * self.cycleTime
                self.offCycle = self.cycleTime * (1 - self.dutyCycle)

	def setDutyCycle(self,duty):
		self.dutyCycle = duty
		self.recalcCycle()

	def setCycleTime(self,time):
		self.cycleTime = time
		self.recalcCycle()
	
	def turnOn(self):
		#self.stopCycle()
		self.statusB = 1
		GPIO.output(self.gpio,True)

	def turnOff(self):
		#self.stopCycle()
		self.statusB = 0
		GPIO.output(self.gpio,False)

	def status(self):
		return {
				'On':self.statusB, 
				'Cycling':self.cycling, 
				'Number of current cycles':self.numCycles,
				'Set Temp':self.setTemp
			}

	def cycle(self):
		if self.cycling != 1:
			self.numCycles = 0
			self.cycling = 1
			self.cycleThread = threading.Thread(target=self.cycleT, name="_heat_cycle")
			self.cycleThread.daemon = True
			self.cycleThread.start()

	def set_temp(self,temp,sensor):
		msg = "Temp set at " + str(temp) + ", starting cycle."
		self.logger.info(msg)
		self.setTemp = temp
		if self.cycling != 1:
			self.numCycles = 0
                        self.cycling = 1
                        self.cycleThread = threading.Thread(target=self.cycleT,args=(temp,sensor), name="_heat_cycle")
                        self.cycleThread.daemon = True
                        self.cycleThread.start()
	
	def cycleT(self,temp=220,sensor=''):
		while self.cycling == 1:
			self.numCycles = self.numCycles + 1
			#rightNow = datetime.datetime.now().time()
        		if sensor is None:
				#print rightNow, ", ON,", " set:", temp, "\n"
				msg = "ON, set:" + str(temp)
				self.logger.info(msg)
				self.turnOn()
			elif temp > sensor.getF():
				#print rightNow, ", ON, set:", temp, ", temp:", sensor.getF(), "\n"
				msg = "ON, set:" + str(temp) + ", temp:" + str(sensor.getF())
				self.logger.info(msg)
				self.turnOn()
			else:
				#print rightNow, ", OFF, set:", temp, ", temp:", sensor.getF(), "\n"
				msg = "OFF, set:" + str(temp) + ", temp:" + str(sensor.getF())
				self.logger.info(msg)
			time.sleep(self.onCycle)
			if self.offCycle != 0:
				self.turnOff()
				#rightNow = datetime.datetime.now().time()
				#print "OFF", rightNow, "\n"
				self.logger.info("OFF")
				time.sleep(self.offCycle)
		self.turnOff()

	def stopCycle(self):
		self.logger.info("Stopping cycle")
		if self.cycling != 0:
			self.cycling = 0
			self.cycleThread.join()
			self.setTemp = ''
