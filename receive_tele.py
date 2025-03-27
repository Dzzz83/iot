import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, CallbackAPIVersion
import json
import time
from counterfit_connection import CounterFitConnection

# initialize the counterfit connection  
CounterFitConnection.init('127.0.0.1', 5000)

# device id  
id = '00c3d273-3908-4abc-bf49-da05232ec820'

# define mqtt topics  
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

# unique client name  
client_name = id + 'nightlight_server'

# create mqtt client  
mqtt_client = Client(client_id=client_name, callback_api_version=CallbackAPIVersion.VERSION2)

# connect to the mqtt broker  
mqtt_client.connect('mqtt.eclipseprojects.io', port=1883, keepalive=60)

# start the mqtt loop in a background thread  
mqtt_client.loop_start()

# function to handle received telemetry  
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("message received:", payload)

# subscribe and set the message handler  
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

# keep the server running  
while True:
    time.sleep(2)
