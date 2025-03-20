import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, CallbackAPIVersion
import json
import time
import random  # Simulate light sensor readings if not using CounterFit
from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

id = '00c3d273-3908-4abc-bf49-da05232ec820'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'

# Create the MQTT client
mqtt_client = Client(client_id=client_name, callback_api_version=CallbackAPIVersion.VERSION2)

# Connect to the MQTT broker
mqtt_client.connect('test.mosquitto.org')

# Start the MQTT loop
mqtt_client.loop_start()

print("MQTT connected!")

# Simulated telemetry sending loop
while True:
    # Simulate a light sensor reading (replace with real sensor if available)
    light = random.randint(0, 100)  
    
    # Create the telemetry JSON payload
    telemetry = json.dumps({'light': light})

    print("Sending telemetry", telemetry)

    # Publish the telemetry to the MQTT broker
    mqtt_client.publish(client_telemetry_topic, telemetry)

    # Wait for 5 seconds before sending the next reading
    time.sleep(5)
