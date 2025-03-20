import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, CallbackAPIVersion
import json
import time
from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

id = '00c3d273-3908-4abc-bf49-da05232ec820'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_server'

# Create MQTT client
mqtt_client = Client(client_id=client_name, callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

# Function to handle received telemetry
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    command = { 'led_on' : payload['light'] < 300 }
    print("Sending message:", command)

    client.publish(server_command_topic, json.dumps(command))


# Subscribe and set the message handler
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

# Keep the server running
while True:
    time.sleep(2)
