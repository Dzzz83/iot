import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, CallbackAPIVersion
import json
import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

from counterfit_shims_grove.grove_led import GroveLed

# Initialize CounterFit connection
CounterFitConnection.init('127.0.0.1', 5000)

# Setup virtual hardware
light_sensor = GroveLightSensor(0)  # Pin 0 for the light sensor
led = GroveLed(1)                   # Pin 1 for the LED

id = '00c3d273-3908-4abc-bf49-da05232ec820'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_combined'

# Create MQTT client
mqtt_client = Client(client_id=client_name, callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

print("MQTT connected!")

# Handle incoming telemetry and send command
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Telemetry received:", payload)
    
    # Send command based on light level
    command = {'led_on': payload['light'] < 300}
    print("Sending command:", command)
    client.publish(server_command_topic, json.dumps(command))

# Handle incoming command to control LED
def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Command received:", payload)

    if payload.get('led_on'):
        led.on()
        print("LED turned ON")
    else:
        led.off()
        print("LED turned OFF")

# Subscribe to topics
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.subscribe(server_command_topic)

# Define handlers for different topics
def on_message(client, userdata, message):
    if message.topic == client_telemetry_topic:
        handle_telemetry(client, userdata, message)
    elif message.topic == server_command_topic:
        handle_command(client, userdata, message)

mqtt_client.on_message = on_message

# Simulate sending telemetry
try:
    while True:
        # Read from the virtual light sensor
        light = light_sensor.light
        telemetry = json.dumps({'light': light})
        print("Sending telemetry:", telemetry)
        
        mqtt_client.publish(client_telemetry_topic, telemetry)
        time.sleep(5)

except KeyboardInterrupt:
    print("\nDisconnecting...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Disconnected gracefully.")
