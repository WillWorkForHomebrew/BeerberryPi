#!/usr/bin/python
import sys
sys.path.append("/home/enrique/BeerberryPi/physical_modules")
import threading
import logging
from flask import Flask, jsonify, request
from one_wire_temp import *
from heating_element import *

#### Initial config.  These values may change, don't use in the program! ####
config = [
	{
                'id':0,
                'type':'heating_element',
                'description':'Relay with heating element',
                'dev_id':8,
                'cycle_length':4,
                'duty_cycle':1
        },
	{
		'id':1,
		'type':'temp_sensor',
		'description':'One wire temperature sensor',
		'dev_id':'28-000004e0b909'
	},
	{
		'id':2,
		'type':'temp_sensor',
                'description':'One wire temperature sensor',
                'dev_id':'28-000004ce5048'
	}
]
heating_element_default = 0
sensor_default = 1

#### END CONFIG ####
# Set up Logging
logging.basicConfig(filename="/var/log/bbpi_control_api.log", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('BrewData')
logger.setLevel('INFO')

logger.info("Starting BeerberryPi Control API")

devices = {}

for device in enumerate(config):
	device = device[1]
	if device['type'] == 'temp_sensor':
		devices[device['id']] = tempSensor(device['dev_id'],logger)
	if device['type'] == 'heating_element':
		devices[device['id']] = heatingElement(device['dev_id'],device['duty_cycle'],device['cycle_length'],logger)
	msg = devices[device['id']].status()
	logger.debug(msg)

app = Flask(__name__)
app.debug = True
welcomeMessage = "Beerberry Pi Control API v1"


@app.route('/')
def index():
	return welcomeMessage

@app.route('/bbp/api/v1.0/status')
def status():
	return jsonify( {'config':config} )	

@app.route('/bbp/api/v1.0/status/<int:dev_id>')
def dev_status(dev_id):
	return jsonify( {'device':devices[dev_id].status()} )

@app.route('/bbp/api/v1.0/set_temp', methods=['GET','POST'])
def start_cycle():
	heating_element_id = heating_element_default
	if 'heating_element_id' in request.form:
		heating_element_id = int(request.form['heating_element_id'])
	if config[heating_element_id]['type'] != 'heating_element':
		string = "Device " + `heating_element_id` + " is not a heating element"
		return jsonify( {'error': string } )
	
	if 'duty_cycle' in request.form:
		duty_cycle = float(request.form['duty_cycle'])
		if duty_cycle > 0:
			if duty_cycle <= 1:
				devices[heating_element_id].setDutyCycle(duty_cycle)
			else:
				return jsonify( {'error': "Duty cycle must be less than or equal to 1" } )
		else:
			return jsonify( {'error': "Duty cycle must be greater than 0" } )
	if 'sensor_id' in request.form:
		sensor_id = int(request.form['sensor_id'])
	else:
		sensor_id = sensor_default
	if config[sensor_id]['type'] != 'temp_sensor':
		return jsonify( {'error': "Device " + `sensor_id` + " is not a sensor" } )
	
        if 'temp' in request.form:
                temp = int(request.form['temp'])
        else:
                return jsonify( {'error': "Must include temp in request" } )
        
	if 'cycle_length' in request.form:
                cycle_len = int(request.form['cycle_length'])
		if cycle_len > 0:
                        devices[heating_element_id].setCycleTime(cycle_len)
	devices[heating_element_id].set_temp(temp,devices[sensor_id])

	return "Heating device " + `heating_element_id` + "started."

@app.route('/bbp/api/v1.0/stop_set_temp', methods=['GET','POST'])
def stop_cycle():
	if 'heating_element_id' in request.form:
                heating_element_id = int(request.form['heating_element_id'])
        else:
                heating_element_id = heating_element_default

        if config[heating_element_id]['type'] != 'heating_element':
                return jsonify( {'error': "Device " + `heating_element_id` + "is not a heating element" } )
	devices[heating_element_id].stopCycle()
	return "Heating device " + `heating_element_id` + " stopped."

@app.route('/bbp/api/v1.0/exit')
def exit_app():
	return "Exiting"
	sys.exit(0)
	func = request.environ.get('werkzeug.server.shutdown')
   	if func is None:
        	raise RuntimeError('Not running with the Werkzeug Server')
    	func()

if __name__ == '__main__':
	app.run()
        #app.run(host='0.0.0.0')

sys.exit(0)
