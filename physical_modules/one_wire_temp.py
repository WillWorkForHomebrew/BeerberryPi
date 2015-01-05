import threading
import time
class tempSensor:

	def __init__(self,num,logger):
		self.dev_num = num
		self.logger = logger
		self.dev_file = "/sys/bus/w1/devices/" + num + "/w1_slave"
		self.currTemp = 0
		self.cycling = 0
		self.start()

	def start(self):
		self.tempThread = threading.Thread(target=self.getCurrTemp, name="_proc")
		self.tempThread.daemon = True
		self.tempThread.start()
		self.cycling = 1 

	def getCurrTemp(self):
		while self.cycling == 1:
			tfile = open(self.dev_file)
			text = tfile.read() 
			tfile.close()
			secondline = text.split("\n")[1]
			tempdata = secondline.split(" ")[9]
			tempC = float(tempdata[2:])
			tempC = tempC / 1000
			self.currTemp = tempC
			msg = "SENSOR ", self.dev_num, ": Read ", tempC
			self.logger.debug(msg) 
			time.sleep(1)
	def getC(self):
		return self.currTemp

	def getF(self):
		tempC = self.getC()
		tempF = tempC * 9/5 + 32
		return tempF

	def status(self):
		return {
				'Temp F':self.getF(),
				'Temp C':self.getC()
			}
	def stop(self):
		self.cycling = 0
		self.tempThread.join()
