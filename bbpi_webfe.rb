require 'haml'
require 'sinatra'
require 'json'
require 'net/http'
require 'uri'


$server='http://127.0.0.1:5000'


# Method to post data
def post (dir, data) #DIR is path to REST, Data is HASH of post data
	address=$server + dir
	uri = URI.parse(address)
	#puts uri.query	
#http = Net::HTTP.new(uri.host, uri.port)
	puts data	
	request=Net::HTTP.post_form(uri,data)	
	puts request.body	#response=http.request(request)
end

#Method to get data
def get (dir) #DIR is path to RES
	begin
		address=$server+dir
		uri = URI.parse(address)
		#http = Net::HTTP.new(uri.host, uri.port)
		request = Net::HTTP.get_response(uri)
		body=request.body
		body=JSON.parse (body)
		puts body	
		code=request.code
		response={'body'=>body,'code'=>code,'exception'=>false}
		return response
		#response=http.request(request)
	rescue Exception =>msg
		response={'body'=>msg,'code'=>401, 'exception' =>true}
		return response
	end
end

configure do
	set :bind, '0.0.0.0'
	set :port, '4567'
end

get '/' do
	settings = get '/bbp/api/v1.0/status/0'
	device1 = get '/bbp/api/v1.0/status/1'
	device2 = get '/bbp/api/v1.0/status/2'
	#puts settings
	if (settings['exception']==true) or (device1['exception']==true) or (device2['exception']==true)
		puts 'warning'
	else
		cycling=settings['body']['device']['Cycling']
		settemp=settings['body']["device"]["Set Temp"]
		dc1tempc=device1['body']["device"]["Temp C"]
		dc1tempf=device1['body']["device"]["Temp F"]
		dc2tempc=device2['body']["device"]["Temp C"]
		dc2tempf=device2['body']["device"]["Temp F"]
	end
	haml :brewhome, :locals => {:temp1=>dc1tempf,:temp2=>dc2tempf,:rsettemp=>settemp,:engaged=>cycling}
end

post '/settemp' do
	temp=params[:htemp]
	cycle_length=params[:hcycle_length]
	duty_cycle=params[:hduty_cycle]
	sensor_id=params[:hsensor_id]
	heating_element_id=0
	#set_temp=220
#	data="cycle_length=#{cycle_length}&duty_cycle=#{duty_cycle}&sensor_id=#{sensor_id}&temp=#{temp}"	
	data = {'cycle_length' => cycle_length, 'duty_cycle' => duty_cycle,'sensor_id' =>sensor_id, 'temp'=>temp, 'heating_element_id' => heating_element_id}
	puts data
	response = post '/bbp/api/v1.0/set_temp', data
	puts response
	redirect '/'
	#haml :brewhome, :locals => {:temp1 => '14',:temp2=>'18',:rsettemp=>$esettemp}
end

get "/brewedit" do
	haml :brewedit, :locals => {:settemp=>"0", :dutycycle=>".5",:cyclelength=>"4",:sensorselect=>"null"}
end

get "/brewstop" do
	settings = get '/bbp/api/v1.0/status/0'
	
	if (settings['exception']==true)
		puts 'warning'
	else
		cycling=settings['body']['device']['Cycling']
	end
	haml :brewstop, :locals => {:engaged=>cycling}
end

post '/stoptemp' do
	data={'heating_element_id'=>'0'}
	response = post '/bbp/api/v1.0/stop_set_temp', data

	redirect '/'
	#haml :brewhome, :locals => {:temp1 => '14',:temp2=>'18',:rsettemp=>$esettemp}
end

=begin
post "/brewpost" do
	$esettemp = params[:settemp]
	redirect '/'
end

get "/brewedit-test" do
	haml :brewedittest
end
=end
