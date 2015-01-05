
# This is a test harness file
require 'haml'
require 'sinatra'
require 'json'
require 'net/http'
require 'jsonify'

#$esettemp="0"
$cycle_length=0
$duty_cycle=0
$heating_element_id
$temp1=82
$temp2=45
$engaged =false
$set_temp=0


def convertc(tempinf)
  tempinc=((tempinf-32)*5/9)
end


configure do
	set :bind, '0.0.0.0'
	set :port, '4568'
end


get '/bbp/api/v1.0/status' do
	# content_type :json

	config = [{"cycle_length"=> @cycle_length, "description" => "Relay with heating element", "dev_id" => 8, "duty_cycle"=> @duty_cycle, "id"=> 0, "type"=> "heating_element"}, {"description"=>"One wire temperature sensor", "dev_id"=> "28-000004e0b909", "id"=>1,"type"=>"temp_sensor"},{"description"=>"One wire temperature sensor", "dev_id"=>"28-000004ce5048", "id"=> 2, "type"=> "temp_sensor"}]
	json = Jsonify::Builder.new(:format => :pretty)
	json.config (config)
	json.compile!
end



get '/bbp/api/v1.0/status/0' do
	data = {"Cycling"=> $engaged, "Number of current cycles"=> 1298, "On"=> 0, "Set Temp"=>$set_temp}
  json = Jsonify::Builder.new(:format => :pretty)
  json.device (data)
  json.compile!
end

get '/bbp/api/v1.0/status/1' do
  data={"Temp C"=> convertc($temp1), "Temp F"=> $temp1}
  json = Jsonify::Builder.new(:format => :pretty)
  json.device (data)
  json.compile!
end

get '/bbp/api/v1.0/status/2' do
  data={"Temp C"=> convertc($temp2), "Temp F"=> $temp2}
  json = Jsonify::Builder.new(:format => :pretty)
  json.device (data)
  json.compile!
end

post '/bbp/api/v1.0/set_temp' do
  $cycle_length = params['cycle_length'] 
  $duty_cycle = params['duty_cycle']
  $sensor_id =params['sensor_id']
  $set_temp = params['temp']
  $heating_element_id = params['heating_element_id']
  $engaged=true
end
  


post '/bbp/api/v1.0/stop_set_temp' do
  $engaged=false
end

