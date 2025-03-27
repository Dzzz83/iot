import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, CallbackAPIVersion
import json
import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

# initialize the counterfit connection  
CounterFitConnection.init('127.0.0.1', 5000)

# setup virtual hardware  
light_sensor = GroveLightSensor(0)  # pin 0 for the light sensor

# device id  
id = '00c3d273-3908-4abc-bf49-da05232ec820'

# unique client name  
client_name = id + 'nightlight_client'

# define the mqtt topic to publish telemetry data  
client_telemetry_topic = id + '/telemetry'

# create the mqtt client instance  
mqtt_client = Client(client_id=client_name, callback_api_version=CallbackAPIVersion.VERSION2)

# connect the client to a public mqtt broker (test.mosquitto.org)  
mqtt_client.connect('mqtt.eclipseprojects.io', port=1883, keepalive=60)

# start the mqtt loop in a background thread to handle network traffic  
mqtt_client.loop_start()

print("mqtt connected!")

# simulated telemetry sending loop  
while True:
    # read from the virtual light sensor  
    light = light_sensor.light  
    
    # create a json payload with the light sensor value  
    telemetry = json.dumps({'light': light})

    print("sending telemetry", telemetry)

    # publish the telemetry data to the mqtt broker  
    mqtt_client.publish(client_telemetry_topic, telemetry)

    # wait for 5 seconds before sending the next reading  
    time.sleep(5)
