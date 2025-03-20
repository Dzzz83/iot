import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, CallbackAPIVersion
import json
import time
import random

id = '00c3d273-3908-4abc-bf49-da05232ec820'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_device'

# Mock LED class for simulation (replace with actual GPIO LED code)
class LED:
    def on(self):
        print("LED turned ON")

    def off(self):
        print("LED turned OFF")

led = LED()

# Create MQTT client
mqtt_client = Client(client_id=client_name, callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

# Function to handle incoming commands
def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Command received:", payload)

    if payload.get('led_on'):
        led.on()
    else:
        led.off()

# Subscribe to the command topic and attach the handler
mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

# Simulate sending telemetry data (like light levels)
try:
    while True:
        # Simulate light levels (randomized for testing)
        light = random.randint(100, 600)
        telemetry = json.dumps({'light': light})
        print("Sending telemetry:", telemetry)

        mqtt_client.publish(client_telemetry_topic, telemetry)
        time.sleep(5)

except KeyboardInterrupt:
    print("\nDisconnecting...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Disconnected gracefully.")
